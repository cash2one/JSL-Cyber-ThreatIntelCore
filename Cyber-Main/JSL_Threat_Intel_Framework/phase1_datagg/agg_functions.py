from Constants import *
import urllib3
import re
import os
import gzip
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from cStringIO import StringIO
import subprocess
from aggregation_report import *



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


def pull_ips(sources, aggregationreport):
    ips = []
    email_report = ''
    for url in sources:

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
            aggregationreport.add_pull('ips', url, len(items))

        except urllib3.exceptions.MaxRetryError:
            email_report = ' Url is unreachable : '
            email_report += str(url)
            email_report += '\n'

    if email_report != '':
        send_mail('fzdahmane@gmail.com', 'pulling from ip source problem report', email_report)
        # send_mail('abdou@johnsnowlabs.com', 'pulling from Domain names source problem report', email_report)

    return ips


def pull_dns(sources, aggregationreport):
    cleaned_domain_names = []
    email_report = ''
    http = urllib3.PoolManager(10, headers=user_agent)
    for url in sources:
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
            aggregationreport.add_pull('domain names', url, len(domain_names))

        except urllib3.exceptions.MaxRetryError:
            email_report = ' Url is unreachable : '
            email_report += str(url)

    if email_report != '':
        send_mail('fzdahmane@gmail.com', 'pulling from Domain names source problem report', email_report)
        # send_mail('abdou@johnsnowlabs.com', 'pulling from Domain names source problem report', email_report)

    return cleaned_domain_names


def pull_all(offender_class):
    aggregationreport = AggregationReport()
    aggregationreport.add_phase('phase_1')
    badips = pull_ips(BADIPS[offender_class], aggregationreport)
    baddomains = pull_dns(BADDOMAINS[offender_class], aggregationreport)
    aggregationreport.end_phase("phase1")
    print aggregationreport.pulls
    return [badips, baddomains, aggregationreport.pulls]


def send_mail(recipient, subject, message):
    username = "abdou@johnsnowlabs.com"
    password = "134613NaClDZ"

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    try:
        print('sending mail to ' + recipient + ' on ' + subject)

        mailServer = smtplib.SMTP('smtp.office365.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
        mailServer.sendmail(username, recipient, msg.as_string())
        mailServer.close()

    except:
        import traceback
        traceback.print_exc()
        print "exception"

# send_mail('abdou@johnsnowlabs.com', 'This is a test', 'message coucou cheri')
