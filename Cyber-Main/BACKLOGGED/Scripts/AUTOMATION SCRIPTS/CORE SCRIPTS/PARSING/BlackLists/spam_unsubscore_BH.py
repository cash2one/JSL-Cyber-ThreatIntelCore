import requests
import pandas as pd

r = requests.get("http://www.unsubscore.com/blacklist.txt")
ips = r.text.split("\n")
df = pd.DataFrame(ips, columns=['IP_Address']).to_csv("spam_usubscore.csv")