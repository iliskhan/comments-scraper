from selenium import webdriver
from tqdm import tqdm

import pandas as pd 

import excel_exporter
import time
import sys

def get_comment(driver, path_to_post):
    user_names = []
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
        while load_more_comment.is_displayed() and i < sys.argv[2]:
            load_more_comment.click()
            i += 1
            time.sleep(3)
    except:
        pass


    comment = driver.find_elements_by_class_name('gElp9 ')
    for c in comment:
        container = c.find_element_by_class_name('C4VMK')
        name = container.find_element_by_class_name('_6lAjh').text
        content = container.find_element_by_tag_name('span').text
        content = content.replace('\n', ' ').strip().rstrip()
        user_names.append(name)
        user_comments.append(content)

 
    return user_names, user_comments


def main():

    driver = webdriver.Chrome()

    user_names = []
    user_comments = []

    links = pd.read_csv('links.csv',header=None)
    
    for idx, link in tqdm(links.iterrows()):
        names, comments = get_comment(driver, link[0])
        user_names.extend(names)
        user_comments.extend(comments)

    print(len(user_names), len(user_comments))
    excel_exporter.export(user_names, user_comments)


    driver.close()

if __name__ == '__main__':
    main()