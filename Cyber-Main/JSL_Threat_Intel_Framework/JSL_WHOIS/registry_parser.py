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

    # Create table
    """
    c.execute('''CREATE TABLE country_asn
        (asn int, country_abbrv txt, country text)''')

    c.execute('''CREATE TABLE country_ipv4
                 (ip text, mask int, country_abbrv txt, first_date text)''')
    c.execute("INSERT INTO whois_db ( VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # Insert a row of data
    """

    registry_file = open(filename, 'r')

    dump = registry_file.readlines()

    for line in dump:
        if line.startswith("#"):
            print "skip"

        elif 'asn' in line.split('|')[2] and '*' not in line.split('|')[1]:

            #print 'ASN'
            try:
                country = pycountry.countries.get(alpha2=line.split('|')[1])
                name = country.name.replace("'", "")
            except:
                print line
                name = ""
            c.execute("INSERT INTO country_asn VALUES ('%d', '%s', '%s')" % (
            int(line.split('|')[3]), line.split('|')[1], name))
        elif 'ipv4' in line.split('|')[2] and '*' not in line.split('|')[1]:
            hosts_n = int(line.split('|')[4])
            mask = int(32 - math.log(hosts_n, 2))
            c.execute("INSERT INTO country_ipv4 VALUES ('%s/%d', '%s', '%s')" % (
                line.split('|')[3], mask, line.split('|')[1], line.split('|')[5]))

            #print 'IPV4'
        else:
            print line.split('|')[2]

    conn.commit()
    conn.close()


for url in SOURCE_URLS:
    pull_from_ftp(url)
    parse_registry(url[3])


def get_whois(ip, cur):
    cur.execute(
        "SELECT * FROM country_ipv4, country_asn WHERE country_ipv4.net_block >> '%s' AND country_ipv4.country_abbrv = country_asn.country_abbrv" % ip.strip())
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
            print ip.strip()
        else:
            whois_data.append([output[2], ip, output[0], output[4], output[3]])

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

# run_whois("ips")
