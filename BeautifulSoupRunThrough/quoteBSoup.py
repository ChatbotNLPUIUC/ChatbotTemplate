#Python program to scrape website
#and save quotes from website
import requests
from bs4 import BeautifulSoup
import csv

def parse_web(URL, csv_name):
    URL = URL
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    courses=[] # a list to store quotes

    table = soup.find('div', attrs = {'id':'courseinventorycontainer'})

    for row in table.findAll('div', attrs = {'class':'courseblock'}):
        course = {}
    	#quote['theme'] = row.h5.text
        course['url'] = row.a['href']
        course['name'] = row.a.getText()
        temp = row.find('p', attrs = {'class':'courseblockdesc'})
        course['description'] = temp.getText()
        courses.append(course)
        #print(row)


    #'theme','url','img','lines','author'

    filename = csv_name

    with open(filename, 'w', newline='') as f:
    	w = csv.DictWriter(f,['url', 'name', 'description'])
    	w.writeheader()
    	for course in courses:
    		w.writerow(course)

if __name__ == "__main__":
    parse_web("http://catalog.illinois.edu/courses-of-instruction/me/", 'uiuc_me.csv')
