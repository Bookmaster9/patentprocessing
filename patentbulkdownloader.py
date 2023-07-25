from urllib import request
from bs4 import BeautifulSoup
import requests
import urllib.request
import requests, zipfile, io
import os

yearly_base_link = "https://bulkdata.uspto.gov/data/patent/officialgazette/20"
years = []
for i in range(22,1,-1):
    if i < 10:
        years.append(str(0)+str(i))
    else:
        years.append(str(i))
yearly_links = [yearly_base_link + i for i in years]

for link in yearly_links:
    year = link[-4:]
    print(year)
    page = requests.get(link)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    all_zips = soup.find_all("td", attrs = {"align": "left", "width": "20%"})
    for t in all_zips:
        print(str(t.text))
        print(str(t.text)[-3:])
        if str(t.text)[-3:] == "zip":
            r = requests.get("https://bulkdata.uspto.gov/data/patent/officialgazette/" + str(year) + "/" + str(t.text))
            z = zipfile.ZipFile(io.BytesIO(r.content))
            newpath = "/Users/lawrenceliu/Dropbox (MIT)/All Patent Data/" + str(year)
            if not os.path.exists(newpath):
                os.mkdir(newpath)
            z.extractall(newpath)
        print("done with " + str(t.text))
    print("done with" + year)
    
        
# print(soup.tr.find_next("tr").t)
# print(soup)

