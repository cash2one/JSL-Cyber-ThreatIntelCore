import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

""" 
    This webpage has a 100 row table that updates continuously,
    so this scraper should be run frequently.
"""

r = requests.get("http://dnsbl.inps.de/analyse.cgi?lang=en&action=show_changes")
content = bs(r.text).find("div", {"id": "content"})

data = {}
data['timestamp'] = []
data['ips'] = []
data['description'] = []

for row in content.table.findAll('tr')[1 :]:
    data['timestamp'].append(row.findAll('td')[1].text)
    data['ips'].append(row.findAll('td')[2].text)
    data['description'].append(row.findAll('td')[3].text)
df = pd.DataFrame(data).to_csv("spam_inps_de_blacklist.csv")
