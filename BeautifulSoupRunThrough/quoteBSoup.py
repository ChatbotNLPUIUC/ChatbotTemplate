#Python program to scrape website
#and save quotes from website
import requests
from bs4 import BeautifulSoup
import csv

URL = "http://catalog.illinois.edu/courses-of-instruction/math/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

quotes=[] # a list to store quotes

table = soup.find('div', attrs = {'id':'courseinventorycontainer'})

for row in table.findAll('div',
						attrs = {'class':'courseblock'}):
	#quote = {}
	#quote['theme'] = row.h5.text
	#quote['url'] = row.a['href']
	#quote['img'] = row.img['src']
	#quote['lines'] = row.img['alt'].split(" #")[0]
	#quote['author'] = row.img['alt'].split(" #")[1]
	#quotes.append(quote)
    print(row.a['href'])

#filename = 'inspirational_quotes.csv'
#with open(filename, 'w', newline='') as f:
	#w = csv.DictWriter(f,['theme','url','img','lines','author'])
	#w.writeheader()
	#for quote in quotes:
		#w.writerow(quote)
