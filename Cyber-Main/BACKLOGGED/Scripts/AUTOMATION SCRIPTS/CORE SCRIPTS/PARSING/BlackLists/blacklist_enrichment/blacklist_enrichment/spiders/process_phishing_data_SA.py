# -*- coding: utf-8 -*-


import scrapy
import re
import json
import csv
import whois
import socket
from geopy.geocoders import Nominatim
geolocator = Nominatim
from ipwhois import IPWhois
from pprint import pprint
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from blacklist_enrichment.items import NewBlacklistSchemaItem


class ProcessPhishingSpider(CrawlSpider):
	name = "phishing1"
	#create list of keywords, and loop through searches here
	def start_requests(self):

		#Note: replace file path with your local filepath
		url  = 'file:///C:/Users/Seraphina/Desktop/John_Snow_Labs/JSL_OUTPUTS/11_3_2016/PHISHING_BL20160306.csv'   
		yield Request(url, callback=self.parse_file_url)



	def parse_file_url(self, response):
		get_url = response #this gets us current URL crawling!
		url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
	
		all_data = response.xpath('//*').extract()
		all_data = all_data[0]
		allrows = all_data.split('\r\n')
		cleanrows = [e.replace(re.match('.*?(<.*>).*', e).group(1), '') if re.match('.*?(<.*>).*', e) else e for e in allrows]
		allrows = cleanrows[1:]

		#asn = [re.match('\s*(\d{5}).*', e).group(1) if re.match('\s*(\d{5}).*', e) else '' for e in allrows]  #not needed

		#1 As, #not needed

		#2 Ip_Adress,
		ips = [re.match('\s*\d{5}\s*(\d+\.\d+\.\d+\.\d+)\s*.*', e).group(1) if re.match('\s*\d{5}(\d+\.\d+\.\d+\.\d+)\s*.*', e) else '' for e in allrows]
		#3 Bgp_Prefix, #not needed
		#4 Country_Code,
		country_code = [re.match('.*\d+\.\d+\.\d+\.(?:\d+)?\s*\.?\/?\d*\s*([A-Z]{2}).*', e).group(1) if re.match('.*\d+\.\d+\.\d+\.(?:\d+)?\s*\.?\/?\d*\s*([A-Z]{2}).*', e) else '' for e in allrows]
		#5 Registry, #not needed
		#6 Listing_Timestamp,  #divide into (a) time, (b) date
		date = [re.match('.*?(\d{4}-\d{2}-\d{2}).*', e).group(1) if re.match('.*?(\d{4}-\d{2}-\d{2}).*', e) else '' for e in allrows]
		#listing_date = []  #need original datasource
		#7 asn_Name #not needed
		

		for i, e in enumerate(ips):

			item = NewBlacklistSchemaItem()


			try:
				item['confidence_score'] = ''
			except:
				item['confidence_score'] = ''
			try:
				item['ipaddress'] = ips[i]
			except:
				item['ipaddress'] = ''
			try:
				item['ipaddress_int'] = ''
			except:
				item['ipaddress_int'] = ''
			try:
				item['offenderclass'] = ''
			except:
				item['offenderclass'] = ''
			try:
				item['first_observed_date'] = ''
			except:
				item['first_observed_date'] = ''
			try:
				item['most_recent_observation_date'] = date[i]
			except:
				item['most_recent_observation_date'] = ''
			try:
				item['most_recent_observation_time'] = ''
			except:
				item['most_recent_observation_time'] = ''
			try:
				item['total_observations'] = ''
			except:
				item['total_observations'] = ''


			#BLUE
			try:
				item['countryabbrv'] = country_code[i]
			except:
				item['countryabbrv'] = ''
			try:
				item['country'] = ''
			except:
				item['country'] = ''
			try:
				item['city'] = ''
			except:
				item['city'] = ''
			try:
				item['coordinates'] = ''
			except:
				item['coordinates'] = ''
			try:
				item['geo_longitude'] = ''
			except:
				item['geo_longitude'] = ''
			try:
				item['geo_latitude'] = ''
			except:
				item['geo_latitude'] = ''
			try:
				item['isp'] = ''
			except:
				item['isp'] = ''
			try:
				item['domain'] = ''
			except:
				item['domain'] = ''
			try:
				item['netspeed'] = ''
			except:
				item['netspeed'] = ''
			try:
				item['network_asn'] = ''
			except:
				item['network_asn'] = ''
			try:
				item['network_class'] = ''
			except:
				item['network_class'] = ''
			try:
				item['network_type'] = ''
			except:
				item['network_type'] = ''

			try:
				item['piplelineid'] = ''
				item['datauploadid'] = ''
				item['uuid'] = ''
				item['referential'] = ''
				item['datasourcename'] = ''
				item['date'] = ''
				item['cog'] = '' 
				item['model'] = ''
				item['concept'] = '' 
				item['segment'] = '' 
				item['pedigree'] = ''
				item['blranking'] = '' 
				item['threat_score'] = ''
				item['total_capabilities'] = '' 
				item['commvett'] = '' 
				item['commdatevett'] = '' 
				item['govvett'] = '' 
				item['govdatevett'] = '' 
				item['active_boolean'] = ''
				item['insrtdttm'] = '' 
				item['updtdttm'] = ''
			except:
				item['piplelineid'] = ''
				item['datauploadid'] = ''
				item['uuid'] = ''
				item['referential'] = ''
				item['datasourcename'] = ''
				item['date'] = ''
				item['cog'] = '' 
				item['model'] = ''
				item['concept'] = '' 
				item['segment'] = '' 
				item['pedigree'] = ''
				item['blranking'] = '' 
				item['threat_score'] = ''
				item['total_capabilities'] = '' 
				item['commvett'] = '' 
				item['commdatevett'] = '' 
				item['govvett'] = '' 
				item['govdatevett'] = '' 
				item['active_boolean'] = ''
				item['insrtdttm'] = '' 
				item['updtdttm'] = ''

			yield item


			







	
			# #RED
			# try:
			# 	item['Confidence_Score_Number'] = ''
			# except:
			# 	item['Confidence_Score_Number'] = ''
			# try:
			# 	item['IP_Address_Text'] = ips[i]
			# except:
			# 	item['IP_Address_Text'] = ''
			# try:
			# 	item['IP_Address_Int_Number'] = ''
			# except:
			# 	item['IP_Address_Int_Number'] = ''
			# try:
			# 	item['Offender_Class_Text'] = ''
			# except:
			# 	item['Offender_Class_Text'] = ''
			# try:
			# 	item['First_Observed_date'] = ''
			# except:
			# 	item['First_Observed_date'] = ''
			# try:
			# 	item['Most_Recent_Observation_date'] = date[i]
			# except:
			# 	item['Most_Recent_Observation_date'] = ''
			# try:
			# 	item['Most_Recent_Observation_time'] = ''
			# except:
			# 	item['Most_Recent_Observation_time'] = ''
			# try:
			# 	item['Total_Observations_Number'] = ''
			# except:
			# 	item['Total_Observations_Number'] = ''


			# #BLUE
			# try:
			# 	item['Country_Abbrv_Text'] = country_code[i]
			# except:
			# 	item['Country_Abbrv_Text'] = ''
			# try:
			# 	item['Country_Name'] = ''
			# except:
			# 	item['Country_Name'] = ''
			# try:
			# 	item['City_Name'] = ''
			# except:
			# 	item['City_Name'] = ''
			# try:
			# 	item['Coordinates_Text'] = ''
			# except:
			# 	item['Coordinates_Text'] = ''
			# try:
			# 	item['Geo_Longitude'] = ''
			# except:
			# 	item['Geo_Longitude'] = ''
			# try:
			# 	item['Geo_Latitude'] = ''
			# except:
			# 	item['Geo_Latitude'] = ''
			# try:
			# 	item['ISP_Text'] = ''
			# except:
			# 	item['ISP_Text'] = ''
			# try:
			# 	item['Domain_Name'] = ''
			# except:
			# 	item['Domain_Name'] = ''
			# try:
			# 	item['Net_Speed_Number'] = ''
			# except:
			# 	item['Net_Speed_Number'] = ''
			# try:
			# 	item['Network_Autonomous_System_Number'] = ''
			# except:
			# 	item['Network_Autonomous_System_Number'] = ''
			# try:
			# 	item['Network_Class_Text'] = ''
			# except:
			# 	item['Network_Class_Text'] = ''
			# try:
			# 	item['Network_Type_Text'] = ''
			# except:
			# 	item['Network_Type_Text'] = ''
	

			#yield item



#scrapy crawl phishing1 -o PHISHING_BL20160311.csv