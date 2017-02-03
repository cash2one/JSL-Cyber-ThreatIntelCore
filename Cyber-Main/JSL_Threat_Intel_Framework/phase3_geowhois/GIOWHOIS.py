import collections
import csv
import os
import sys

import gio


def dictToCSV(dico, fname):
    keys = set().union(*(d.keys() for d in dico))
    # for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname + '.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dico)


def merge_two_dicts(x, y):
    try:
        del y['']
    except:
        xx = 0

    return dict(x.items() + y.items())


def getstuff(csv1, csv2):
    index = collections.defaultdict(list)

    file1 = open(csv1, "rb")
    rdr = csv.DictReader(file1)
    for row in rdr:
        # print row
        index[row['2']].append(row)
    file1.close()

    file2 = open(csv2, "rb")
    rdr = csv.DictReader(file2)
    counter = 0
    DATA = []
    for row in rdr:
        DATA.append(merge_two_dicts(row, index[row['2']][0]))
        counter += 1
    print counter
    file2.close()
    dictToCSV(DATA, "3")


def main_geowhois(filename, offenderClass, iteration, date, currentTime):
    if len(sys.argv) < 3:
        print "python GIO+WHOIS.py filename offenderClass"
        # return

    os.system("cut --complement -d, -f 1 %s > %s" % (filename, filename + '.domains'))
    os.system("cut --complement -d, -f 2 %s > %s" % (filename, filename + '.ips'))

    os.system("python phase3_geowhois/whois.py %s %s %s" % (filename, filename + '.whois', 1000))
    os.system('cut --complement -d, -f 1,4,5,7,8 %s > %s ' % (filename + '.whois', filename + '.whois.shrunk'))
    # os.system("sed -i -e '1i%s\' %s" % ('ipaddress,BGP,first_observed_date', filename+'.whois.shrunk'))

    # included_cols = ['BGP','ipaddress','fisu abdou
    # rst_observed_date']
    os.system("sed 's/ //g'  " + filename + ".whois.shrunk > " + filename + ".whois.shrunk.spaceless")
    os.system('cat ' + filename + '.whois.shrunk.spaceless | grep ^[0-9] > ' + filename + '.whois.shrunk.clean')
    with open(filename + '.whois.shrunk.clean') as filein:
        reader = csv.reader(filein)
        print reader
        ipaddress, BGP, first_observed_date = zip(*reader)

    gio.main_1(BGP, first_observed_date, filename, offenderClass, iteration, date, currentTime)
    files = [filename + '.whois', filename + '.ips', filename + '.whois.tmp', filename + '.domains',
             filename + '.whois.shrunk',
             filename + '.whois.shrunk.spaceless', filename + '.whois.shrunk.clean', 'output*', '*list']
    for fn in files:
        os.system("rm %s" % fn)
        # os.system("python gio.py %s %s %s" % (filename, filename+'.gio', offenderClass))

        # getstuff("1", "2")


if __name__ == '__main__':
    main()
