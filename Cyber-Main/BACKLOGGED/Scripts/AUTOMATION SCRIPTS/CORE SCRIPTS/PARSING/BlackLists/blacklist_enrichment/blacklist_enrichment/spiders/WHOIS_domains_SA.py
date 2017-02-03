###whois test - Seraphina Anderson, John Snow Labs###

# -*- coding: utf-8 -*-


import whois
import scrapy
import re
import json
import csv
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from blacklist_enrichment.items import WhoIsItem


########################################
###generate a list of domains, or ips###
########################################


#CODE BLOCK 1: Get list of ip addresses or domains from a CSV file, OR
#CODE BLOCK 2: Get list of ip addresses or domains directly from a list of
#source urls


class BlackLists(CrawlSpider):
    name = "whois_domains"
    #create list of keywords, and loop through searches here
    def start_requests(self):

        ###############################
        ###for single source datasets##     
        ###############################

        url  = 'http://secure.mayhemiclabs.com/malhosts/malhosts.txt'   #ipBlacklist6.csv
        yield Request(url, callback=self.parse_domain_blacklist_url)

        # urls = ['https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist',    #spam  #ipBlacklist1 => length = 
        #         'https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist',  #spam? #ipBlacklist3 => length = 
        #         'https://zeustracker.abuse.ch/blocklist.php?download=badips',  #spam  #ipBlacklist2 => length = 
        #         'http://malc0de.com/bl/IP_Blacklist.txt',   #walware  #ipBlacklist4 => length = 
        #         'http://www.binarydefense.com/banlist.txt',  #spam ?  #ipBlacklist5 => length = 
        #         'http://www.unsubscore.com/blacklist.txt',   #spam  #ipBlacklist6 => length =    
        #         'http://antispam.imp.ch/spamlist',  #spam   TEST FROM HERE!
        #         'http://wget-mirrors.uceprotect.net/rbldnsd-all/ips.backscatterer.org.gz']  #spam
                
                

        # for i, e in enumerate(urls):
        #     url = urls[i]
        #     yield Request(url, callback=self.parse_ip_blacklist_url)
            
        

    def parse_domain_blacklist_url(self, response):
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up

        
        #ASSIGN ID TO DATASOURCE
        # if 'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist' in url:
        #     num = '1'

        # elif 'https://zeustracker.abuse.ch/blocklist.php?download=badips' in url:
        #     num = '2'

        # elif 'https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist' in url:
        #     num = '3'

        # elif 'http://malc0de.com/bl/IP_Blacklist.txt' in url:
        #     num = '4'

        # elif 'http://www.binarydefense.com/banlist.txt' in url:
        #     num = '5'
      
        # elif 'http://www.unsubscore.com/blacklist.txt' in url:
        #     num = '6'
            
        # else:
        #     num = 'error - check code!!!'


        ###ASSIGN BLACKLIST TYPE NAMES###
        if 'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist' in url:
            blackListType = 'spam'
        elif 'https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist' in url:
            blackListType = 'spam'
        elif 'https://zeustracker.abuse.ch/blocklist.php?download=badips' in url:
            blackListType = 'spam'
        elif 'http://malc0de.com/bl/IP_Blacklist.txt' in url:
            blackListType = 'malware'
        elif 'http://www.binarydefense.com/banlist.txt' in url:
            blackListType = 'spam'
        elif 'http://www.unsubscore.com/blacklist.txt' in url:
            blackListType = 'spam'
        elif 'http://antispam.imp.ch/spamlist' in url:
            blackListType = 'spam'
        elif 'http://wget-mirrors.uceprotect.net/rbldnsd-all/ips.backscatterer.org.gz' in url:
            blackListType = 'spam'
        elif 'https://www.blocklist.de/downloads/export-ips_all.txt' in url:
            blackListType = 'spam'
        else:
            blackListType = "Something's broken!"



        
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up

        getall = response.xpath('//body').extract()
        getrows = getall[0].split('\n')
        #filter out unwanted rows
        clean = [e for e in getrows if '#' not in e]
        clean = [e for e in clean if re.match('^.*?\w+.*$', e)]
        separate_columns = [e.split('\t') for e in clean]
        clean_blank_rows = [e for e in separate_columns if '' not in e]
        data = clean_blank_rows
        domains = [e[0] for e in data]

        #data fields
        #sample data item:  [u'039b1ee.netsolhost.com', u'ZeuS/WNSPoem/ZBot', u'ZT', u'0']

        
        for i, e in enumerate(domains):
            item = WhoIsItem()
            domain = domains[i]
            w = whois.whois(str(domain))
            #updated_date = w['updated_date']
            #item['updated_date'] = w['updated_date']
            

            item['updated_date'] = w.updated_date
            item['status'] = w.status
            item['name'] = w.name
            item['dnssec'] = w.dnssec
            item['city'] = w.city
            item['expiration_date'] = w.expiration_date
            item['zipcode'] = w.zipcode
            item['domain_name'] = w.domain_name
            item['country'] = w.country
            item['whois_server'] = w.whois_server
            item['state'] = w.state
            item['registrar'] = w.registrar
            item['referral_url'] = w.referral_url
            item['address'] = w.address
            item['name_servers'] = w.name_servers
            item['org'] = w.org
            item['creation_date'] = w.creation_date
            item['emails'] = w.emails
            #item['ip_Address_Text'] = ipAddress[i]
            #item['Blacklist_Type_Name'] = blackListType

            yield item 
           


            #output:
            #scrapy crawl whois_domains -o whois_sample2.csv
    		


        # query a particular url or ip address
		#w = whois.whois('webscraping.com')
		# get list of data fields to query:
		#keys = w.keys()
		#query a particular data field:
		#w.expiration_date
		#get a list of particular values:
		#w['emails']







#####################
###whois variables###
#####################

#['updated_date', 'status', 'name', 'dnssec', 'city', 'expiration_date',
#'zipcode', 'domain_name', 'country', 'whois_server', 'state', 'registrar',
#'referral_url', 'address', 'name_servers', 'org', 'creation_date', 'emails']

#1 updated_date
#2 status
#3 name
#4 dnssec
#5 city
#6 expiration_date
#7 zipcode
#8 domain_name
#9 country
#10 whois_server
#11 state
#12 registrar
#13 referral_url
#14 address
#15 name_servers
#16 org
#17 creation_date
#18 emails

       
        



        #CSV files:

        #combined source datasets
        #scrapy crawl bl2a -o blacklists_combined_a.csv






#example whois dictionary:

##{
##  "updated_date": "2013-08-20 00:00:00", 
##  "status": [
##    "clientDeleteProhibited https://www.icann.org/epp#clientDeleteProhibited", 
##    "clientRenewProhibited https://www.icann.org/epp#clientRenewProhibited", 
##    "clientTransferProhibited https://www.icann.org/epp#clientTransferProhibited", 
##    "clientUpdateProhibited https://www.icann.org/epp#clientUpdateProhibited", 
##    "clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited", 
##    "clientUpdateProhibited http://www.icann.org/epp#clientUpdateProhibited", 
##    "clientRenewProhibited http://www.icann.org/epp#clientRenewProhibited", 
##    "clientDeleteProhibited http://www.icann.org/epp#clientDeleteProhibited"
##  ], 
##  "name": "Richard Penman", 
##  "dnssec": "unsigned", 
##  "city": "Melbourne", 
##  "expiration_date": [
##    "2020-06-26 00:00:00", 
##    "2020-06-26 18:01:19"
##  ], 
##  "zipcode": "3056-02-14 00:00:00", 
##  "domain_name": "WEBSCRAPING.COM", 
##  "country": "AU", 
##  "whois_server": "whois.godaddy.com", 
##  "state": "Victoria", 
##  "registrar": [
##    "GODADDY.COM, LLC", 
##    "GoDaddy.com, LLC"
##  ], 
##  "referral_url": "http://www.godaddy.com", 
##  "address": "13/815 Leonard St", 
##  "name_servers": [
##    "NS1.WEBFACTION.COM", 
##    "NS2.WEBFACTION.COM", 
##    "NS3.WEBFACTION.COM", 
##    "NS4.WEBFACTION.COM"
##  ], 
##  "org": "Registrant Street: 13/815 Leonard St", 
##  "creation_date": [
##    "2004-06-26 00:00:00", 
##    "2004-06-26 18:01:19"
##  ], 
##  "emails": [
##    "abuse@godaddy.com", 
##    "contact@webscraping.com"
##  ]
##}
