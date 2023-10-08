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
time.sleep(1)
'''for i in range(30):
    driver.find_element(By.ID, "custom-loader-button").click()
    time.sleep(0.2)'''
homeSource = driver.page_source


homeSoup = BeautifulSoup(homeSource, 'lxml')

posts = homeSoup.find_all("div", class_ = "custom-message-header")
links = []
for post in posts:
	links.append(post.find("a")["href"])


questions = []
topResponses = []
for link in links:
	postLink = url + link
	driver.get(postLink)
	time.sleep(0.5)
	postSource = driver.page_source
	postSoup = BeautifulSoup(postSource, 'lxml')

	comments = postSoup.find_all("div", class_ = "lia-message-body-content")
	if len(comments) < 2: continue

	'''questionRaw = comments[0].find_all()
	#print(questionRaw)
	questionText = ""
	for paragraph in questionRaw:
		questionText += "".join(paragraph.findAll(string = True)) + "\n"'''
	#questionRaw = comments[0].find_all(["p", "pre"])
	#responseRaw = comments[1].find_all(["p", "pre"])
	#question = ""
	#response = ""
	#for paragraph in questionRaw:
	question = "".join(comments[0].findAll(string=True))
	#for paragraph in responseRaw:
	response = "".join(comments[1].findAll(string=True))
	questions.append(question)
	topResponses.append(response)

outQuestions = open("Questions.txt", "w", encoding='utf-8')
outResponses = open("Responses.txt", "w", encoding='utf-8')
for i in range(len(questions)):
	outQuestions.write(questions[i] + "\n----------------\n")
	outResponses.write(topResponses[i] + "\n----------------\n")
outQuestions.close()
outResponses.close()


driver.quit()