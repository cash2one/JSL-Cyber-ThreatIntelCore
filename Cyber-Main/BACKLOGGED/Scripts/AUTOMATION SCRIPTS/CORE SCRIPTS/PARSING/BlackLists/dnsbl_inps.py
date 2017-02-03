import BeautifulSoup as bs
import urllib3
URL = "http://dnsbl.inps.de/analyse.cgi?lang=en&action=show_changes"


def dnsbl_ips(url):
    '''

    :param url:
    :return a Dictionary of lists with three keys : IP, timestamp, description:
    '''

    spamlist = []

    http = urllib3.PoolManager()
    doc = http.request('GET', url).data

    soup = bs.BeautifulSoup(doc)


    for row in soup.findAll('tr'):

        aux = row.findAll('td')

        if len(aux) > 0:
            print aux[1].string, aux[3].string, aux[2].find('a').string
            spam = {}
            spam['ip_address'] = aux[2].find('a').string
            spam['listing_timestamp'] = aux[1].string
            spam['description_text'] = aux[3].string

            spamlist.append(spam)

    return spamlist

'''
spamlist = dnsbl_ips(URL)
for ip, ts, info in zip(spamlist['ip'], spamlist['timestamp'], spamlist['info']):
    print ip, ts, info

'''