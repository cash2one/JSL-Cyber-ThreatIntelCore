'''
    Multi-threaded Script does reverse domain name resolution
    Usage :
            python reverse.py input.txt
'''
import csv
import dns
import dns.resolver
import itertools
import collections
import multiprocessing.pool
import urllib3
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from multiprocessing import Pool
import socket
import re
socket.setdefaulttimeout(5)
REQUESTED_FIELDS = ['A', 'AAAA', 'PTR', 'CNAME', 'MX', 'NS', 'TXT', 'SOA']

resolver = dns.resolver.Resolver()
resolver.timeout = 1
#resolver.lifetime = 1

pat = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
IPS = []

DATA = []

def dictToCSV(dict, fname):
    temp = []

    for elmt in dict:
        if elmt is not None:
            temp.append(elmt)
    dict = temp
    keys = set().union(*(d.keys() for d in dict))
    #for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname+'.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dict)
    return
        #print dict





def isIP(entry):
    test = re.findall(pat, entry)
    if test:
        return True
    else:
        return False


def worker(arg):
    """query dns for (hostname, qname) and return (qname, [rdata,...])"""
    try:
        url, qname = arg

        rdatalist = [rdata for rdata in resolver.query(url, qname)]
        return qname, rdatalist
    except dns.exception.DNSException, e:
        return qname, []


def resolve_dns(url_list):
    """
    Given a list of hosts, return dict that maps qname to
    returned rdata records.
    """
    response_dict = collections.defaultdict(list)
    # create pool for queries but cap max number of threads
    pool = multiprocessing.pool.ThreadPool(processes=min(len(url_list)*3, 60))
    for qname, rdatalist in pool.imap(
            worker,
            itertools.product(url_list, ('A', 'AAA', 'PTR', 'CNAME', 'MX', 'NS', 'TXT', 'SOA')),
            chunksize=1):
        response_dict[qname].extend(rdatalist)
    pool.close()
    #print response_dict
    return response_dict


def dns_lookup(ip):

    ip = ip.strip()
    entry = {}
    try:

        if isIP(ip):
            entry['ip_address'] = ip
            entry['domain'] = ''
            ais = socket.gethostbyaddr(ip)

            #print ip, ais[0]
            entry['domain'] = ais[0]
        else :
            domain = ip
            if 'www.' in domain:
                domain = domain[4:]

            entry['domain'] = domain
            entry['ip_address'] = ''
            ais = socket.gethostbyname(ip)


            entry['ip_address'] = ais
            #print ip, ais

        http = urllib3.PoolManager()
        doc = http.request('GET', 'http://pro.ip-api.com/json/%s?key=Z9P32o57C0f7fye' % entry['ip_address']).data
        data = json.loads(doc)

        Status = data['status']

        entry['ip_address'] = ip
        if Status == 'success' :

            entry['country_code'] = data['countryCode']
            entry['asn_number'] = data['as']


        if entry['domain'] is not '':

            url = entry['domain']
            for field in REQUESTED_FIELDS:
                try:
                    qname = field
                    entry[qname] = ""
                    rdatalist = [rdata for rdata in resolver.query(url, qname)]
                    for rdata in set(rdatalist):
                        #print rdata
                        entry[qname] += str(rdata)+'_'
                    if len(entry[qname]) > 1:
                        entry[qname] = entry[qname][:-1]
                #except dns.exception.DNSException, e:
                    #print qname, []
                except:
                    continue
        #print entry
    except:
        import traceback
        #traceback.print_exc()
        #print entry
        pass
    if entry is not None:
        DATA.append(entry)
    print entry['ip_address'], 'handled '
    return entry

def main():
    import sys
    if len(sys.argv)  < 3:
        print """

        Usage :
            python zoneField.py inputFile outputFile

        """
        return
    filename = sys.argv[1]


    with open(filename, 'r') as f:
        IPS = f.readlines()

    p = Pool(8)
    DATA = p.map(dns_lookup, IPS)

    dictToCSV(DATA, sys.argv[2])




if __name__ == '__main__':

    main()
