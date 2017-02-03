#utf-8
import dns.resolver
import csv

bls = ["zen.spamhaus.org", "spam.abuse.ch", "cbl.abuseat.org", "virbl.dnsbl.bit.nl", "dnsbl.inps.de",
    "ix.dnsbl.manitu.net", "dnsbl.sorbs.net", "bl.spamcannibal.org", "bl.spamcop.net",
    "xbl.spamhaus.org", "pbl.spamhaus.org", "dnsbl-1.uceprotect.net", "dnsbl-2.uceprotect.net",
    "dnsbl-3.uceprotect.net", "db.wpbl.info"]

output_data = []


def dictToCSV(dict, fname):
    keys = set().union(*(d.keys() for d in dict))
    #for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname+'.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dict)
        print dict


def function0(input_filename, output_filename):
    with open(input_filename) as in_file:
        lines = in_file.readlines()
        for ip in lines:
            output_data.append(function1(ip))

    dictToCSV(output_data, output_filename)



def function1(ip_address):
    results = {}
    for bl in bls:
        try:
            ip_address = ip_address.replace('"', '').replace('\n', '').replace('\r', '')
            #print bl, ip_address
            results["ip_address"] = ip_address
            my_resolver = dns.resolver.Resolver()
            
            query = '.'.join(reversed(str(ip_address).split("."))) + "." + bl
            print "Query: ", query
            #print "AAAAAAAAAAa"
            answers = my_resolver.query(query, "A")
            #print "BBBBBBBBBBBB"
            answer_txt = my_resolver.query(query, "TXT")
            #print "CCCCCCCCCCCCc"
            #print True
            results[bl] = True
            print 'IP: %s IS listed in %s (%s: %s)' %(ip_address, bl, answers[0], answer_txt[0])
        except :
            results[bl] = False
            print 'IP: %s is NOT listed in %s' %(ip_address, bl)

    return results


function0('ips.txt', 'out_revised')

print output_data
