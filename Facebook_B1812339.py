# Credit: Nguyen Thanh Hoang Hai

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException



if __name__ == "__main__":
    comment_button_class = "_15kq"
    more_comments_xpath = '//*[@id="m_story_permalink_view"]//div[@class="async_elem"]/a'
    user_xpath = '//div[@class="_2b05"]'
    comment_xpath = "//div[@data-commentid]"

    url = input("Input facebook post url you want to crawl comment (e.g: https://www.facebook.com/daa.ctu.edu.vn/posts/3745882885460437):\n")

    # use mobile version of facebook
    url = url.replace('www.', '').replace("//facebook", "//mobile.facebook")

    try:
        driver = webdriver.Firefox()
    except WebDriverException:
        print("\nPlease install Firefox and download geckodriver at https://github.com/mozilla/geckodriver/releases")
        input("\nPress enter to close")
        quit()

    driver.get("https://www.facebook.com")
    input("Please login then press enter to start crawling")

    driver.get(url)

    # workaround for video post ex: https://www.facebook.com/LienquanMobile/posts/2838238359809802
    time.sleep(3)
    try:
        comment_href = driver.find_element(By.CLASS_NAME, comment_button_class)
        comment_href.click()
    except NoSuchElementException:
        print("This post seems doesn't have Comment button")

    previous_comments = True
    while previous_comments:
        time.sleep(3)
        try:
            more_comments_link = driver.find_element(By.XPATH, more_comments_xpath)
            print("Found more comments link:"+more_comments_link.get_attribute("href"))
            more_comments_link.click()
        except NoSuchElementException:
            print('There is no "View previous comments…"')
            previous_comments = False

    users = driver.find_elements(By.XPATH, user_xpath)
    comments = driver.find_elements(By.XPATH, comment_xpath)

    with open("Facebook_B1812339.csv", 'w', encoding="utf-8", newline='') as csvfile:
        crawl_writer = csv.DictWriter(csvfile, fieldnames=['index', "name", "profile link", "comment"])
        crawl_writer.writeheader()

        for i in range(len(users)):
            crawl_data = dict()
            
            crawl_data["index"] = i
            crawl_data["name"] = users[i].text
            try:
                crawl_data["profile link"] = users[i].find_element(By.TAG_NAME, 'a').get_attribute("href").replace("//mobile", "//www")
            except NoSuchElementException:
                pass
            crawl_data["comment"] = comments[i].text
            print(crawl_data)

            crawl_writer.writerow(crawl_data)

    input("\nDone! Press enter to close")
    driver.close()