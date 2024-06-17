from pprint import pprint
import requests
from bs4 import BeautifulSoup
import sys
import re
import urllib


review_base_url = "https://www.google.com/async/reviewSort?async=feature_id:{},next_page_token:{},_fmt:pc"


def get_reviews_sub(url, next_page_token=""):

    company_id = re.search(r"lrd\=(.*?),", url).groups()[0]

    review_url = review_base_url.format(company_id, next_page_token)

    print(review_url)
    # Making a GET request
    r = requests.get(review_url)

    next_token = re.search(r"data-next-page-token=\"(.*?)\"", r.text).groups()[0]

    # check status code for response received
    # success code - 200
    # print(r.text)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    # next_token = soup.find(attrs={"name": "data-next-page-token"})
    review_divs = soup.find_all(class_="gws-localreviews__google-review")
    reviews = []
    for review_div in review_divs:
        review_contents = review_div.div.contents
        name = review_contents[0].get_text()
        review_text = ""
        for text in review_contents[3].div.div.div.next_sibling.stripped_strings:
            review_text = text
            break

        if review_text:
            reviews.append({'name': name, 'review':review_text})
    # reviews = [x.get_text(" ") for x in review_divs]
    return reviews, next_token



# print(get_reviews_sub())
def get_reviews(url):

    # company_id = re.search(r"lrd\=(.*?),", url).groups()[0]
    reviews = []
    new_token = ""
    while True:
        print("Fetching reviews")
        new_reviews, new_token = get_reviews_sub(url, new_token)
        reviews.extend(new_reviews)
        # break
        if new_token == "":
            break
    return reviews

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Usage error')
        sys.exit(1)

    url = sys.argv[1]
    print(get_reviews(url))
