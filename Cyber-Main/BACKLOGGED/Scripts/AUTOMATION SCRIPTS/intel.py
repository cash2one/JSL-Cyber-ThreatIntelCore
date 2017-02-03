#!/usr/bin/python
#################################################################################
#	CyberIntel - OSINT Cyber Threat Intelligence Feed for ArcSight				#
#	freecyberintel at gmail.com												#
#-------------------------------------------------------------------------------#
#	Copyright (C) 2013  Cyber Intel											#
#																				#
#	This program is free software: you can redistribute it and/or modify		#
#	it under the terms of the GNU General Public License as published by		#
#	the Free Software Foundation, either version 3 of the License, or			#
#	(at your option) any later version.										#
#																				#
#	This program is distributed in the hope that it will be useful,			#
#	but WITHOUT ANY WARRANTY; without even the implied warranty of				#
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the				#
#	GNU General Public License for more details.								#
#																				#
#	You should have received a copy of the GNU General Public License			#
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.		#
#################################################################################

## Version 0.3
##
## New Features:
## 		Proxy User Authentication
##		Updated Sources

from os import listdir
from os.path import isfile, join

import dns.resolver
import csv
import urllib2, time, re, socket, sys, select
from optparse import OptionParser
badsips = []

socket.setdefaulttimeout(10)

cyberIntelVersion = "0.3"
proxyEnabled = "no"
syslogServer = "localhost"
writeOutFileName = ""
syslogPort = 514
#proxyUser = ""


ipAddressRegex = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
domainNameRegex = re.compile(r"([\w\.][-\w\.]{0,253}[\w\.]+\.)+([a-zA-Z]{2,9})")
commentString1 = re.compile("#.*?\n")
commentString2 = re.compile("\.in-addr\.arpa\.?")
commentString3 = re.compile(r"^[a-z0-9].*")


tor_sources = {
		'https://check.torproject.org/exit-addresses':'TOR',
		'http://torstatus.rueckgr.at/router_detail.php?':'TOR',
		'https://globe.torproject.org/':'TOR',
		'http://rules.emergingthreats.net/open/suricata/rules/tor.rules':'TOR'
}


spam_sources = {
	'http://reputation-email.com/reputation/rep_worst.htm':'spam', #just take IPS
		'http://www.unsubscore.com/blacklist.txt':'spam',
	'http://mirror1.malwaredomains.com/files/domains.txt':'spam' , # search 'spamhause.org' in the text file and parse host name/domain name attached to it. This will require parsing script
		 'http://dnsbl.inps.de/analyse.cgi?lang=en&action=show_changes':'spam', # Timestamp/ips/domains
		 'http://antispam.imp.ch/spamlist':'spam', # schema to be laid out:ip-address	unixtime	hostname
		'http://spamvertised.abusebutler.com/stats.php':'spam'
}

dns_bl_sources  = {
	'http://www.openbl.org/lists/base_all.txt':'DNS BL',
	'http://www.dnsbl.manitu.net/partners.php?language=en':'DNS BL'
}

phishing_sources = {

	'http://dns-bh.sagadc.org/20160219.txt':'PHISHING' ,
		'http://mirror1.malwaredomains.com/files/domains.txt':'PHISHING'
}

ssl_black_list = {
	'https://sslbl.abuse.ch/downloads/ssl_extended.csv':'SSL BL'
}

ddns_sources = {
	'http://dns-bh.sagadc.org/dynamic_dns.txt':'DDNS'
}

badIpSources = {

	"https://www.autoshun.org/files/shunlist.csv":'MALWARE',
	"https://www.badips.com/get/list/any/2?age=7d":"badips known attackers",
	"http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist-high.txt":'MALWARE',
	"http://osint.bambenekconsulting.com/feeds/dga-feed.txt": 'bambenek DGA feed',
	"https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/bitcoin_nodes_1d.ipset": 'bitcoin nodes',
	'http://lists.blocklist.de/lists/all.txt':'MALWARE',
	'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/botscout_1d.ipset':'MALWARE',
	'http://danger.rulez.sk/projects/bruteforceblocker/blist.php':'MALWARE',
	'ht+tp://cinsscore.com/list/ci-badguys.txt':'MALWARE',
	'http://www.mtc.sri.com/live_data/attackers/':'MALWARE',
	'http://isc.sans.edu/reports.html':'MALWARE',
	'http://www.projecthoneypot.org/list_of_ips.php':'MALWARE',
	'http://www.openbl.org/lists/base.txt':'MALWARE',
	'http://www.nothink.org/blacklist/blacklist_malware_http.txt':'MALWARE',
	'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist':'MALWARE',
	'https://spyeyetracker.abuse.ch/blocklist.php?download=ipblocklist':'MALWARE',
	'https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist':'MALWARE',
	'http://www.malwaredomainlist.com/hostslist/ip.txt':'MALWARE',
	'http://rules.emergingthreats.net/blockrules/compromised-ips.txt':'MALWARE',
	'http://rules.emergingthreats.net/blockrules/emerging-botcc.rules':'MALWARE',
	'http://rules.emergingthreats.net/fwrules/emerging-PF-CC.rules':'MALWARE',

	'http://rules.emergingthreats.net/blockrules/emerging-ciarmy.rules':'MALWARE',
	'http://doc.emergingthreats.net/pub/Main/RussianBusinessNetwork/emerging-rbn-malvertisers.txt':'MALWARE',
}


badDomainSources = {
	'http://www.nothink.org/blacklist/blacklist_malware_dns.txt':'MALWARE',
	'http://secure.mayhemiclabs.com/malhosts/malhosts.txt':'MALWARE',
	'http://mirror1.malwaredomains.com/files/justdomains':'MALWARE',
	'http://www.malwaredomainlist.com/hostslist/hosts.txt':'MALWARE',
	'http://isc.sans.edu/feeds/suspiciousdomains_Low.txt':'MALWARE',
	'http://isc.sans.edu/feeds/suspiciousdomains_Medium.txt':'MALWARE',
	'http://isc.sans.edu/feeds/suspici ousdomains_High.txt':'MALWARE',
	'https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist':'MALWARE',
	'https://spyeyetracker.abuse.ch/blocklist.php?download=domainblocklist':'MALWARE',
	'https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist':'MALWARE',
}
import socket
domains = []
DATA = []


def dictToCSV(dict, fname):
    temp = []

    for elmt in dict:
        if elmt is not None:
            temp.append(elmt)

    dict = temp

    keys = set().union(*(d.keys() for d in dict))
    #for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname+'.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dict)
        print dict


def resolve(ip):
	for i in ip:
         try:

            socket.setdefaulttimeout(1)

            answers = socket.gethostbyaddr(i)

            #print answers
            DATA.append({'domainName':answers[0], 'ipAddress' : answers[2][0]})
            #print answers

         except:
            import traceback

def main(filename, regex, ips):
	mypaths = ['suspicious']
	mypaths = ['malware', 'badips', 'baddomains']

	temp = []

	for mypath in mypaths:
		onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

		for fileName in onlyfiles:
			with open(mypath+'\\'+fileName) as oldfile:

					outfile = open(filename, 'a')
					for line in compileOutput(oldfile.read(), regex):
						#print line
						if ips is not None:

							temp.append(line)
						else :

							outfile.write(line[0]+line[1]+'\n')
	#print temp
	return temp


def syslog(message,host,port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	data = '<29>%s' + message
	sock.sendto(data, (host, port))
	sock.close()


def writeOutput(source,data,outputMethod,dataType):
	if outputMethod == "syslog":
		for line in data:
			if dataType == "Domain":
				line = line[0]+ line[1]
				res = re.match(r"^[a-z0-9].*", line)
				if res is not None:
					line = res.group(0)
					if not line.startswith("iFrame"):
#						line = res.group(0) + "," + source + "\n"
						cef = 'CEF:0|CyberIntel|MalDomain|0.1|100|Known Malicious '+dataType+'|5|dhost='+line+' msg='+source
			elif dataType == "IP":
				cef = 'CEF:0|CyberIntel|MalIP|0.1|100|Known Malicious '+dataType+'|5|dst='+line+' msg='+source
			syslog(cef,syslogServer,syslogPort)

	elif outputMethod == "file":
		f = open(writeOutFileName, 'a')
		for line in data:
			if dataType == "Domain":
				line = line[0]+ line[1]
				res = re.match(r"^[a-z0-9].*", line)
				if res is not None:
					line = res.group(0)
					if not line.startswith("iFrame"):
						line = res.group(0) + "," + source + "\n"
						f.write(line)
			if dataType == "IP":
				line = line + "," + source + "\n"
				f.write(line)
		f.close()


def compileOutput(site,regex):
		result = re.sub(commentString1,"", site)
		result = re.sub(commentString2,"", result)
		return re.findall(regex, result)




def scrapeIntel(url,regex):
	try:
		if proxyEnabled == "yes":
			proxy_url = "http://%s:%s" % (options.proxy, options.proxy_port)
			https_url = "https://%s:%s" % (options.proxy, options.proxy_port)
			proxy_support = urllib2.ProxyHandler({'http': proxy_url, 'https':https_url})
			if options.proxy_user:
				password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
				password_mgr.add_password(None, proxy_url, options.proxy_user, options.proxy_pass)
				proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_mgr)
				opener = urllib2.build_opener(proxy_support, proxy_auth_handler)
				urllib2.install_opener(opener)
			else:
				opener = urllib2.build_opener(proxy_support)
				urllib2.install_opener(opener)

		print "Grabbing data from: "+url
		webSite = urllib2.urlopen(url).read()
		return compileOutput(webSite, regex)
	except:
		import traceback
		traceback.print_exc()
		print 'Connection Failed: '+url
		return "false"


def processData(output):
	'''
	if options.sslip:
		for URL,Name in ssl_black_list.iteritems():
			result = scrapeIntel(URL,ipAddressRegex)

			if result != "false":
				writeOutput(Name,result,options.output,"IP")
	elif options.phishingip:
		for URL,Name in phishing_sources.iteritems():
			result = scrapeIntel(URL,ipAddressRegex)

			if result != "false":
				writeOutput(Name,result,options.output,"IP")
	elif options.spamip:
		for URL,Name in spam_sources.iteritems():
			result = scrapeIntel(URL,ipAddressRegex)

			if result != "false":
				writeOutput(Name,result,options.output,"IP")
	elif options.torip:
		for URL,Name in tor_sources.iteritems():
			result = scrapeIntel(URL,ipAddressRegex)

			if result != "false":
				writeOutput(Name,result,options.output,"IP")
	elif options.ddnsip:

		for URL,Name in ddns_sources.iteritems():
			result = scrapeIntel(URL,ipAddressRegex)

			if result != "false":
				writeOutput(Name,result,options.output,"IP")
	'''
	if options.badip:
		for URL,Name in badIpSources.iteritems():
		#for URL,Name in ddns_sources.iteritems():
			result = scrapeIntel(URL,ipAddressRegex)

			if result != "false":
				writeOutput(Name,result,options.output,"IP")
	elif options.baddomain:
		for URL,Name in phishing_sources.iteritems():
			result = scrapeIntel(URL,domainNameRegex)
			if result != "false":
				writeOutput(Name,result,options.output,"Domain")
	else:
		print "no input source defined"
		sys.exit()


if __name__ == "__main__":
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option(	"-v", "--version",
					  	action="store_true", dest="version",
					  	default=False,
					  	help="show version")
	parser.add_option(	"--badip", dest="badip", action="store_true",
				help="Get bad IP addresses")
	parser.add_option(	"--baddomain", dest="baddomain", action="store_true",
				help="Get bad domain names")
	parser.add_option(	"-o", "--output",
				action="store", dest="output",
					  	metavar="METHOD", help="select output method syslog/file")
	parser.add_option(	"-s", "--syslog",
				action="store", dest="syslog_server",
					  	metavar="SERVER", help="select syslog server SERVER")
	parser.add_option(	"-p", "--port",
				action="store", type=int, dest="syslog_port",
					  	metavar="PORT", help="syslog PORT")
	parser.add_option(	"-f", "--file",
				action="store", dest="file_name",
					  	metavar="FILE", help="select filename to write to")
	parser.add_option(	"--proxy",
				action="store", dest="proxy",
				metavar="PROXY", help="connect via proxy PROXY")
	parser.add_option(	"--proxy_port", action="store", dest="proxy_port",
				metavar="PROXY_PORT", help="proxy server port")
	parser.add_option(	"--proxy_user", action="store", dest="proxy_user",
				metavar="PROXY_USER", help="proxy username")
	parser.add_option(	"--proxy_pass", action="store", dest="proxy_pass",
				metavar="PROXY_PASS", help="proxy password")


	(options, args) = parser.parse_args()


	if options.version:
		print "CyberIntel", cyberIntelVersion
		sys.exit()

	if options.proxy:
		proxyEnabled = "yes"

	if not options.output:
		parser.print_help()
		sys.exit()

	if options.output == "syslog":
		if not options.syslog_server:
			print "syslog server required\n"
			sys.exit()
		else:
			syslogServer = options.syslog_server
			if options.syslog_port:
				syslogPort = options.syslog_port
			processData(options.output)
	elif options.output == "file":
		if not options.file_name:
			print "please select filename to write to\n"
			sys.exit()
		else:
			writeOutFileName = options.file_name
			processData(options.output)
			if options.badip:

				#badsips = main(writeOutFileName, ipAddressRegex, badsips)


				fbad = open('badips.txt', 'w')



				for ip in badsips:
				    fbad.write(ip+'\n')
				print badsips
				#resolve(badsips)
				#dictToCSV(DATA, "outpuuut")


			else:
				main(writeOutFileName, domainNameRegex, None)
	else:
		print "select a correct output method\n"
		#parser.print_help()
sys.exit()
