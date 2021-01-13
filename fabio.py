import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

pattern = '.*\/.*\/(.*)'


"""with open("file.txt","w") as f:
    data = pd.read_excel(r'url_kickstarter.xlsx', engine='openpyxl', usecols = "B")
    for url in list(data["url"]):
        f.write(url)
        sauce= urllib.request.urlopen(url).read()
        soup= bs.BeautifulSoup(sauce,'html')
        for p in soup.find_all('p'):"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

pattern = '.*\/.*\/(.*)'


"""with open("file.txt","w") as f:
    data = pd.read_excel(r'url_kickstarter.xlsx', engine='openpyxl', usecols = "B")
    for url in list(data["url"]):
        f.write(url)
        sauce= urllib.request.urlopen(url).read()
        soup= bs.BeautifulSoup(sauce,'html')
        for p in soup.find_all('p'):"""

with open("file.txt","w",encoding="utf-8") as f:
    s = requests.Session()
    data = pd.read_excel(r'url_kickstarter.xlsx', engine='openpyxl', usecols="B")
    for url in list(data["url"]):
        result = re.match(pattern, url).group(1)
        f.write(url)
        f.write("\n\n\n")
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        xcsrf = soup.find("meta", {"name": "csrf-token"})["content"]

        query = """
        query Campaign($slug: String!) {
          project(slug: $slug) {
            risks
            story(assetWidth: 680)
          }
        }"""

        r = s.post("https://www.kickstarter.com/graph",
            headers= {
                "x-csrf-token": xcsrf
            },
            json = {
                "query": query,
                "variables": {
                    "slug": result
                }
            })
        f.write("Story \n\n")
        f.write(r.json()["data"]["project"]["story"] + "\n\n")
        f.write("risks \n\n")
        f.write(r.json()["data"]["project"]["risks"] + "\n\n")