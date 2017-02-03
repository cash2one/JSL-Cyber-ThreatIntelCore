import urllib3

NEXT_CHECK = 1
DOMAIN = 2
TYPE = 3
REFERENCE = 4

URL = "http://www.unsubscore.com/blacklist.txt"

def unsubscore_ips(url):
    '''

    :param url:
    :return A list of IP Addresses:
    '''

    blacklist = []

    http = urllib3.PoolManager()
    doc = http.request('GET', url).data
    doc = doc.split('\n')
    for line in doc:
        line = line.replace('\r', '')
        if line is not '':
            blacklist.append({'ip_address': line})

    return blacklist
'''
blacklist = unsubscore_ips(URL)

for element in blacklist:
    print element
'''