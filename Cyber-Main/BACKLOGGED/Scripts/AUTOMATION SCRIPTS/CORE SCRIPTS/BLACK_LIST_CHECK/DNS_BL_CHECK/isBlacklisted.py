#utf-8

import csv
import dns
import dns.resolver
import itertools
import collections
import multiprocessing.pool
import urllib3
import json

bls = ["zen.spamhaus.org", "spam.abuse.ch", "cbl.abuseat.org", "virbl.dnsbl.bit.nl", "dnsbl.inps.de",
    "ix.dnsbl.manitu.net", "dnsbl.sorbs.net", "bl.spamcannibal.org", "bl.spamcop.net",
    "xbl.spamhaus.org", "pbl.spamhaus.org", "dnsbl-1.uceprotect.net", "dnsbl-2.uceprotect.net",
    "dnsbl-3.uceprotect.net", "db.wpbl.info"]

output_data = []

resolver = dns.resolver.Resolver()
resolver.timeout = 1
#resolver.lifetime = 1




def dictToCSV(dico, fname):
    keys = set().union(*(d.keys() for d in dico))
    #for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname+'.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dico)
        print dico


def function0(input_filename, output_filename):
    with open(input_filename) as in_file:

        lines = in_file.readlines()

        p = multiprocessing.pool.Pool(16)
        output_data = p.map(function1, lines)
        '''
        for ip in lines:
            output_data.append(function1(ip))
        '''
    dictToCSV(output_data, output_filename)



def function1(ip_address):
    results = {}



    for bl in bls:
        try:
            ip_address = ip_address.replace('"', '').replace('\n', '').replace('\r', '')
            #print bl, ip_address
            results["ip_address"] = ip_address
            #my_resolver = dns.resolver.Resolver()

            query = '.'.join(reversed(str(ip_address).split("."))) + "." + bl
            #print query
            ##print query
            #print "AAAAAAAAAAa"
            answers = resolver.query(query, "A")
            #print "BBBBBBBBBBBB"
            answer_txt = resolver.query(query, "TXT")
            #print "CCCCCCCCCCCCc"
            #print True
            results[bl] = True
            print 'IP: %s IS listed in %s (%s: %s)' %(results["ip_address"], bl, answers[0], answer_txt[0])
        except dns.resolver.NXDOMAIN:
            results[bl] = False
            #print False
            print 'IP: %s is NOT listed in %s' %(results["ip_address"], bl)

        except dns.exception.Timeout:
            results[bl] = False
            x=0
            print 'IP: %s is NOT listed in %s' %(results["ip_address"], bl)
            #print "timeout"

    return results


if __name__ == '__main__':
    import time

    start = time.time()
    function0('ips.txt', 'out.txt')
    print  time.time() - start

#print output_data