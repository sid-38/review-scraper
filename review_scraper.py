import requests
from bs4 import BeautifulSoup
import sys
import re
import urllib
import pdb

# URL that loads a window of reviews, decided by the next page token.
# Arguments
#   1. "lrd" token from the google reviews url
#   2. next page token available in the previous reviews (lazy loading)

reviews_url = "https://www.google.com/async/reviewSort?async=feature_id:{},next_page_token:{},_fmt:pc"

# URL for a specific review
# Arguments
#   1. review_id
#   2. 2nd part of lrd. lrd would be of the format .*:.*  
# Latitude and Longitude can be given as 0, and it would get adjusted automatically by gmaps
review_share_url = "https://www.google.com/maps/reviews/@0,0,17z/data=!3m1!4b1!4m6!14m5!1m4!2m3!1s{}!2m1!1s0x0:{}"

# HTML XPATHS
#   Reivew Text (more) - //*[@id="reviewSort"]/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[2]/span/span/span[1]/span
#   Reivew Text (more) - //div[@class="gws-localreviews__google-review"]/div[1]/div[3]/div/div[1]/div[2]/span/span/span[1]/span
#   Review Text - //div[@class="gws-localreviews__google-review"]/div[1]/div[3]/div/div[1]/div[2]/span/span
#   Star rating - //div[@class="gws-localreviews__google-review"]/div[1]/div[3]/div/div[1]/div[1]/span[1]
#   Owner response - //div[@class="gws-localreviews__google-review"]/div[-1]/div/div/div[1]/div[2]



def get_reviews_lazy(url, num_reviews=50, next_token=""):

    lrd = re.search(r"lrd\=(.*?),", url).groups()[0]
    reviews = []
    lrd_2 = re.search(r".*:(.*)", lrd).groups()[0]

    while True:

        review_url = reviews_url.format(lrd, next_token)
        
        r = requests.get(review_url)

        next_token = re.search(r"data-next-page-token=\"(.*?)\"", r.text).groups()[0]

        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')

        review_divs = soup.find_all(class_="gws-localreviews__google-review")

        for review_div in review_divs:
            review_id = re.search(r'data-ri="(.*?)"', str(review_div)).groups()[0]
            review_url = review_share_url.format(review_id,lrd_2)

            owner_response = review_div.contents[-1].div.div
            if owner_response:
                owner_response = owner_response.div.contents[1].get_text()

            review_contents = review_div.div.contents
            name = review_contents[0].get_text()
            review_text = ""
            star_text = review_contents[3].div.div.div.span['aria-label']
            star_val = re.match(r"Rated (.*) out of 5", star_text)
            assert star_val, "Rating does not match the designed regex pattern"
            star_val = star_val.groups()[0]
            
            for text in review_contents[3].div.div.div.next_sibling.stripped_strings:
                review_text = text
                break

            if review_text:
                reviews.append({'name': name, 'review':review_text, 'rating': star_val, 'owner_response':owner_response, 'review_url': review_url})

        if len(reviews) >= num_reviews or not next_token:
            break

    return reviews, next_token



def get_all_reviews(url):

    reviews = []
    new_token = ""
    while True:
        print("Fetching reviews")
        new_reviews, new_token = get_reviews_lazy(url, new_token)
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
    print(get_all_reviews(url))
