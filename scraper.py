from selenium import webdriver
from tqdm import tqdm

import pandas as pd 

import json
import time
import sys
import os

def get_comment(driver, path_to_post):
    user_comments = []

    driver.get(path_to_post)
    try:
        close_button = driver.find_element_by_class_name('xqRnw')
        close_button.click()
    except:
        pass


    try:
        load_more_comment = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button')
        i = 0
        while load_more_comment.is_displayed():
            load_more_comment.click()
            i += 1
            time.sleep(3)
    except:
        pass


    description = driver.find_element_by_class_name('C4VMK')
    description = description.find_elements_by_tag_name('span')[1].text

    comment = driver.find_elements_by_class_name('gElp9 ')
    for c in comment:
        container = c.find_element_by_class_name('C4VMK')
        content = container.find_element_by_tag_name('span').text
        content = content.replace('\n', ' ').strip().rstrip()
        user_comments.append(content)

    user_comments.pop(0)

    return description, user_comments


def main():

    driver = webdriver.Chrome()


    links = pd.read_csv('links.csv',header=None)
    
    with open('comments.json','w', encoding='utf-8') as f_json:
        f_json.write('[\n')
        for idx, link in tqdm(links.iterrows()):
            try:
                description, comments = get_comment(driver, link[0])
                data = {'описание': description, 'комменты': comments}
                out = json.dumps(data, ensure_ascii=False)
                print(f'\t{out},', file=f_json)
            except:
                pass
                
        f_json.seek(0, os.SEEK_END)
        f_json.seek(f_json.tell() - 3, os.SEEK_SET)
        f_json.write('\n]')

    driver.close()

if __name__ == '__main__':
    main()