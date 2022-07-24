#!/usr/bin/env python3

import argparse
import requests
import sys
from bs4 import BeautifulSoup as bs


# def scrapeImageLinksFromIssue(url, lowres):
#     req = requests.get(url, headers)
#     soup = bs(req.content, 'html.parser')
#     soup = soup.prettify()
#     lines = soup.split("\n")
#     imageLinks = []

#     for line in lines:
#         if "https://2.bp.blogspot.com" in line:
#             imageUrl = extractImageUrlFromText(line, lowres)
#             imageLinks.append(imageUrl)

#         if checkForCaptcha(line):
#             solveCaptcha(url)
#             return scrapeImageLinksFromIssue(url, lowres)

#     return imageLinks


if __name__ == "__main__":
    # build the parser
    parser = argparse.ArgumentParser(
        description='traverse the Web as a linked graph from the starting --url \
                    finding all outgoing links (<a> tag): it will store each outgoing link \
                    for the URL, and then repeat the process for each of them, until \
                    --limit URLs will have been traversed.', 
                    epilog='Example: hyperlinks.py https://docs.python.org/')

    parser.add_argument('--url', '--url', help='Starting URL')
    parser.add_argument('--limit', '--limit', help='Number of URLs to traverse', type=int, default=1000, action='store')

    # ensure that no args is a help call
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    arguments = parser.parse_args()

    print("Starting URL: " + arguments.url)
    print("Limit: " + str(arguments.limit))


    # if arguments.selenium == True and arguments.selenium_display == True:
    #     print("Please provide only -s or -sd, not both")
    #     print("Quitting")
    #     quit()

    # # set variables from arguments
    # startURL = arguments.URL
    # singleIssue = False
    # if "?id=" in startURL:
    #     singleIssue = True
    #     print("You have provided the link for a single issue.")
    #     print("When providing the URL for the info page, this script will download all issues in the series.")

    # if arguments.folder != None:
    #     print(f"Title detected, using {arguments.folder} as title")
    #     comicTitle = arguments.folder
    # else:
    #     print("No title specified. Reading title from Url...")
    #     comicTitle = getComicTitle(startURL, singleIssue)
    #     print(f"Using title: {comicTitle}")

    # downloadFull = False
    # if arguments.complete == True and singleIssue == False:
    #     print("Argument -c detected and comic info URL supplied. Downloading entire comic into one folder")
    #     downloadFull = True

    # lowres = False
    # if arguments.lowres == True:
    #     print("Argument -l detected. Downloading low resolution images")
    #     lowres = True
    # else:
    #     print("Downloading max quality images")

    # useSelenium = False
    # if arguments.selenium == True:
    #     print("Argument -s detected. Using Selenium to scrape the page(s)")
    #     useSelenium = True

    # seleniumDisplay = False
    # if arguments.selenium_display == True:
    #     print("Argument -sd detected. Using Selenium in display mode")
    #     useSelenium = True
    #     seleniumDisplay = True

    # disableWait = False
    # if arguments.disable_wait == True:
    #     print("Argument -d detected. Disabling wait between requests")
    #     print("This may cause CAPTCHAs to appear more often.")
    #     disableWait = True

    # issueStart = 0
    # if arguments.issue == True:
    #     print("Argument -i detected.")
    #     print("This is an experimental feature. Use at your own risk. Meant to be used when the script has crashed partway through a series.")
    #     issueStart = input("What issue would you like to start with? enter an integer: ")

    # print(f"Starting to scrape {comicTitle} from {startURL}")

    # main(downloadFull, singleIssue, comicTitle, lowres, disableWait, startURL, useSelenium, seleniumDisplay, issueStart)
    # print("\nComic Downloaded")