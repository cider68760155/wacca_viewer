from selenium import webdriver
from bs4 import BeautifulSoup
import json

import chromedriver_binary

DIFFICULTY = ['NORMAL', 'HARD', 'EXPERT', 'INFERNO']

try:
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(options=option)
    driver.get('https://wacca.marv.jp/music/')
    num_new = len(driver.find_elements_by_class_name('song'))
    driver.find_element_by_xpath('//a[@data-s="all"]').click()
    while num_new == len(driver.find_elements_by_class_name('song')):
        pass
    num_song = len(driver.find_elements_by_class_name('song'))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    category = [a.text for a in soup.find_all(class_='data_cat')]
    title = [a.text for a in soup.find_all(class_='data_name')]
    level = [[a.text.replace(' ', '').replace('+', '.5') for a in levels.find_all(
        class_='level_value')] for levels in soup.find_all(class_='level_list')]
    ret = [{} for i in range(num_song)]
    for i in range(num_song):
        ret[i]['title'] = title[i]
        ret[i]['category'] = category[i]
        for j, lv in enumerate(level[i]):
            ret[i]['level_' + DIFFICULTY[j]] = float(lv)
    print(ret)
    with open('./docs/data/songs.json', 'w') as f:
        json.dump(ret, f, ensure_ascii=False)
finally:
    driver.quit()
