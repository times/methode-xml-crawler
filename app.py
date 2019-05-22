import requests
import sys
import os
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get(sys.argv[1]).text, features="html.parser")

i = 0
path = os.mkdir(sys.argv[1].split("/")[-1])
os.mkdirs(path)
while soup.find_all('link'):
    i = i + 1
    path = 
    print("Level ", i)
    if i == 1:
        break
    for link in soup.find_all('link'):
        os.mkdir(sys.argv[1].split("/")[-1])
        print("New link")
        # print(link.parent)
        # print(link.get('href'))
        link.name = 'lnk'
        linkcontent = BeautifulSoup(requests.get(link.get('href')).text, features="html.parser")
        link.insert(0, linkcontent)

print("Writing")
f = open(sys.argv[1].split("/")[-1] + ".xml", "w+")
f.write(soup.prettify())
f.close()
print("Done")