# -*- coding: utf-8 -*-

import scrapy
import re
import json
import csv
import pycountry
from ipwhois import IPWhois
from pprint import pprint
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from blacklist_enrichment.items import GetCountriesItem


class WhoIsSpider(CrawlSpider):
	name = "get_countries"
	#create list of keywords, and loop through searches here
	def start_requests(self):

		###############################
		###for single source datasets##     
		###############################

		#url = 'file:///c:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/16_3_2016/codes1.txt'   #ipBlacklist6.csv
		url = 'file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/16_3_2016/codes1.txt' 
		#url = 'file:///C:/Users/Seraphina/john-snow-labs-version-control/cyber/CORE SCRIPTS/PARSING/BlackLists/blacklist_enrichment/codes1.txt'
		yield Request(url, callback=self.parse_file_url)



	def parse_file_url(self, response):
		item = GetCountriesItem()
		#get_url = response #this gets us current URL crawling!
		#url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
		#i.e. here, we have: <200 file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/6_3_2016/WHOIS_DATA/DNS_BL_domains201603032016.csv>
		
		all_data = response.xpath('//*').extract()
		all_data = all_data[0]
		allrows = all_data.split('\r\n')
		allrows = allrows[1:]
		getcells = [e.split(',') for e in allrows]

		getcodes = []
		countries = []

		for e in getcells:
			
			for i, f in enumerate(e):
				if i == 27:
					getcodes.append(f)
					print e
				
			#return getcodes


		#process country codes
		
		for code in getcodes:
			
			try:
				result = pycountry.countries.get(alpha2=str(code))
				country = result.name
				print country
				item['country'] = country
				
			except:
				item['country'] = ''
				
			yield item

			#countries.append(country)
			#print countries
			#return countries
			

		# for j, f in enumerate(countries):
		# 	item = GetCountriesItem()
		# 	print countries[j]
		# 	item['country'] = countries[j]
		# 	print countries[j]
    		


    	
    		
    		
    		

    		


		
