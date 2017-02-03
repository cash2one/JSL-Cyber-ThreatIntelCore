import math
import pycountry
import psycopg2
import os
from ftplib import FTP

SOURCE_URLS = [
    ('ftp.arin.net', 'pub/stats/arin', 'delegated-arin-extended-latest', 'arin'),
    ('ftp.afrinic.net', 'stats/afrinic', 'delegated-afrinic-latest', 'afrinic'),
    ('ftp.ripe.net', 'pub/stats/ripencc', 'delegated-ripencc-latest', 'ripencc'),
    ('ftp.lacnic.net', 'pub/stats/lacnic', 'delegated-lacnic-latest', 'lacnic'),
    ('ftp.apnic.net', 'pub/stats/apnic', 'delegated-apnic-latest', 'apnic')
]


def pull_from_ftp(entry):
    ftp = FTP(entry[0])
    ftp.login()
    ftp.cwd(entry[1])
    ftp.retrbinary('RETR ' + entry[2], open(entry[3], 'wb').write)
    ftp.quit()


def list_to_file(data, filename):
    output_file = open(filename, 'w')
    output_file.write('begin\nverbose\n')

    for line in data:
        output_file.write(line + '\n')
    output_file.write("end\n")
    output_file.close()


def parse_registry(filename):
    # conn = sqlite3.connect('example.db')
    conn = psycopg2.connect \
        ("dbname='whois_db' user='postgres' host='localhost' password='crawler123'")

    c = conn.cursor()

    """
    c.execute('''CREATE TABLE country_ipv4
        (ip inet, country_abbrv text, first_date text, asn integer)''')
    # Create table

    c.execute('''CREATE TABLE country_asn
        (asn int, country_abbrv txt, country text)''')

    c.execute('''CREATE TABLE country_ipv4
                 (ip inet, country_abbrv text, first_date text, asn integer)''')
    c.execute("INSERT INTO whois_db ( VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # Insert a row of data
    """

    registry_file = open(filename, 'r')

    dump = registry_file.readlines()

    for line in dump:
        if line.startswith("#"):
            print "skip"

        elif 'ipv4' in line.split('|')[2] and '*' not in line.split('|')[1]:
            hosts_n = int(line.split('|')[4])
            mask = int(32 - math.log(hosts_n, 2))

            c.execute("INSERT INTO country_ipv4 VALUES ('%s/%d', '%s', '%s', 0)" % (
                line.split('|')[3], mask, line.split('|')[1], line.split('|')[5]))

        else:
            x = ""
            # print line.split('|')[2]

    conn.commit()
    conn.close()


# for url in SOURCE_URLS:
# pull_from_ftp(url)
#parse_registry(url[3])

file_dump = open("ips")
lines = file_dump.readlines()
asn = ""
bgp = ""
conn = psycopg2.connect \
    ("dbname='whois_db' user='postgres' host='localhost' password='crawler123'")

c = conn.cursor()
counter = 0
for line in lines:
    c.execute("select * from  ip_asn where ip_asn.ip >> '%s'" % line.strip())
    if c.fetchone() is None:
        counter += 1
        print line.strip()

    """
    if line.startswith(" ") and 'Local' not in asn:
        print asn, line.strip()
        c.execute("INSERT INTO ip_asn VALUES ('%s', '%d')"
                  % (line.strip(), int(asn)))

    else:
        asn = line.strip()
    """

conn.commit()
conn.close()


def get_whois(ip, cur):
    cur.execute(
        "SELECT * FROM country_ipv4, bgp_to_asn WHERE country_ipv4.net_block >> '%s' AND country_ipv4.country_abbrv = country_asn.country_abbrv" % ip.strip())
    return cur.fetchone()


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
        else:
            whois_data.append([output[2], ip.strip(), output[0], output[4], output[3], output[5]])

    return whois_data


# print run_whois("ipss")
"""
    list_to_file(unresolved, "unresolved")

    os.system("netcat v4.whois.cymru.com 43  < unresolved > unresolved.whois")
    os.system("sed -i 's/,/./g' unresolved.whois")
    os.system("sed -i 's/|/,/g' unresolved.whois")
    os.system("cut --complement -d, -f 5,7,8 unresolved.whois > unresolved")
    os.system(" sed  -i 's/ //g' unresolved")
    os.system(" tail unresolved -n +2 > unresolved.whois")
    os.system("rm unresolved")

    final_results = open("unresolved.whois", 'r')
    lines = final_results.readlines()

    for line in lines:
        line = line.strip()

        whois_data.append(line.split(','))
"""
# run_whois("ips")
