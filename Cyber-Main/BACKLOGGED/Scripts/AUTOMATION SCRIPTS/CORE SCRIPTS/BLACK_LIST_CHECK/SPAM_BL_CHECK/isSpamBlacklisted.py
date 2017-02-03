import dns.resolver
import csv
import multiprocessing.pool

bls = ["cbl.abuseat.org", "bl.spamcop.net",
        "xbl.spamhaus.org", "pbl.spamhaus.org", "pbl.spamhaus1.org"]


output_data = []


resolver = dns.resolver.Resolver()
resolver.timeout = 1
#resolver.lifetime = 6



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


        p = multiprocessing.pool.Pool(16)
        output_data = p.map(function1, lines)

        '''
        for ip in lines:
            output_data.append(function1( ip))
        '''
    dictToCSV(output_data, output_filename)


def function1(ip_address):
    results = {}
    for bl in bls:
        try:
            ip_address = ip_address.replace('"', '').replace('\n', '').replace('\r', '')
            results["ip_address"] = ip_address.replace('"', '').replace('\n', '').replace('\r', '')
            #my_resolver = dns.resolver.Resolver()
            query = '.'.join(reversed(str(ip_address).split("."))) + "." + bl
            answers = resolver.query(query, "A")
            answer_txt = resolver.query(query, "TXT")
            results[bl] = True

            print 'IP: %s IS listed in %s (%s: %s)' % (ip_address, bl, answers[0], answer_txt[0])
        except dns.resolver.NXDOMAIN:
            results[bl] = False
            print 'IP: %s is NOT listed in %s' % (ip_address, bl)
        except dns.exception.Timeout:
            x=0
            print 'IP: %s is NOT listed in %s' % (ip_address, bl)
            #print "timeout"

    return results


if __name__ == '__main__':

    function0('blacklist.txt', 'out')

#print output_data