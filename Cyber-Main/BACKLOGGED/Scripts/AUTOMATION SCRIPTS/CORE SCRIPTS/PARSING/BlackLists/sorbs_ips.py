import BeautifulSoup as bs
import urllib3
URL = "http://www.sorbs.net/home/stats.shtml"


def sorbs_ips(url):
    '''

    :param url:
    :return A list of Lists (20x2) : IP Address, Rank :
    '''
    spamlist = []
    http = urllib3.PoolManager()
    doc = http.request('GET', url).data

    soup = bs.BeautifulSoup(doc)
    soup = soup.findAll('table')[6]


    for row in soup.findAll('tr'):

        aux = row.findAll('td')

        if len(aux) > 1 and aux[0].string is not None:
            spam = {}
            spam['ip_address'] = aux[1].string
            spam['Rank'] = aux[0].string
            spamlist.append(spam)

    return spamlist

def sorbs_domains(url):
    '''

    :param url:
    :return A list of lists (20x2) : Domain Name, Rank:
    '''
    spamlist = []
    http = urllib3.PoolManager()
    doc = http.request('GET', url).data

    soup = bs.BeautifulSoup(doc)
    soup = soup.findAll('table')[8]

    for row in soup.findAll('tr'):

        aux = row.findAll('td')

        if len(aux) > 1:
            spam = {}
            spam['ip_address'] = aux[1].string
            spam['rank'] = aux[0].string
            spamlist.append(spam)

    return spamlist[1:]
'''
spamlist = dnsbl_ips(URL)
for row in spamlist:
    print row

spamlist = dnsbl_domains(URL)
for row in spamlist:
    print row
'''
