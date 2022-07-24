#!/usr/bin/env python3

import argparse
import requests
import sys
from bs4 import BeautifulSoup as bs
from publicsuffixlist import PublicSuffixList
from collections import deque
import json



# a function that extracts hyperlinks using requests from a given url
def scrapeHyperlinksFromURL(url):
    # get the html from the url
    html = requests.get(url).text
    # create a BeautifulSoup object from the html
    soup = bs(html, 'html.parser')
    # find all the hyperlinks in the html
    hyperlinks = soup.find_all('a')
    # create a list of hyperlinks
    hyperlinkList = []
    # iterate through the hyperlinks
    for link in hyperlinks:
        # if the link is not empty
        if link.get('href') != None:
            # add the link to the list
            cleanedLink = link.get('href')
            if cleanedLink[0:2] == "//":
                cleanedLink = "http:" + cleanedLink
            elif cleanedLink[0:1] == "/":
                if url[-1] == "/":
                    cleanedLink = url + cleanedLink[1:]
                else:
                    cleanedLink = url + cleanedLink
            hyperlinkList.append(cleanedLink)
    # return the list of hyperlinks
    return hyperlinkList


def runScrape(startUrl, limit):
    count = 0
    # url = startUrl
    hyperlinks = deque()
    hyperlinks.append(startUrl)

    # print(hyperlinks)

    visitedlinks = set()

    resultDict = {}

    while count < limit:
        link = hyperlinks[0]
        if link[0:2] == "//":
            link = "http:" + link
        # Don't scrape the same URL twice
        if link not in visitedlinks:
            visitedlinks.add(link)
            
            print("Scraping: " + link)
            pagelinks = scrapeHyperlinksFromURL(link)
            
            if link not in resultDict:
                resultDict[link] = {"outgoing": pagelinks}
            elif "outgoing" not in resultDict[link]:
                resultDict[link]["outgoing"] = pagelinks

            # Add the new links to the queue
            hyperlinks.extend(pagelinks)

            # Track total number of scrapes
            count += 1
            print("Scraped " + str(count) + " pages")

        # Remove the processed URL
        hyperlinks.popleft()

        for outgoinglink in pagelinks:
            if outgoinglink not in resultDict:
                resultDict[outgoinglink] = {"incoming": [link]}
            elif "incoming" not in resultDict[outgoinglink]:
                resultDict[outgoinglink]["incoming"] = [link]
            else:
                resultDict[outgoinglink]["incoming"].append(link)

        # If the queue is empty, we're done
        if len(hyperlinks) == 0:
            break
    
    with open("links.json", "w") as write_file:
        json.dump(resultDict, write_file, indent=4)
    
    return resultDict


if __name__ == "__main__":
    # build the parser
    parser = argparse.ArgumentParser(
        description='traverse the Web as a linked graph from the starting --url \
                    finding all outgoing links (<a> tag): it will store each outgoing link \
                    for the URL, and then repeat the process for each of them, until \
                    --limit URLs will have been traversed.', 
                    epilog='Example: hyperlinks.py https://docs.python.org/')

    parser.add_argument('--url', help='Starting URL')
    parser.add_argument('--limit', help='Number of URLs to traverse', type=int, default=1000, action='store')

    # ensure that no args is a help call
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    arguments = parser.parse_args()

    # catch urls without https://
    url = arguments.url
    if not arguments.url.startswith('https://') and not arguments.url.startswith('http://'):
        print('No schema detected, attempting to use http://')
        url = 'http://' + arguments.url
    # use publicsuffixlist to get domain from url
    # url = arguments.url.split('//')[1].split('/')[0]
    # domain = PublicSuffixList().privatesuffix(url)

    # regex to select domain from url
    # domain = arguments.url.split('//')[1].split('/')[0]

    # 

    # print("Domain: ", domain)


    

    print("Starting URL: " + url)
    print("Limit: " + str(arguments.limit))


    runScrape(url, arguments.limit)
