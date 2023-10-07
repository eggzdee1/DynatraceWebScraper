#First you need to download chromedriver (search it up) and put it into your Windows folder
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

url = "https://community.dynatrace.com"

#Open a Chrome window, scroll down a bunch, pull the HTML, and exit
options = Options()
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(2)
'''for i in range(30):
    driver.find_element(By.ID, "custom-loader-button").click()
    time.sleep(0.2)'''
page = driver.page_source


soup = BeautifulSoup(page, 'lxml')

posts = soup.find_all("div", class_ = "custom-message-header")
links = []
for post in posts:
    links.append(post.find("a")["href"])


for link in links:
    postLink = url + link
    driver.get(postLink)


driver.quit()