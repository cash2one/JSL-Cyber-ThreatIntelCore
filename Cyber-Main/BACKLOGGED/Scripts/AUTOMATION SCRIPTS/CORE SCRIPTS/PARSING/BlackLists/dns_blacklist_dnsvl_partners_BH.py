import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

r = requests.get("http://www.dnsbl.manitu.net/partners.php?language=en")
soup = bs(r.text)
table = soup.find("table").findAll("td", {"colspan" : "2"})[1]
data = {}
data['type'] = []
data['dns_server'] = []
data['ip_address'] = []
data['provider'] = []

for row in table.findAll("tr")[1 :]:
    data['type'].append(row.findAll('td')[0].text.replace("\t", "").replace("\n", ""))
    data['dns_server'].append(row.findAll('td')[1].text.replace("\t", "").replace("\n", ""))
    data['ip_address'].append(row.findAll('td')[2].text.replace("\t", "").replace("\n", ""))
    data['provider'].append(row.findAll('td')[3].text.replace("\t", "").replace("\n", ""))

# The table in the dataframe is in the right format, but reading the CSV with
# Libre Office Spreadsheet reader is distorted because of the nested structure of some fields
# Print df.head() to print the first 5 rows of the dataframe to check the structure

df = pd.DataFrame(data).to_csv("dns_blacklist_dnsvl.csv", encoding='utf-8')
