import requests
from bs4 import BeautifulSoup
import csv

URL = "http://catalog.illinois.edu/courses-of-instruction/math/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())
