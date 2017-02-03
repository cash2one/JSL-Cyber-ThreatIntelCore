import time
import datetime
import urllib3
import re
import sys
import os
import gzip
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from cStringIO import StringIO
import subprocess

url = "https://www.dshield.org/feeds/suspiciousdomains_High.txt"
DOMAIN_NAME_REGEX = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}


def do_fetch():
    report = open('../report', 'a')
    cleaned_domain_names = []
    email_report = ''
    http = urllib3.PoolManager(10, headers=user_agent)

    print "pulling from %s " % url
    try:
        r = http.request('GET', url)
        domain_names = []
        for line in r.data.split('\n'):
            if not line.startswith('#'):
                domain_names += re.findall(DOMAIN_NAME_REGEX, line)
        for ip in domain_names:
            if not (ip.endswith('.txt') or ip.endswith('.php') or ip.endswith('.html') or ip.endswith('.jpeg')
                    or ip.endswith('.bin') or ip.endswith('.jpg') or ip.endswith('.htm') or ip.endswith('.htmls')):
                cleaned_domain_names.append(ip)
        print "%s domain names pulled from %s" % (len(domain_names), url)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        report.write("%s domain names pulled from %s at %s \n" % (len(domain_names), url, st))

        results = open('../output_domains', 'a')
        [results.write(line + '\n') for line in cleaned_domain_names]
        results.close()

        # aggregationreport.add_pull('domain names', url, len(domain_names))

    except urllib3.exceptions.MaxRetryError:
        email_report = ' Url is unreachable : '
        email_report += str(url)

    return cleaned_domain_names


if __name__ == '__main__':
    do_fetch()
