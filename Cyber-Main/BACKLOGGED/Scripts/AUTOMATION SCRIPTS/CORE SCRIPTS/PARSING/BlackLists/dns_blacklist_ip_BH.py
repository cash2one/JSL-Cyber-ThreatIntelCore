import requests
import pandas as pd

r = requests.get("http://www.openbl.org/lists/base_all.txt")

data = r.text.split("\n")

df = pd.DataFrame(data[4:], columns=['ips']).to_csv("dns_blacklist_ip.csv")