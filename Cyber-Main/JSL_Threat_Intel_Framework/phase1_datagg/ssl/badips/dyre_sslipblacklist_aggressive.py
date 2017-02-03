import urllib3
import re
import os
import gzip
from cStringIO import StringIO
import subprocess


def ipsFromgzWget(url):
    length = len(url.split('/'))
    filename = url.split('/')[length - 1]
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(['wget', '%s' % url], stdout=devnull, stderr=subprocess.STDOUT)
    # os.system("wget %s" % url)
    gzipped = open(filename)
    results = gzip.GzipFile(fileobj=StringIO(gzipped.read()))
    ips = re.findall(IPV4_REGEX, results.read())
    os.remove(filename)
    return ips


IPV4_REGEX = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
url = 'https://sslbl.abuse.ch/blacklist/dyre_sslipblacklist_aggressive.csv'


def do_fetch():
    ips = []
    email_report = ''

    print "pulling from %s " % url
    try:
        if 'wget' in url:
            items = ipsFromgzWget(url)
        else:

            http = urllib3.PoolManager(10, headers=user_agent)

            r = http.request('GET', url)
            dump = r.data
            items = re.findall(IPV4_REGEX, dump)

        ips += items
        print "%s ips pulled from %s" % (len(items), url)
        # aggregationreport.add_pull('ips', url, len(items))


        results = open('../output_ips', 'a')
        [results.write(line + '\n') for line in ips]
        results.close()

    except urllib3.exceptions.MaxRetryError:
        email_report = ' Url is unreachable : '
        email_report += str(url)
        email_report += '\n'

    if email_report != '':
        send_mail('fzdahmane@gmail.com', 'pulling from ip source problem report', email_report)
        # send_mail('abdou@johnsnowlabs.com', 'pulling from Domain names source problem report', email_report)

    return ips


if __name__ == '__main__':
    do_fetch()
