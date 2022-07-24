#!/usr/bin/env python3

import argparse
import requests
# import sys
from bs4 import BeautifulSoup as bs
# from publicsuffixlist import PublicSuffixList
from collections import deque
import json


# JSON Encoder class for serializing sets
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

# Save results to JSON file "out"
def saveToJSON(resultDict, out):
    if out[-5:] == ".json":
        with open(out, 'w') as f:
            json.dump(resultDict, f, indent=4, cls=SetEncoder)
    else:      
        with open(out + ".json", "w") as f:
            json.dump(resultDict, f, indent=4, cls=SetEncoder)

# Clean links to remove parameters and fragments
def cleanLink(link, url):
    if link[0:2] == "//":
        cleanedLink = "http:" + link
    elif link[0:1] == "/" or "//" not in link:
        if url[-1] == "/":
            cleanedLink = url + link[1:]
        else:
            cleanedLink = url + link
    else:
        cleanedLink = link

    if "?" in cleanedLink:
        cleanedLink = cleanedLink.split("?")[0]
    
    return cleanedLink
    
    
# Extract hyperlinks from a URL
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
        if link.get('href') != None:
            link = link.get('href')

            # Skip same-page links
            if link[0] == "#":
                continue
            
            # Clean up the link
            cleanedLink = cleanLink(link, url)
            
            hyperlinkList.append(cleanedLink)

    # return the list of hyperlinks
    return hyperlinkList


def runScrape(startUrl, limit, out=None):
    count = 0
    # url = startUrl
    hyperlinks = deque()
    hyperlinks.append(startUrl)

    visitedlinks = set()

    resultDict = {}

    while count < limit:
        link = hyperlinks[0]

        # Don't scrape the same URL twice
        if link not in visitedlinks:
            visitedlinks.add(link)
            
            print("Scraping: " + link)
            pagelinks = scrapeHyperlinksFromURL(link)
            
            # Add data to the result dictionary
            if link not in resultDict:
                resultDict[link] = {"outgoing": pagelinks}
            elif "outgoing" not in resultDict[link]:
                resultDict[link]["outgoing"] = pagelinks

            # Add the new links to the queue
            hyperlinks.extend(pagelinks)

            # Track total number of scrapes
            count += 1
            if count == 1:
                print("Scraped " + str(count) + " page")
            else:
                print("Scraped " + str(count) + " pages")

        # Remove the processed URL
        hyperlinks.popleft()

        # Create dictionary entries with incoming data for all scraped links
        for outgoinglink in pagelinks:
            if outgoinglink not in resultDict:
                # Using sets because some sites (facebook for example) love linking to their own pages... hundreds of times....
                resultDict[outgoinglink] = {"incoming": set([link])}
            elif "incoming" not in resultDict[outgoinglink]:
                resultDict[outgoinglink]["incoming"] = set([link])
            else:
                resultDict[outgoinglink]["incoming"].add(link)

        # If the queue is empty, we're done
        if len(hyperlinks) == 0:
            break
    
    # Write results to json file, or stdout if no output file is specified
    if out is not None:
        saveToJSON(resultDict, out)
    else:
        print(resultDict)

    return resultDict


if __name__ == "__main__":
    # build the parser
    parser = argparse.ArgumentParser(
        description='traverse the Web as a linked graph from the starting --url \
                    finding all outgoing links (<a> tag): it will store each outgoing link \
                    for the URL, and then repeat the process for each of them, until \
                    --limit URLs will have been traversed.', 
                    epilog='Example: hyperlinks.py --url https://docs.python.org/ --limit 10 --out links.json')

    parser.add_argument('--url', help='Starting URL', required=True)
    parser.add_argument('--limit', help='Number of URLs to traverse', type=int, default=1000, action='store', required=True)
    parser.add_argument('--out', help='Number of URLs to traverse', type=str, action='store')

    # ensure that no args is a help call
    # if len(sys.argv)==1:
    #     parser.print_help(sys.stderr)
    #     sys.exit(1)

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

    if arguments.out:
        runScrape(url, arguments.limit, arguments.out)
    else:
        runScrape(url, arguments.limit)
