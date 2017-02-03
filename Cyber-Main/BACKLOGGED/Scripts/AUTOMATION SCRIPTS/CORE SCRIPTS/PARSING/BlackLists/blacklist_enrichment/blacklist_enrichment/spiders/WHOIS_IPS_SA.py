###script to generate WhoIs data, Seraphina Anderson, John Snow Labs, 26/2/2016###

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
from blacklist_enrichment.items import IpWhoIsQueryItem


class WhoIsSpider(CrawlSpider):
	name = "whois_ips"
	#create list of keywords, and loop through searches here
	def start_requests(self):

		###############################
		###for single source datasets##     
		###############################

		url  = 'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist'   #ipBlacklist6.csv
		yield Request(url, callback=self.parse_ip_blacklist_url)

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
			
		

	def parse_ip_blacklist_url(self, response):
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



		
		stuff = response.xpath('//body').extract()
		#add arguments if data structure varies
		data = stuff[0].split(re.match('.*?(\\n).*', stuff[0]).group(1))

		###IMPLEMENT TESTS HERE FOR VARIATION  IN UNSTRUCTURED DATA###
		
		#ipAddress = [re.match('.*?\\t(\d+\.\d+\.\d+\.\d+).*', e).group(1) if re.match('.*?\\t(\d+\.\d+\.\d+\.\d+).*', e) else re.match('\d+\.\d+\.\d+\.\d+', e).group(0) for e in data]
		ipAddress = [re.match('.*?(?:\\t)?(\d+\.\d+\.\d+\.\d+).*', e).group(1) for e in data if re.match('.*?(?:\\t)?(\d+\.\d+\.\d+\.\d+).*', e)]

		#check for publish date - listingDate - update as appropriate
		date = [re.match('.*?L?l?ast\s*U?u?pdated\s*:?\s*(\d{4}-\d{2}-\d{2}).*', e).group(1) for e in data if re.match('.*?L?l?ast\s*U?u?pdated\s*:?\s*(\d{4}-\d{2}-\d{2}).*', e)]

		n = 0

		for e in ipAddress:
			item = IpWhoIsQueryItem()
			ip = ipAddress[n]
			obj = IPWhois(str(ip))
			results = obj.lookup_rdap(depth=1)

			n += 1



			if 'asn' in results.keys():
				item['Autonomous_System_Number'] = results['asn']

			if 'asn_cidr' in results.keys():
				item['Autonomous_System_Number_Cidr_Text'] = results['asn_cidr']

			if 'asn_country_code' in results.keys():
				item['Autonomous_System_Number_Country_Code_Text'] = results['asn_country_code']

			if 'asn_date' in results.keys():
				item['Autonomous_System_Number_date'] = results['asn_date']

			if 'asn_registry' in results.keys():
				item['Autonomous_System_Number_Registry_Text'] = results['asn_registry']

			if 'entities' in results.keys():
				item['Entities_List'] = results['entities']

			if 'cidr' in results['network'].keys():
				item['Network_Cidr_IP'] = results['network']['cidr']

			if 'country' in results['network'].keys():
				item['Network_Country_Text'] = results['network']['country']

			if 'end_address' in results['network'].keys():
				item['Network_End_Address_IP'] = results['network']['end_address']

			

			action = []
			actor = []
			timestamp = []

			for i, e in enumerate(results['network']['events']):

				if 'action' in results['network']['events'][i].keys():
					value = results['network']['events'][i]['action']
					action.append(value)
				else:
					action.append('')

				if 'actor' in results['network']['events'][i].keys():
					value = results['network']['events'][i]['actor']
					actor.append(value)
				else:
					actor.append('')

				if 'timestamp' in results['network']['events'][i].keys():
					value = results['network']['events'][i]['timestamp']
					timestamp.append(value)
				else:
					timestamp.append('')
					
				
					

				

			item['Network_Events_Action_Text'] = action
			item['Network_Events_Actor_Text'] = actor
			item['Network_Events_Timestamp'] = timestamp


			if 'handle' in results['network'].keys():
				item['Network_Handle_IP_Range'] = results['network']['handle']

			if 'ip_version' in results['network'].keys():  #nested *
				item['Network_IP_Version_Text'] = results['network']['ip_version']

			if 'links' in results['network'].keys():  #nested *
				item['Network_Links_List'] = results['network']['links']

			if 'name' in results['network'].keys():  #nested *
				item['Network_Name'] = results['network']['name']



						 
			#7I**'notices': list of dictionaries

			description = []
			links = []
			title = []
			for j, f in enumerate(results['network']['notices']):
				if 'description' in results['network']['notices'][j].keys():
					value = results['network']['notices'][j]['description']
					description.append(value)
				else:
					description.append('')
				if 'links' in results['network']['notices'][j].keys():
					value = results['network']['notices'][j]['links']
					links.append(value)
				else:
					links.append('')
				if 'title' in results['network']['notices'][j].keys():
					value = results['network']['notices'][j]['title']
					title.append(value)
				else:
					title.append('')

			
			item['Network_Notices_Description_Text'] = description  #[{'description': u'This output has been filtered.',  => network_notices_description
			item['Network_Notices_Links_List'] = links  #': None,  =>  network_notices_links
			item['Network_Notices_Title_Text'] = title  #': u'Filtered'},  => network_notices_title  [list of dictionaries]
			  

			if 'parent_handle' in results['network'].keys():
				item['Network_Parent_Handle_Text'] = results['network']['parent_handle']  #': None,  => network_parent_handle
			if 'raw' in results['network'].keys():
				item['Network_Raw'] = results['network']['raw']  #': None,  => network_raw

			# if 'remarks' in results['network'].keys():
			# 	item['Network_Remarks_Text'] = results['network']['remarks']  #': None,  => network_remarks

			#contains a list of dictionaries: results['network']['remarks'][0].keys()
			#results['network']['remarks'][m]
			
			description = []
			links = []
			title = []

			for m, o in enumerate(results['network']['notices']):
				if 'description' in results['network']['remarks'][m].keys():
					value = results['network']['remarks'][m]['description']
					description.append(value)
				else:
					description.append('')
				if 'links' in results['network']['remarks'][m].keys():
					value = results['network']['remarks'][m]['links']
					links.append(value)
				else:
					links.append('')
				if 'title' in results['network']['remarks'][m].keys():
					value = results['network']['remarks'][m]['title']
					title.append(value)
				else:
					title.append('')

			item['Network_Remarks_Description_Text'] = description
			item['Network_Remarks_Links_List'] = links
			item['Network_Remarks_Title_Text'] = title


			if 'start_address' in results['network'].keys():
				item['Network_Start_Address_IP'] = results['network']['start_address']  #': '62.76.176.0',  => network_start_address
			if 'status' in results['network'].keys():
				item['Network_Status_Text'] = results['network']['status']  #': None,  => network_status
			if 'type' in results['network'].keys():
				item['Network_Type'] = results['network']['type']  #': u'ASSIGNED PA'},  => network_type


			#8*'objects': 

			#8A**{u'AR23823-RIPE': 
			#8AA***{'contact': 
			#8AAA****{'address': 
			address_type = []
			value = []
			if 'AR23823-RIPE' in results['objects'].keys():
				for k, g in enumerate(results['objects']['AR23823-RIPE']['contact']['address']):
					if 'type' in results['objects']['AR23823-RIPE']['contact']['address'][k].keys():
						entry = results['objects']['AR23823-RIPE']['contact']['address'][k]['type']
						address_type.append(entry)
					else:
						address_type.append('')
					if 'value' in results['objects']['AR23823-RIPE']['contact']['address'][k].keys():
						entry = results['objects']['AR23823-RIPE']['contact']['address'][k]['value']
						value.append(entry)
					else:
						value.append('')

				item['Objects_RIPE_Code_Contact_Address_Type_Text'] = address_type   #{'type': None,  => objects_AR23823-RIPE_contact_address_type
				item['Objects_RIPE_Code_Contact_Address'] = value  #': u'7, Kalyazinskaya,\n194017, St. Petersburg'}],  => objects_AR23823-RIPE_contact_address_value



			address_type = []
			value = []
			if 'AR23823-RIPE' in results['objects'].keys():
				if re.match('\w{2}\d{5}',keys[0]):
					Ripe_Code_Text = re.match('\w{2}\d{5}',keys[0]).group(0)
					for l, h in enumerate(results['objects']['AR23823-RIPE']['contact']['email']):
						if 'type' in results['objects']['AR23823-RIPE']['contact']['email'][l].keys():
							entry = results['objects']['AR23823-RIPE']['contact']['email'][l]['type']
							address_type.append(entry)
						else:
							address_type.append('')
						if 'value' in results['objects']['AR23823-RIPE']['contact']['email'][l].keys():
							entry = results['objects']['AR23823-RIPE']['contact']['email'][l]['value']
							value.append(entry)
						else:
							value.append('')


				item['Objects_RIPE_Code_Contact_Email_Type_Text'] = address_type  #[{'type': None,  => objects_AR23823-RIPE_contact_email_type 
				item['Objects_RIPE_Code_Contact_Email'] = value   #': u'admin@clodo.ru'},  =>  objects_AR23823-RIPE_contact_email_value

	                                           

			if 'AR23823-RIPE' in results['objects'].keys():

				if 'kind' in results['objects']['AR23823-RIPE']['contact'].keys():                               
					item['Objects_RIPE_Code_Kind_Text'] = results['objects']['AR23823-RIPE']['contact']['kind']  #: u'group',  =>  objects_AR23823-RIPE_kind
				if 'name' in results['objects']['AR23823-RIPE']['contact'].keys():
					item['Objects_RIPE_Code_Name'] = results['objects']['AR23823-RIPE']['contact']['name']  #': u'Abuse-C Role',  => objects_AR23823-RIPE_name
				if 'phone' in results['objects']['AR23823-RIPE']['contact'].keys():
					item['Objects_RIPE_Code_Phone'] = results['objects']['AR23823-RIPE']['contact']['phone']  #': None,  => objects_AR23823-RIPE_phone
				if 'role' in results['objects']['AR23823-RIPE']['contact'].keys():
					item['Objects_RIPE_Code_Role_Text'] = results['objects']['AR23823-RIPE']['contact']['role'] #': None,  =>  objects_AR23823-RIPE_role
				if 'title' in results['objects']['AR23823-RIPE']['contact'].keys():
					item['Objects_RIPE_Code_Title_Text'] = results['objects']['AR23823-RIPE']['contact']['title'] #': None},  => objects_AR23823-RIPE_title




				if 'entities' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Entities_List'] = results['objects']['AR23823-RIPE']['entities']  #': [u'ITHOUSE-MNT', u'ROSNIIROS-MNT'],  [list]   => objects_entities
				if 'events' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Events'] = results['objects']['AR23823-RIPE']['events']  #': None,  => objects_events
				if 'events_actor' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Events_Actor_Text'] = results['objects']['AR23823-RIPE']['events_actor'] #': None,  =>  objects_events_actor
				if 'handle' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Handle'] = results['objects']['AR23823-RIPE']['handle'] #': u'AR23823-RIPE',  => objects_handle
				if 'links' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Links_List'] = results['objects']['AR23823-RIPE']['links'] #': None,  =>  objects_links
				if 'notices' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Notices_List'] = results['objects']['AR23823-RIPE']['notices'] #': None,  =>  objects_notices
				if 'raw' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Raw_Text'] = results['objects']['AR23823-RIPE']['raw']#': None,  =>  objects_raw
				if 'remarks' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Remarks_Text'] = results['objects']['AR23823-RIPE']['remarks'] #': None, =>  objects_remarks
				if 'roles' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Roles_List'] = results['objects']['AR23823-RIPE']['roles'] #': [u'abuse'],  => objects_roles  [list]
				if 'status' in results['objects']['AR23823-RIPE'].keys():
					item['Objects_Status_Text'] = results['objects']['AR23823-RIPE']['status']  #': None}},  =>  objects_status


			if 'query' in results.keys():
				item['Query_IP'] = results['query']  #': '62.76.186.48',  => query
			if 'raw' in results.keys():
				item['Raw_Text'] = results['raw']  #': None}  => raw
		   
			yield item 
			i += 1


			#scrapy crawl whois_ips -o whois_ips3_SA.csv


