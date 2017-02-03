import pandas as pd

df = pd.read_csv('http://dns-bh.sagadc.org/dynamic_dns.txt', sep='\t', skiprows=(0,1,2,3,4,5,6,7,8,9,10,11,12,13), error_bad_lines=False, header=None)
df.to_csv("dns_sagadc.csv")