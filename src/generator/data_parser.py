import requests
from bs4 import BeautifulSoup as bs

URL = "https://citaty.info/topic/vesna?page=22"

r = requests.get(URL)
soup = bs(r.text, "html.parser")
quotes = soup.find_all('div', class_='field-item even last')
for qoute in quotes:
    flag = False
    res = ""
    for i in str(qoute.contents[0]):
        if i == "<":
            flag = True
        elif i == ">":
            flag = False
        elif not flag:
            res += i
    fin = open("qoutes.txt", "a")
    fin.write("\n")
    fin.write(res)
    fin.close()
