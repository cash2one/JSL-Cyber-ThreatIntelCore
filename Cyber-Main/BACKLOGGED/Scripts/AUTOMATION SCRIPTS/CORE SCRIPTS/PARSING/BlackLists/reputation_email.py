import urllib3
import re

URL = "http://reputation-email.com/reputation/rep_worst.htm"

def reputation_email_ips(url):
    '''
    :param url:
    :return a List of IP addresses:
    '''

    http = urllib3.PoolManager()
    doc = http.request('GET', url).data
    bad_ips = re.findall('\d+\.\d+\.\d+\.\d+', doc)
    ips = []
    for bad_ip in bad_ips:
        ips.append({'ip_address':  bad_ip[:-1]})
    return ips
'''
print reputation_email_ips(URL)
'''
