from antispam_imp import *
from malwares.cybercrime_tracker import *
from dnsbl_inps import *
from dnsbl_manitu import *
from malwares.parse_malware_domains import *
from reputation_email import *
from sorbs_ips import *
from unsubscore import *
from malwares.zeustracker import *
from malwares.malc0de import *
from malwares.palevo import *
from malwares.feodo_tracker import *
from malwares.zeus_tracker import *
from pyexcel.cookbook import merge_all_to_a_book
import pyexcel.ext.xlsx # needed to support xlsx format, pip install pyexcel-xlsx



'''
print "######################################################################"

for csvfile in ["malware.csv", "spam.csv"]:
    workbook = Workbook(csvfile + '.xlsx')
    worksheet = workbook.add_worksheet()
    with open(csvfile, 'rb') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()
    print "######################################################################"

    wb = xlwt.Workbook()
    ws = wb.add_sheet(csvfile.split('.')[0])
    with open(csvfile, 'rb') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    ws.write(r, c, col)
    wb.save('output.xls')
'''



WHOIS_FILES = ['list1_list2outputwhois',
               'list3outputwhois',
               'list4outputwhois']

SPAMS_OLD = ['http://dnsbl.inps.de/analyse.cgi?lang=en&action=show_changes',
'http://antispam.imp.ch/spamlist',
'http://www.dnsbl.manitu.net/partners.php?language=en',
'http://reputation-email.com/reputation/rep_worst.htm',
'http://www.sorbs.net/home/stats.shtml',
'http://www.unsubscore.com/blacklist.txt']

SPAMS = []
DDNS_BL = ['http://dns-bh.sagadc.org/dynamic_dns.txt'] #Dynamic DNS Black List




MALWARE_OLD = ['http://www.malwaredomainlist.com/mdl.php?inactive=&sort=Date&search=&colsearch=All&ascordesc=DESC&quantity=100000&page=0',
'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist',
'https://zeustracker.abuse.ch/blocklist.php?download=baddomains',
'http://cybercrime-tracker.net/index.php?s=0&m=400000',
'http://malc0de.com/database/?&page=1',
'https://palevotracker.abuse.ch/']

MALWARE = ['https://feodotracker.abuse.ch/',
           'https://palevotracker.abuse.ch/',
           'https://zeustracker.abuse.ch/monitor.php?filter=all']

def dictToCSV(dict, fname):
    keys = set().union(*(d.keys() for d in dict))
    #for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname+'.csv', 'wb') as output_file:
        output_file.write('''ip_address,listing_date,host_name,autonomous_system_number,description_text,zeus_tracker,spyeye_tracker,feodo_tracker,palevo_tracker\n''')
        #dictWriter = csv.DictWriter(output_file, keys)
        #dictWriter.writeheader()
        keys = set().union(*(d.keys() for d in dict))
        #dictWriter.writerows(dict)
        for element in dict:

            for key in keys:
                if key not in element.keys() or element[key] is None:
                    element[key] = ''
                    print element

            print element
            output_file.write(element['ip_address']+','+element['listing_date']+','+element['host_name']+','+element['autonomous_system_number']+','+element['description_text']+','+element['zeus_tracker']+','+element['spyeye_tracker']+','+element['feodo_tracker']+','+element['palevo_tracker']+','+'\n')
        print dict

malware_results = []
spam_results = []
all_whois = {}

for file in WHOIS_FILES:
    with open(file) as whois_file:
        lines = whois_file.readlines()
        for i in range(0, len(lines), 2):
            lines[i+1] = lines[i+1].replace('\n', '')
            lines[i+1] = lines[i+1].replace(' ', '')
            lines[i+1] = lines[i+1].replace('\t', '').split('|')
            all_whois[lines[i+1][1]] = [lines[i+1][2], lines[i+1][0]]


for spam in SPAMS:

    if 'antispam.imp' in spam:
        spam_results = spam_results + anti_spam_imp_ips(spam)
        #dictToCSV(all_results)

    elif 'dnsbl.inps' in spam:

        print len(spam_results)
        spam_results += dnsbl_ips(spam)
        print len(spam_results)
    elif 'dnsbl.manitu' in spam:

        spam_results += dnsbl_manitu(spam)
    elif 'reputation-email' in spam:

        spam_results += reputation_email_ips(spam)
    elif 'sorbs.net' in spam:

        spam_results += sorbs_ips(spam)
        spam_results += sorbs_domains(spam)
    elif 'unsubscore.com' in spam:

        spam_results += unsubscore_ips(spam)

for spam in MALWARE:



    if 'www.malwaredomainlist' in spam:
        malware_results  = malware_results + parse_malware_domains(spam)

    elif 'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist' in spam:

        malware_results += parse_zeus_ips(spam)
    elif 'https://zeustracker.abuse.ch/blocklist.php?download=baddomains' in spam:

        malware_results += parse_zeus_domains(spam)
    elif 'malwaredomains.com' in spam:

        malware_results += parse_malware_domains(spam)

    elif 'cybercrime-tracker' in spam:

        malware_results += parse_cyberCrime(spam)

    elif 'malc0de' in spam:

        malware_results += malc0de_ips(spam)

    elif 'palevo' in spam:
        malware_results += palveo_ips(spam)

    elif 'feodo' in spam:
        malware_results += feodo_tracker_ips(spam)

    elif 'https://zeustracker.abuse.ch/monitor.php?filter=all' in spam :
        malware_results += zeus_tracker_ips(spam)





for i in range(len(spam_results)):

    if 'ip_address' in spam_results[i].keys() and spam_results[i]['ip_address'] in all_whois.keys():

        spam_results[i]['autonomous_system_name'] = all_whois[spam_results[i]['ip_address']][0]
        spam_results[i]['autonomous_system_number'] = all_whois[spam_results[i]['ip_address']][1]

for i in range(len(malware_results)):

    if 'ip_address' in malware_results[i].keys() and malware_results[i]['ip_address'] in all_whois.keys():

        malware_results[i]['autonomous_system_name'] = all_whois[malware_results[i]['ip_address']][0]
        malware_results[i]['autonomous_system_number'] = all_whois[malware_results[i]['ip_address']][1]




dictToCSV(malware_results, "malware")

#dictToCSV(spam_results, "spam")



merge_all_to_a_book(["malware.csv", "spam.csv"], "output.xlsx")

'''
for csvfile in ["malware.csv", "spam.csv"]:
    wb = xlwt.Workbook()
    ws = wb.add_sheet(csvfile.split('.')[0])
    with open(csvfile, 'rb') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    ws.write(r, c, col)
    wb.save('output.xls')

'''
