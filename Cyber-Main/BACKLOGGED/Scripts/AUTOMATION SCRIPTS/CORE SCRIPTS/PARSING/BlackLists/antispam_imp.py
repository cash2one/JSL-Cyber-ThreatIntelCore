import urllib3
import datetime


URL = "http://antispam.imp.ch/spamlist"

def anti_spam_imp_ips(url):
    '''
    :param url:
    :return spamlist:
     A dictionary of lists with four keys : IP, unixtime, localtime, hits
    '''

    spamlist = []

    http = urllib3.PoolManager()
    doc = http.request('GET', url).data
    doc = doc.split('\n')
    doc = doc[8:-1]
    for line in doc:
        fields = line.split('\t')
        spam = {}
        spam['ip_address'] = fields[1]
        spam['listing_timestamp'] =  datetime.datetime.fromtimestamp(
                                int(fields[2][:-1])
                                ).strftime('%Y-%m-%d %H:%M:%S')
        #spam['listingDate'] = fields[3]
        #spam['hits'] = fields[4][fields[4].index("(") + 1:fields[4].rindex(")")]
        spam['host_name'] = fields[4].split(')')[1]
        spam['host_name'] = spam['host_name'][:-1].replace(' ', '')
        spamlist.append(spam)

    #bad_ips = re.findall('\d+\.\d+\.\d+\.\d+', doc)

    #for i in range(len(doc)):
    #    doc[i] = doc[i][:-1]
    return spamlist

#spamlist = anti_spam_imp_ips(URL)
#print spamlist

