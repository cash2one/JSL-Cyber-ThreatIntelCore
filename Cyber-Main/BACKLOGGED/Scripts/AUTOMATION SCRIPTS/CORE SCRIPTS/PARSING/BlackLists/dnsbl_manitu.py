import urllib3
import BeautifulSoup as bs
import re

URL = "http://www.dnsbl.manitu.net/partners.php?language=en"



def dnsbl_manitu(url):
    '''

    :param url:
    :return A list of lists : IP, Date-Time :
    '''
    spamlist = []
    http = urllib3.PoolManager()
    doc = http.request('GET', url).data

    soup = bs.BeautifulSoup(doc)
    soup = soup.findAll('table')[2]


    for row in soup.findAll('tr'):

        aux = row.findAll('td')

        if len(aux) > 1 and aux[0].string is not None:


            spam = {}

            name = aux[3].find('span')
            name = name.next
            spam['company_name'] = name.replace('\t', '').replace('\n', '')
            urls = aux[3].findAll('a')
            for url in urls:
                if 'www' in url.string:
                    spam['website'] = url.string

            if len(aux[2].contents) > 1:
                #print aux[2]
                ip = aux[2].contents[0]
            else:
                ip = aux[2].string
            #print aux[0].string, aux[1].string, ip, aux[3]

            ip = ip.replace('\t', '')
            ip = ip.replace('\n', '')

            spam['ip_address'] = ip
            spam['blacklist_type_name '] = aux[0].string.replace('\t', '').replace('\n', '')
            spam['host_name'] = aux[1].string.replace('\t', '').replace('\n', '')
            spamlist.append(spam)

    return spamlist

#print dnsbl_manitu(URL)