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


#file:///home/sagi/html_files


class WhoIsSpider(CrawlSpider):
	name = "tidy_data"
	#create list of keywords, and loop through searches here
	def start_requests(self):

		###############################
		###for single source datasets##     
		###############################

		url  = 'file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/6_3_2016/WHOIS_DATA/DNS_BL_domains201603032016.csv'   #ipBlacklist6.csv
		yield Request(url, callback=self.parse_file_url)



	def parse_file_url(self, response):
		get_url = response #this gets us current URL crawling!
		url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
		#i.e. here, we have: <200 file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/6_3_2016/WHOIS_DATA/DNS_BL_domains201603032016.csv>


		all_data = response.xpath('//*').extract()
		all_data = all_data[0]
		allrows = all_data.split('\r\n')


		getcells = [e.split(' ') for e in allrows]

		cleancells = [[f for f in e if f != ''] for e in getcells if e != '']
		cleancells = [[f.replace(re.match('.*?([,]+).*', f).group(1), '') if re.match('.*?([,]+).*', f) else f for f in e] for e in cleancells if e != '']

		data = cleancells

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




#Overall length of data: 15207

























