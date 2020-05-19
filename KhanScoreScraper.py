from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import gc
import csv

"""
By Daniela Hinojosa Sada
You need Python, Pip, and Selenium to be functioning on your computer
Python comes with Apple computers. Here are the instructions for Pip and Selenium:

Full Selenium Support: https://selenium-python.readthedocs.io/installation.html

1. SETUP
- Make sure this "KhanScoreScraper.py" file is on your Desktop
- Download this file to your Desktop: https://bootstrap.pypa.io/get-pip.py (control + click the page 
	and press "Save As")
- Download one of the following drivers (for the browser you will use). Remember where you put it.
		Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
		Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
		Firefox:	https://github.com/mozilla/geckodriver/releases
		Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/
- Open Finder
- Press Command + Shift + G and type "/usr/local/bin". Press "Go."
- Put the driver in the folder you are in
- Open up "terminal" (command + space)
- Type "cd Desktop" in the terminal and hit enter
- Type "python get-pip.py" in the terminal and hit enter
- Type "pip install selenium" in the terminal and hit enter

- Type "python KhanScoreScraper.py" in the terminal and hit enter
- Now you must wait until the program finishes running. Once it is done, 
	the pop up browser will close and you will have a csv file called
	"Khan Scores.csv" on your Desktop

* you may need to run the program one or two times to get it to run properly; sometimes
	it gets stuck when putting in the password at the start
*if you run this multiple times, make sure that the CSV file is CLOSED while
	the program is running. Otherwise, it won't update with the scores.
"""
#Delete one (1) hashtag below to select which browser you are using:

#driver = webdriver.Chrome()
#driver = webdriver.Safari()
#driver = webdriver.Firefox()

#** ONE MORE SETUP STEP BELOW


delay = 15

# 2. SETUP
# put your google and password here between the apostraphes
mail_address = ''
password = ''

#Put your Khan Academy class assignment scores link here
#E.g., "https://www.khanacademy.org/coach/class/414u1y8517471c/assignment-scores"
khanurl = 'https://www.khanacademy.org/coach/class/123455667234/assignment-scores'

#put one student's first and last name as it appears on Khan between the quotes.
#e.g., 'Marta Lopez'
studentname = ''

#you're ready to run the program now!

url = 'https://www.google.com/accounts/Login?hl=ja&continue=http://www.google.co.jp/'
driver.get(url)

# Finds login field
login_field = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.ID, 'identifierId')))
login_field.send_keys(mail_address)

# Clicks next button
driver.find_element_by_id('identifierNext').click()

# Finds password field
password_field = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.ID, 'password')))
password_field = password_field.find_element_by_tag_name('input')

ActionChains(driver).move_to_element(password_field).click(password_field).perform()
password_field.send_keys(password)

# Clicks next button
driver.find_element_by_id('passwordNext').click()


driver.get(khanurl)

#google login
button = driver.find_element_by_class_name('_1up6svzf')
ActionChains(driver).move_to_element(button).click(button).perform()

page_load = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, '_bfbtmj')))

#Student: (URL, ([assignment], [score]))
students = {}

#generate dictionary with name as key. URL and score dictionary are values.
elems = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div/div[3]/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[1]//a')
for elem in elems:
    students[elem.text] = (elem.get_attribute("href"), [], [])

#iterate thru students and go to url and collect scores
for student in students:

	driver.get(students[student][0])

	WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, '_j1kt73')))

	assignments = driver.find_elements_by_class_name("_j1kt73")
	for elem in assignments:
		if elem.text != "In progress" and elem.text != "Completed" and elem.text != "CompletedLATE" and elem.text != "Not completed":
			students[student][1].append(elem.text)
	scores = driver.find_elements_by_class_name("_36rlri")
	for elem in scores:
		if elem.text == "0":
			students[student][2].append(0)
		elif elem.text.isnumeric() and int(elem.text) > 24:
			students[student][2].append(elem.text)	

with open('Khan Scores.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	header = ["Name:"]
	for x in students[studentname][1]:
		header.append(x)
	writer.writerow(header)

	for student in students:
		new_row = []
		new_row.append(student)
		for x in students[student][2]:
			new_row.append(x)
		writer.writerow(new_row)	

gc.collect()
driver.close()
