import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

r = requests.get("http://cybercrime-tracker.net/fuckerz.php")

soup = bs(r.text)
table = soup.find('table', class_='ExploitTable')

ips = []
for row in table.findAll('tr')[1:]:
    ips.append(row.findAll('td')[1].find('a').text)
df = pd.DataFrame(ips, columns=['IP_Address']).to_csv("cybercrime_fucekrs_BH.csv", index=False)