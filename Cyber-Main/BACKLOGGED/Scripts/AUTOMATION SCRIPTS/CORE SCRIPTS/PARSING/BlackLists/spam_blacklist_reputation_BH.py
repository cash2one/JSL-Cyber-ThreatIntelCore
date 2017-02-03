import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

user_agent = {'User-agent': 'Mozilla/5.0'}

r = requests.get("http://reputation-email.com/reputation/rep_worst.htm", headers=user_agent)

soup = bs(r.text)
div = soup.find("div", class_="L1C1_column_content")
ips = []
for row in div.findAll("a"):
	ips.append(row.text)

df = pd.DataFrame(ips, columns=['IP_Address']).to_csv("spam_blacklist_rep_email.csv")