# -*- coding: utf-8 -*-


import scrapy
import re
import json
import csv
from ipwhois import IPWhois
from pprint import pprint
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from blacklist_enrichment.items import TestItem


class WhoIsSpider(CrawlSpider):
	name = "DNSBL2"
	#create list of keywords, and loop through searches here
	def start_requests(self):

		###############################
		###for single source datasets##     
		###############################

		url  = 'file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/6_3_2016/WHOIS_DATA/DNS_BL_IPs20160304.csv'   #ipBlacklist6.csv
		yield Request(url, callback=self.parse_file_url)



	def parse_file_url(self, response):
		get_url = response #this gets us current URL crawling!
		url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
		#i.e. here, we have: <200 file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/6_3_2016/WHOIS_DATA/DNS_BL_domains201603032016.csv>


		all_data = response.xpath('//*').extract()
		all_data = all_data[0]
		allrows = all_data.split('\r\n')

		getcells = [e.split(',') for e in allrows]
		clearspaces = [[e[i].replace(re.match('.*(\s+)$', e[i]).group(1), '') if re.match('.*(\s+)$', e[i]) else e[i] for i, f in enumerate(e)] for e in getcells]
		cleartags = [[e[j].replace(re.match('.*?(<.*>).*', e[j]).group(1), '') if re.match('.*?(<.*>).*', e[j]) else e[j] for j, f in enumerate(e)] for e in clearspaces]
		clearspaces = [[e[k].replace(re.match('^(\s+).*', e[k]).group(1), '') if re.match('^(\s+).*', e[k]) else e[k] for k, f in enumerate(e)] for e in cleartags]
		replaceNA = [['' if e[l] == 'NA' else e[l] for l, f in enumerate(e)] for e in clearspaces]


		data = replaceNA

		#u'NA', u'1.23.226.221', u'NA', u'IN', u'apnic', u'2010-05-05', u'NA'


		for i, e in enumerate(data):
			item = TestItem()
			try:
				item['Autonomous_System_Number'] = data[i][0]
			except:
				item['Autonomous_System_Number'] = ''
			try:
				item['Address_IP'] = data[i][1]   
			except: 
				item['Address_IP'] = ''
			try:
				item['Autonomous_System_Number_CIDR'] = data[i][2]  
			except:  
				item['Autonomous_System_Number_CIDR'] = ''
			try:
				item['Country_Code_Text'] = data[i][3] 
			except:
				item['Country_Code_Text'] = ''
			try:
				item['Regional_Internet_Registries'] = data[i][4]
			except:
				item['Regional_Internet_Registries'] = ''
			try:
				item['Autonomous_System_Number_date'] = data[i][5] 
			except:
				item['Autonomous_System_Number_date'] = ''
			try:
				item['Information_Text'] = data[i][6]
			except:
				item['Information_Text'] = ''

			yield item




#scrapy crawl DNSBL2 -o DNSBL2.csv



































# DNS_BL_domains201603032016.csv -> done
# DNS_BL_IPs20160304.csv -> done

# DYNAMIC_DNS_IPS20160303output.csv
# Dynamic_DNS_RES_IPsDoutput20160304.csv
# DYNAMIC_DNSoutput20160305.csv
# MALWARE_BL_IPs20160303output.csv
# MALWARE_IPsDoutput20160304.csv
# PHISHING_BL_IPs20160303output.csv
# PHISING_IPsDoutput20160304.csv
# SPAM_IPs20160303output.csv
# SPAM_IPsDoutput20160304.csv
# SSL_BL_IPS20160303output.csv