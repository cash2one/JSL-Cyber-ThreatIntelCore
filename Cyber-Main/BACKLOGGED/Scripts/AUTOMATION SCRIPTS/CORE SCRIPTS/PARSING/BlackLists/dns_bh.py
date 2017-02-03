import urllib3

URL ="http://dns-bh.sagadc.org/dynamic_dns.txt"


def dynamic_dns_bl(url):

    '''
        :param url:
        :return blacklist:
        A list of lists
        each entry has 2 values : blacklisted domain, reference
    '''

    blacklist = []
    http = urllib3.PoolManager()
    doc = http.request('GET', url).data
    doc = doc.split('\n')
    doc = doc[14:]
    for line in doc:
        fields = line.split('#from')
        if len(fields) == 1:
            fields = line.split('#')
            if len(fields) == 1:
                fields = line.split('from')
                if len(fields) == 1:
                    fields = line.split('malicious')
                    if len(fields) == 1:
                        fields = line.split('harmful')
                        if len(fields) == 1:
                            fields = line.split('redkit')
                            if len(fields) == 1:
                                fields = line.split('test')
                                if len(fields) == 1:
                                        fields = line.split('malvertising')
        if len(fields) > 1:
            fields[0] = fields[0].replace('\t', '')
            fields[1] = fields[1].replace('\r', '')
            fields[1] = fields[1].replace('\t', '')
            spam = {}
            spam['host_name'] = fields[0]
            spam['reference'] = fields[1]
            blacklist.append(spam)
    return blacklist
'''
print dynamic_dns_bl(URL)
'''
