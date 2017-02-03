
MALWARE BlackList  
	BY_IP:
		'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist' #abuse.ch ZeuS domain blocklist "BadDomains" (excluding hijacked sites)
		'http://www.malwaredomainlist.com/hostslist/ip.txt'
		'http://www.malwaredomainlist.com/mdlcsv.php'  #complete database in csv format
		http://cybercrime-tracker.net/fuckerz.php # pull only IP
	Parsing:
		'http://cybercrime-tracker.net/all.php'
MALWARE Black List
	 BY_DOMAIN:
		'http://mirror1.malwaredomains.com/files/domains.txt'
		'http://secure.mayhemiclabs.com/malhosts/malhosts.txt' #NEW DATASOURCE


SSL_Black List:
	Parsing:
		 'https://sslbl.abuse.ch/downloads/ssl_extended.csv' #
		# Timestamp of Listing (UTC)	Referencing Sample (MD5)	Destination IP	Destination Port	SSL certificate SHA1 Fingerprint	Listing reason

Phishing  Black List:
	By_Domain:
		'http://dns-bh.sagadc.org/20160219.txt' # domains NEW DATASOURCE
		'http://mirror1.malwaredomains.com/files/domains.txt'  #domains NEW DATASOURCE

DNS Black List:
	By_IP:
		'http://www.openbl.org/lists/base_all.txt'] # DNS Black List
	Parsing:
		http://www.dnsbl.manitu.net/partners.php?language=en #good parsing information

Spam Black List:
	By_IP:
		'http://reputation-email.com/reputation/rep_worst.htm' #just take IPS
		'http://www.unsubscore.com/blacklist.txt'
	Parse:
		'http://mirror1.malwaredomains.com/files/domains.txt'  # search 'spamhause.org' in the text file and parse host name/domain name attached to it. This will require parsing script
		 'http://dnsbl.inps.de/analyse.cgi?lang=en&action=show_changes' # Timestamp/ips/domains
		 'http://antispam.imp.ch/spamlist' # schema to be laid out:ip-address	unixtime	hostname
		'http://spamvertised.abusebutler.com/stats.php'

Dynamic DNS Resolution :
	By_Domain:
		'http://dns-bh.sagadc.org/dynamic_dns.txt' #Dynamic DNS Black List


TOR IP RESOLUTION:
	BY_URL:

