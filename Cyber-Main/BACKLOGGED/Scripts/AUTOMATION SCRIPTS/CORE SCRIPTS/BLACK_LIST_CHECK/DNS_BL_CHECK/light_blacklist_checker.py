import sqlite3

import popen
import os
import sys


bls = ["zen.spamhaus.org", "spam.abuse.ch", "cbl.abuseat.org", "virbl.dnsbl.bit.nl", "dnsbl.inps.de",
    "ix.dnsbl.manitu.net", "dnsbl.sorbs.net", "bl.spamcannibal.org", "bl.spamcop.net",
    "xbl.spamhaus.org", "pbl.spamhaus.org", "dnsbl-1.uceprotect.net", "dnsbl-2.uceprotect.net",
    "dnsbl-3.uceprotect.net", "db.wpbl.info"]


USAGE = ""
def main():

    if len(sys.argv) < 2:
        print USAGE
        return
    ip = sys.argv[1]
    A = os.popen("dig A %s +short " % ip).read()
    TXT = os.popen("dig TXT %s +short " % ip).read()


    for bl in bls:
        try:
            ip_address = ip_address.replace('"', '').replace('\n', '').replace('\r', '')
            print bl, ip_address
            results["ip_address"] = ip_address
            my_resolver = dns.resolver.Resolver()

            query = '.'.join(reversed(str(ip_address).split("."))) + "." + bl
            print query
            #print query
            #print "AAAAAAAAAAa"
            answers = my_resolver.query(query, "A")
            #print "BBBBBBBBBBBB"
            answer_txt = my_resolver.query(query, "TXT")
            #print "CCCCCCCCCCCCc"
            print True
            results[bl] = True
            #print 'IP: %s IS listed in %s (%s: %s)' %(myIP, bl, answers[0], answer_txt[0])
        except :
            results[bl] = False
            print False
            #print 'IP: %s is NOT listed in %s' %(myIP, bl)

    return results



if __name__ == '__main__':
    main()