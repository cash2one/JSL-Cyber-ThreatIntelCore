import collections
import csv
import os
import sys

import gio


def dictToCSV(dico, fname):
    keys = set().union(*(d.keys() for d in dico))
    #for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname+'.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dico)
        #print dico


def merge_two_dicts(x, y):

    #z = x.copy()
    #z.update(y)
    try:
        del y['']
    except:
        xx=0
    #print str(len(y)) + "barrk"
    #print str(len(y)) + "bark"
    a = x.items()
    a = y.items()
    return dict(x.items() + y.items())


def getstuff(csv1, csv2):

    index = collections.defaultdict(list)

    file1=open(csv1, "rb")
    rdr= csv.DictReader(file1)
    for row in rdr:
        #print row
        index[row['2']].append(row)
    file1.close()

    file2= open(csv2, "rb")
    rdr= csv.DictReader(file2)
    counter = 0
    DATA = []
    for row in rdr:
        #print counter
        #print row, index[row['IP_Address']]
        #print index[row['IP_Address']]
        #print 'a'
        #print row
        #print index[row['enr_query']]
        #print row['enr_query']
        #print row
        DATA.append(merge_two_dicts(row, index[row['2']][0]))
        counter += 1
    print counter
    file2.close()
    dictToCSV(DATA, "3")


def main():

    if len(sys.argv) < 3:
        print "python GIO+WHOIS.py iplist offenderClass"
        return
    iplist = sys.argv[1]
    offenderClass = sys.argv[2]

    os.system("cut --complement -d, -f 1 %s > %s" % (iplist, iplist+'.domains'))
    os.system("cut --complement -d, -f 2 %s > %s" % (iplist, iplist+'.ips'))

    os.system("python whois.py %s %s %s" % (iplist, iplist+'.whois', 1000))
    os.system('cut --complement -d, -f 1,4,5,7,8 %s > %s ' % (iplist+'.whois',iplist+'.whois.shrunk') )
    #os.system("sed -i -e '1i%s\' %s" % ('ipaddress,BGP,first_observed_date', iplist+'.whois.shrunk'))


    #included_cols = ['BGP','ipaddress','fisu abdou
    # rst_observed_date']
    os.system("sed 's/ //g'  "+iplist+".whois.shrunk > "+iplist+".whois.shrunk.spaceless")
    os.system('cat '+iplist+'.whois.shrunk.spaceless | grep ^[0-9] > ' + iplist+'.whois.shrunk.clean')
    with open(iplist+'.whois.shrunk.clean') as filein:
        reader = csv.reader(filein)
	print reader
        ipaddress,BGP,first_observed_date = zip(*reader)




    gio.main_1(BGP, first_observed_date, iplist, offenderClass)
    files = [iplist+'.whois', iplist+'.ips', iplist+'.whois.tmp', iplist+'.domains', iplist+'.whois.shrunk',iplist+'.whois.shrunk.spaceless',iplist+'.whois.shrunk.clean', 'output*']
    for fn in files:
        os.system("rm %s" % fn)
    #os.system("python gio.py %s %s %s" % (iplist, iplist+'.gio', offenderClass))

    #getstuff("1", "2")

if __name__ == '__main__':
    main()
