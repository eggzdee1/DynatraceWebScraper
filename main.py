from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

url = "https://community.dynatrace.com"

options = Options()
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(1)
for i in range(30):
    driver.find_element(By.ID, "custom-loader-button").click()
    time.sleep(0.2)
homeSource = driver.page_source


homeSoup = BeautifulSoup(homeSource, 'lxml')

posts = homeSoup.find_all("div", class_ = "custom-message-header")
links = []
for post in posts:
	links.append(post.find("a")["href"])


questions = []
allResponses = []
for link in links:
	postLink = url + link
	driver.get(postLink)
	time.sleep(0.5)
	postSource = driver.page_source
	postSoup = BeautifulSoup(postSource, 'lxml')

	comments = postSoup.find_all("div", class_ = "lia-message-body-content")
	if len(comments) < 2: continue

	question = "".join(comments[0].findAll(string=True))
	responses = []
	for i in range(1, len(comments)):
		responses.append("".join(comments[i].findAll(string=True)))
	questions.append(question)
	allResponses.append(responses)

outQuestions = open("Questions.txt", "w", encoding='utf-8')
#outResponses = open("Responses.txt", "w", encoding='utf-8')
for i in range(len(questions)):
	outQuestions.write(str(i + 1) + ":\n" + questions[i] + "\n----------------\n")
	for j in range(len(allResponses[i])):
		outQuestions.write(str(i + 1) + "." + str(j + 1) + ":\n" + allResponses[i][j] + "\n----------------\n")
outQuestions.close()
#outResponses.close()

print(len(questions))


driver.quit()