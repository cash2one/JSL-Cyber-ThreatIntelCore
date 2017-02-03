import pandas as pd

df = pd.read_csv("http://dns-bh.sagadc.org/20160219.txt", sep='\t', error_bad_lines=False, header=None)

df.iloc[:, 2].to_csv("phishing_domains_dns_bh.csv")