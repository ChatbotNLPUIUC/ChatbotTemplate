#Python program to scrape website
#and save quotes from website
import requests
from bs4 import BeautifulSoup
import csv

URL = "http://catalog.illinois.edu/courses-of-instruction/math/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

courses=[] # a list to store quotes

table = soup.find('div', attrs = {'id':'courseinventorycontainer'})

for row in table.findAll('div', attrs = {'class':'courseblock'}):
    course = {}
	#quote['theme'] = row.h5.text
    course['url'] = row.a['href']
    course['name'] = row.a.getText()
    temp = table.find('p', attrs = {'class':'courseblockdesc'})
    course['description'] = temp.getText()
    courses.append(course)
    #print(row)


#'theme','url','img','lines','author'

filename = 'uiuc_math.csv'

with open(filename, 'w', newline='') as f:
	w = csv.DictWriter(f,['url', 'name', 'description'])
	w.writeheader()
	for course in courses:
		w.writerow(course)
