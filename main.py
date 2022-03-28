# Justin Liu, Piyush Mewada
# 03/27/2022
# Project 1: Web Scraping
# jtl170000, pxm170012

# This program will create a knowledge base for a topic based on a starting URL
# Input: A URL that links to a webpage that has other URLs as a string the main method
# Output: The top terms in the data collected. A dictionary of the Knowledge Base
# It will also create a lot of files for the data to be stored and a pickle file of the knowledge base


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import io
import os
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
import pickle


# This method go through the inital URL and gets more URLs
# Input: The starting url as a string
# Output: Returns a list of urls as a string
def url_crawler(starter_url):
    req = Request(
        starter_url,
        headers={'User-Agent': 'Mozilla/5.0'})
    # Open and Read the url's webpage
    raw_data = urlopen(req).read()

    data = raw_data.decode('utf-8')
    useful_data = BeautifulSoup(data, features="html.parser")

    url_list = ""
    for link in useful_data.findAll('a', attrs={'href': re.compile("^http://")}):
        if url_list.count('\n') < 30:
            url_list += link.get('href')
            url_list += '\n'
    # print(url_list)
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

    return fileCount


# This function loops through all of the files and tokenizes them into sentences and puts each sentence
# on a new line
# Input: The number of files to go through
# Output: None
def tokenize_sentences(file_count):
    iter = 1
    while iter < file_count:
        # open file and read text
        with open(os.path.join(os.getcwd(), "data" + str(iter) + ".txt"), 'r', encoding='utf-8') as f:
            text_in = f.read()
        # close file
        f.close()

        # Use sent_tokenizer to get the individual sentences
        str_sent_tokens = sent_tokenize(text_in)

        # open file for writing and write each sentence to new line
        curr_file = io.open("data" + str(iter) + ".txt", mode="w", encoding="utf-8")
        for sent in str_sent_tokens:
            curr_file.write(sent)
            curr_file.write('\n')
        curr_file.close()

        iter += 1


# This function gets the top 40 terms from a group of documents using term frequency and returns it.
# Input: The number of files to go through
# Output: A dictionary of the top terms
def get_top_terms(file_count):
    document_arr = []

    # loop through all of the files and put them in the array of documents while doing some whitespace
    # cleaning and removing of punctuation
    iter = 1
    while iter < file_count:
        with open(os.path.join(os.getcwd(), "data" + str(iter) + ".txt"), 'r', encoding='utf-8') as f:
            document_arr.insert(iter - 1, f.read().lower())
        # close file
        f.close()

        document_arr[iter - 1] = re.sub(r"[\s]+", " ", document_arr[iter - 1])
        document_arr[iter - 1] = re.sub(r'[^A-Za-z0-9 ]+', " ", document_arr[iter - 1])
        # print(document_arr[iter - 1])
        iter += 1

    # combine all the documents and get the term frequencies
    all_docs_combined = ""
    for document in document_arr:
        all_docs_combined += document

    # get term frequency dictionary and sort it by largest
    tf_dict = term_freq(all_docs_combined)
    sorted_tf_dict = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
    print("Term Frequencies: ", sorted_tf_dict[:40])
    return sorted_tf_dict[:40]


# This function gets the term frequencies of a particular document, it first checks if the
# word is alphabetical, if it isn't a stopword, and if the length of the word is greater than
# two, it then returns that dict of frequencies back.
# Input: Text that needs to be tokenized and sorted
# Output: A dictionary of the count of term
def term_freq(doc):
    eng_stopwords = stopwords.words('english')
    temp_tf_dict = {}
    doc_tokens = word_tokenize(doc)
    doc_tokens = [w for w in doc_tokens if (w.isalpha() and w not in eng_stopwords and len(w) > 2)]
    for t in doc_tokens:
        if t in temp_tf_dict:
            temp_tf_dict[t] += 1
        else:
            temp_tf_dict[t] = 1
    return temp_tf_dict


# Build Knowledge Base
# Input: The number of files to go through to get the infomation
# Output: The knowledge base dictionary
def createKnowledgeBase(file_count):
    # Create Knowledge Base Dict
    knowledgeBase = {}

    iter = 1
    while iter < file_count:
        # open file and read text
        with open(os.path.join(os.getcwd(), "data" + str(iter) + ".txt"), 'r', encoding='utf-8') as f:
            text_in = f.read()
        # close file
        f.close()

        # Word list for top 10 words
        word_list = ["nfl", "football", "game", "espn", "team", "player", "rules", "playoff", " pro ",
                     "college"]

        # Use sent_tokenizer to get the individual sentences
        str_sent_tokens = sent_tokenize(text_in)
        # For every sentence
        for sent in str_sent_tokens:
            # For every word in the top terms
            for word in word_list:
                # If the word is in the sentence
                if word in sent:
                    # Add or update the knowledge base with the new sentence
                    if word in knowledgeBase:
                        knowledgeBase[word].append(sent)
                    else:
                        knowledgeBase[word] = [sent]

        iter += 1

    # Pickle the knowledge base
    pickle.dump(knowledgeBase, open('knowledgeBase.pickle', 'wb'))

    # Return the output
    return knowledgeBase


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
    # print(urls.count('\n'))

    # Scrape each url
    url_list = urls.splitlines()
    num_files = urlScraper(url_list)

    # Tokenize the sentences in each file
    tokenize_sentences(num_files)

    # Get the top terms
    top_terms = get_top_terms(num_files)

    # Create the Knowledge Base
    createKnowledgeBase(num_files)

    # Unpickle the knowledge base
    kb_pickled = pickle.load(open('knowledgeBase.pickle', "rb"))

    # Print out the knowledge base
    print("\nKnowledge Base:")
    for entry in kb_pickled:
        print(entry, ":", kb_pickled[entry])
