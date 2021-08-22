#B1709552
#Do Trung Nguyen
#KKDL: crawling data facebook without acc

from selenium import webdriver
from time import sleep
import random
import re
import emojis
import json
from collections import OrderedDict # giữ nguyên thứ trự element truyền vào dict

# 1. Khai báo browser
DRIVER_PATH = './chromedriver.exe' # đường dẫn đến driver
#URL_PAGE = 'https://www.facebook.com/pg/truyentranhnhamnhi/posts/?ref=page_internal'

URL_PAGE = 'https://www.facebook.com/CTUDHCT/'

POST_MESSAGE_XPATH = '//*[@data-testid="post_message"]'
# POST_XPATH = '//*[@data-visualcompletion="ignore-dynamic"]'
# URL_POST_XPATH = '//*[@class="_5pcq"]'

def scrape_post():
    post_data = OrderedDict()
    post_data['url_page'] = URL_PAGE

    driver  = webdriver.Chrome(DRIVER_PATH)
    driver.get(URL_PAGE)

    sleep(random.randint(8, 14))
    post_data['title'] = driver.title

    post_data['post_message'] = list()
    post_message = driver.find_elements_by_xpath(POST_MESSAGE_XPATH)
    for pm in post_message:
        message = format_message(pm)
        post_data['post_message'].append(message)

    return post_data

def format_message(post_message):
    message = {}
    message_text = post_message.find_element_by_tag_name('p')
    text = message_text.text

    message['hashtag'] = getHashtag(text)

    message['emoji'] = getEmoji(text)

    message['text'] = getText(text,message['emoji'],message['hashtag'])

    return message

# lấy base text và loại hashtag, emoji
def getText(text,emoji_list,hashtag_list):
    text = emojis.decode(text)
    #text = re.split(r'^:.+:$',text)
    for e in emoji_list:
        if e in text:
            text = text.replace(e,'')
    
    for h in hashtag_list:
        if h in text:
            text = text.replace('#'+h,'')

    return text

# lấy hashtag
def getHashtag(text):
    return [tag.strip("#") for tag in text.split() if tag.startswith("#")]

# lấy emoji
def getEmoji(text):
    emoji = []
    for e in emojis.get(text):
       emoji.append(emojis.decode(e))
    return emoji


if __name__ == "__main__":

    post_data = scrape_post()

    # in ra
    print(json.dumps(post_data,ensure_ascii=False, indent=2))

    # ensure_ascii=False để lưu Tiếng Việt
    with open('data.json', 'w', encoding='utf-8') as file: # file nằm ở thư mục cá nhân
        json.dump(post_data, file,ensure_ascii=False)
 
    