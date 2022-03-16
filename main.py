from urllib import request
import urllib
from bs4 import BeautifulSoup
import re


def url_crawler(starter_url):
    r = request.Request(starter_url)
    with request.urlopen(r) as response:
        raw_data = response.read()

    data = raw_data.decode('utf-8')
    useful_data = BeautifulSoup(data)
    url_list = ""
    for link in useful_data.findAll('a', attrs={'href': re.compile("^http://")}):
        url_list += link.get('href')
        url_list += '\n'
    print(url_list)
    return url_list

if __name__ == '__main__':
    starter_url = r'https://en.wikipedia.org/wiki/American_football'


    url_list = url_crawler(starter_url)
    print(url_list)



