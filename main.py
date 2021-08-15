import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import constants as cons
import time
from nltk.corpus import stopwords

driver = webdriver.Firefox()


def search_business(key_word="bubble tea", location="Nashville, TN"):
    driver.get("http://www.yelp.com")
    search_location = driver.find_element_by_id(cons.SEARCH_LOCATION_ID)
    search_location.clear()
    search_location.send_keys(location)
    search_keyword = driver.find_element_by_id(cons.SEARCH_KEYWORD_ID)
    search_keyword.send_keys(key_word)
    search_btn = driver.find_element_by_id(cons.SEARCH_BTN_ID)
    search_btn.send_keys(Keys.RETURN)


def get_current_page_business():
    businesses_on_page = driver.find_elements_by_xpath(cons.BUSINESS_CARD_XPATH)
    return businesses_on_page


def get_business_page_num():
    time.sleep(5)
    pages = driver.find_elements_by_xpath(cons.BUSINESS_PAGES_XPATH)
    return len(pages)


def click_next_page_btn():
    next_page_btns = driver.find_elements_by_xpath(cons.NEXT_PAGE_BTN_XPATH)
    if len(next_page_btns) > 1:
        next_page_btns[1].send_keys(Keys.RETURN)
    else:
        next_page_btns[0].send_keys(Keys.RETURN)


def parse_comment(bus_name, comment_writer):
    comments = driver.find_elements_by_xpath(cons.COMMENT_XPATH)
    ratings = driver.find_elements_by_xpath(cons.RATING_XPATH)
    for idx in range(len(comments)):
        rating_attribute = ratings[idx].get_attribute("aria-label")
        rating = str(rating_attribute)[0]
        comment_writer.writerow({'business': str(bus_name), 'comment': str(comments[idx].text), 'rating': rating})


def scrape_yelp_comment(search_term, location):
    search_business(search_term, location)
    page_num = get_business_page_num()
    with open("reviews.csv", 'w', newline='') as csv_file:
        fieldnames = ['business', 'comment', 'rating']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, 2):
            print("crawling page " + str(i) + " of search result")
            time.sleep(2)
            businesses = get_current_page_business()
            for index in range(0, len(businesses)):
                businesses = get_current_page_business()
                business_name = businesses[index].text
                print("crawling " + business_name)
                businesses[index].send_keys(Keys.RETURN)
                time.sleep(2)
                review_page_num = get_business_page_num()
                if review_page_num != 0:
                    real_page_num = 1
                    while True:
                        try:
                            time.sleep(2)
                            print("crawling review page " + str(real_page_num))
                            parse_comment(business_name, writer)
                            click_next_page_btn()
                            real_page_num += 1
                        except:
                            break
                    while real_page_num != 1:
                        print("back to previous page " + str(real_page_num))
                        driver.back()
                        time.sleep(2)
                        real_page_num -= 1
                else:
                    time.sleep(2)
                    print("crawling only page of review")
                    parse_comment(business_name, writer)
                driver.back()
            click_next_page_btn()
    driver.close()


def write_data_to_csv():
    f = open("reviews.txt", "a")
    with open('reviews.csv', mode='r') as csv_files:
        csv_reader = csv.DictReader(csv_files)
        for row in csv_reader:
            f.write(row['comment'])
    f.close()


def clean_comments():
    # data cleaning
    # word_tokenize accepts a string as an input, not a file.
    stop_words = set(stopwords.words('english'))
    file1 = open("reviews.txt")
    line = file1.read()  # Use this to read file content as a stream:
    words = line.split()
    for r in words:
        if not r in stop_words:
            append_file = open('reviews_filtered.txt', 'a')
            append_file.write(" " + r)
            append_file.close()


if __name__ == '__main__':
    scrape_yelp_comment("Bubble Tea", "Nashville")
    write_data_to_csv()
    clean_comments()
