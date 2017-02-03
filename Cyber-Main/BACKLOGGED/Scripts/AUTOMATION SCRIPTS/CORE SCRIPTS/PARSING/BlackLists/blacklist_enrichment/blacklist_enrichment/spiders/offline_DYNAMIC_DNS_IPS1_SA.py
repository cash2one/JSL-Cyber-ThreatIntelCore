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
	name = "DYNAMIC_DNS_IPS1"
	#create list of keywords, and loop through searches here
	def start_requests(self):

		###############################
		###for single source datasets##     
		###############################

		url  = 'file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/6_3_2016/WHOIS_DATA/DYNAMIC_DNS_IPS20160303output.csv'   #ipBlacklist6.csv
		yield Request(url, callback=self.parse_file_url)



	def parse_file_url(self, response):
		get_url = response #this gets us current URL crawling!
		url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
		#i.e. here, we have: <200 file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/6_3_2016/WHOIS_DATA/DNS_BL_domains201603032016.csv>


		all_data = response.xpath('//*').extract()
		all_data = all_data[0]
		allrows = all_data.split('\r\n')

		cleartags = [e.replace(re.match('.*?(<.*>).*', e).group(1), '') if re.match('.*?(<.*>).*', e) else e for e in allrows]
		testgap = [e for e in cleartags if re.match('^\s*(\d{4,6}\s+).*', e)]

		getcells = [e.split(re.match('.*?(\s{2,}).*', e).group(1)) for e in testgap if re.match('.*?(\s{2,}).*', e)] 
		clearblanks = [[f for f in e if f != ''] for e in getcells]
		clearblanks = [[f for f in e if f != ' '] for e in clearblanks]

		#splitas = [[e[i].split(re.match('\s*\d{4,6}(\s+).*', e[i]).group(1)) if (i == 0 and re.match('.*?\d{4,6}(\s+).*', e[i])) else e[i] for i, f in enumerate(e)] for e in clearblanks]



		[u'20773',
  		u'80.237.146.9',
  		u' 80.237.128.',
  		u' DE',
  		u'ripenc',
  		u'HOSTEUROPE-AS Host Europe GmbH,DE'],


  		Autonomous_System_Number = scrapy.Field() 
		Address_IP = scrapy.Field()  
		Autonomous_System_Number_CIDR = scrapy.Field() 
		Country_Code_Text = scrapy.Field() 
		Regional_Internet_Registries = scrapy.Field()

		Information_Text = scrapy.Field()




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




#scrapy crawl DYNAMIC_DNS_IPS1 -o DYNAMIC_DNS_IPS1.csv