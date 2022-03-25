# Justin Liu, Piyush Mewada
# 03/27/2022
# Project 1: Web Scraping
# jtl170000, pxm170012


from urllib import request
import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import io


def url_crawler(starter_url):
    r = request.Request(starter_url)
    with request.urlopen(r) as response:
        raw_data = response.read()

    data = raw_data.decode('utf-8')
    useful_data = BeautifulSoup(data, features="html.parser")

    url_list = ""
    for link in useful_data.findAll('a', attrs={'href': re.compile("^http://")}):
        if url_list.count('\n') < 30:
            url_list += link.get('href')
            url_list += '\n'
    print(url_list)
    return url_list


# This method checks for if the elements on a webpage are visible and relevant
# It only returns True if the element is not a part of a style, script, document, head, title, or comment
# Inputs: An element from a webpage
# Outputs: True or False based on if the input is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


# This method scrapes a list of urls for the text on the page.
# Inputs: A list of urls to scrape
# Outputs: It does not return anything. It just creates the files in the same directory.
def urlScraper(url_list):
    # Count how many files have been made
    fileCount = 1
    # For each url in the list
    for my_url in url_list:
        # Open/Create a file to store all the text
        file = io.open("data" + str(fileCount) + ".txt", mode="w", encoding="utf-8")
        # Try to open the webpage, if there is an error opening or reading the page, skip it
        try:
            # Request the webpage to open using this browser, this allows the crawler to go on sites that might block
            # bots from entering
            req = Request(
                my_url,
                headers={'User-Agent': 'Mozilla/5.0'})
            # Open and Read the url's webpage
            html = urlopen(req).read()
            # Parse the page
            soup = BeautifulSoup(html, features="html.parser", from_encoding="iso-8859-1")
            # Get all the text data from the page
            data = soup.findAll(text=True)
            # Filter out all the invisible text
            result = filter(visible, data)
            # Create a list from the filter
            temp_list = list(result)
            # Combine the temp_list
            temp_str = ' '.join(temp_list)
            # Clean up the text
            temp_str = cleanUpText(temp_str)
            # Write cleaned up text to the file
            file.write(temp_str)
            # Increment the file count
            fileCount += 1
        except:
            pass
    # Close the file
        file.close()


# This method clean up a string of text
# It removes all the new lines and tabs and converts groups spaces to just one space
# Input: A string to be cleaned up
# Output: A string value that has been cleaned
def cleanUpText(text):
    text = re.sub('[\n\r\t]+', "", text)
    text = re.sub(' +', " ", text)
    return text


# Main Methods
if __name__ == '__main__':
    # This is our starting URL
    start_url = r'https://en.wikipedia.org/wiki/American_football'

    # Get a list of URLs from starter
    urls = url_crawler(start_url)
    print(urls.count('\n'))

    # Scrape each url
    url_list = urls.splitlines()
    urlScraper(url_list)
