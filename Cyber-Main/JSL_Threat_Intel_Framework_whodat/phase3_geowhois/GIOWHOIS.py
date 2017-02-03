import collections
import csv
import os
import sys
import psycopg2
import gio
import pycountry


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


def main_geowhois(filename, offenderClass, iteration, date):
    if len(sys.argv) < 3:
        print "python GIO+WHOIS.py filename offenderClass"
        # return

    os.system("cut --complement -d, -f 1 %s > %s" % (filename, filename + '.domains'))
    os.system("cut --complement -d, -f 2 %s > %s" % (filename, filename + '.ips'))

    ###############################

    def get_whois(ip, cur):
        results = []
        cur.execute(
            "select ip_asn.ip, ip_asn.asn from  ip_asn where ip_asn.ip >> '%s' " % (
                ip.strip()))
        one = cur.fetchone()
        if one is None:
            results += ['', '']
        else:
            results += one
        cur.execute(
            "select  country_ipv4.country_abbrv, country_ipv4.first_date from   country_ipv4 where  country_ipv4.ip >> '%s'" % (
                ip.strip()))

        one = cur.fetchone()
        if one is None:
            results += ['', '']
        else:
            results += one
        return results

    def run_whois(ips_filename):
        conn = psycopg2.connect \
            ("dbname='whois_db' user='postgres' host='localhost' password='crawler123'")
        c = conn.cursor()
        ips = open(ips_filename).readlines()
        unresolved = []
        whois_data = []
        for ip in ips:
            output = get_whois(ip, c)

            if output is None:
                unresolved.append(ip.strip())
                whois_data.append(['', ip, '', '', '', ])
                print ip.strip()
            else:
                whois_data.append([output[3], ip, output[0], output[2], output[1], ])

        return whois_data

    whois_output = run_whois(filename + ".ips")

    ######################################
    gio.main_1(whois_output, filename, offenderClass, iteration, date)
    files = [filename + '.whois', filename + '.ips', filename + '.whois.tmp', filename + '.domains',
             filename + '.whois.shrunk',
             filename + '.whois.shrunk.spaceless', filename + '.whois.shrunk.clean', 'output*', '*list']
    for fn in files:
        os.system("rm %s" % fn)
        # os.system("python gio.py %s %s %s" % (filename, filename+'.gio', offenderClass))

        # getstuff("1", "2")


if __name__ == '__main__':
    main()
