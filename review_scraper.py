from pprint import pprint
import requests
from bs4 import BeautifulSoup
import sys
import re
import urllib
import pdb


review_base_url = "https://www.google.com/async/reviewSort?async=feature_id:{},next_page_token:{},_fmt:pc"

# HTML Format


# Stars

# <div class="gws-localreviews__google-review">
#   <a>
#   <div>
#     <div>
#     <g>
#     <div>
#     <div>
#       <div>
#         <div>
#           <div>
#             <span aria="Rated 5 out of 5">
#             <span>
#             <span>
#         <div>
#   <div>
#   <div?> Picture
#   <div (Last)>
#     <div>
#       <div>
#         <div>
#           <div>
#           <div>
#             Response from owner
#         <div>


def get_reviews_sub(url, num_reviews=50, next_token=""):

    # num_reviews = int(num_reviews,10)
    company_id = re.search(r"lrd\=(.*?),", url).groups()[0]
    reviews = []

    while True:

        review_url = review_base_url.format(company_id, next_token)

        print(review_url)
        # Making a GET request
        r = requests.get(review_url)

        next_token = re.search(r"data-next-page-token=\"(.*?)\"", r.text).groups()[0]

        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')

        review_divs = soup.find_all(class_="gws-localreviews__google-review")

        for review_div in review_divs:
            # pdb.set_trace()
            owner_response = review_div.contents[-1].div.div
            if owner_response:
                owner_response = owner_response.div.contents[1].get_text()
            # print("Response from owner ", owner_response)
            review_contents = review_div.div.contents
            name = review_contents[0].get_text()
            review_text = ""
            star_text = review_contents[3].div.div.div.span['aria-label']
            # print(star_text)
            star_val = re.match(r"Rated (.*) out of 5", star_text)
            assert star_val, "Rating does not match the designed regex pattern"
            star_val = star_val.groups()[0]
            # print(int(star_val))
            for text in review_contents[3].div.div.div.next_sibling.stripped_strings:
                review_text = text
                break

            if review_text:
                reviews.append({'name': name, 'review':review_text, 'rating': star_val, 'owner_response':owner_response})

        if len(reviews) >= num_reviews or not next_token:
            break

    return reviews, next_token



def get_reviews(url):

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
