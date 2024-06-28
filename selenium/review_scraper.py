from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By

link = "https://www.google.com/search?q=smrt+system&oq=smrt+system&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARBFGDsyBggCEEUYOzIGCAMQRRg8MgYIBBBFGDwyBggFEEUYPDIGCAYQLhhA0gEIMTMyNGowajmoAgCwAgE&sourceid=chrome&ie=UTF-8#lrd=0x89ac9179732ea44f:0xaa22124a29eb61d3,1,,,,"


def get_review_text(element):

    review_spans= element.find_elements(By.XPATH, './div[1]/div[3]/div/div[1]/div[2]/span//*')
    # Review is small and does not have a snippet section
    if len(review_spans) == 1:
        review_data = review_spans[0].get_attribute('innerText')

    # Review is big and has to ignore the snipper section to get the full text
    else:
        review_data = review_spans[0].find_element(By.XPATH, './span[1]/span').get_attribute('innerText')
    return review_data

        

def get_review_data(element):
    print(get_review_text(element))

driver = webdriver.Chrome()

driver.get(link)
driver.implicitly_wait(10)

max_reviews = 50


elements = driver.find_elements(By.CLASS_NAME, "gws-localreviews__google-review")
driver.execute_script("arguments[0].scrollIntoView(true);", elements[-1])
# driver.implicitly_wait(5)
elements = driver.find_elements(By.CLASS_NAME, "gws-localreviews__google-review")
# print([x.text for x in elements])
# pprint([get_review_data(x) for x in elements])
for element in elements:
    get_review_data(element)


driver.quit()
