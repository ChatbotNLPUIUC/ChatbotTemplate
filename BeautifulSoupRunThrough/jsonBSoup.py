#Python program to scrape website
#and save quotes from website
import requests
from bs4 import BeautifulSoup
import csv
import json

URL = "http://catalog.illinois.edu/courses-of-instruction/math/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

courses=[] # a list to store quotes

table = soup.find('div', attrs = {'id':'courseinventorycontainer'})

for row in table.findAll('div', attrs = {'class':'courseblock'}):
    course = {}
	#quote['theme'] = row.h5.text
    course['tag'] = row.a.getText().strip()
    temp = row.find('p', attrs = {'class':'courseblockdesc'})
    course['patterns'] = temp.getText().strip().split('.')
    course['responses'] = [row.a['href']]
    course['context'] = [""]
    courses.append(course)
    #print(row)

intent = {}
intent['intents'] = courses
#'theme','url','img','lines','author'

filename = 'test_math.json'
json_obj = json.dumps(intent, indent = 4)

with open(filename, 'w',) as outfile:
	outfile.write(json_obj)
