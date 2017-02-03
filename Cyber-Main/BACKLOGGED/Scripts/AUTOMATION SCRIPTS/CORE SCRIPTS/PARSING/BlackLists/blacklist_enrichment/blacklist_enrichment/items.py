# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TestItem(scrapy.Item):
	Autonomous_System_Number = scrapy.Field() 
	Address_IP = scrapy.Field()  
	Autonomous_System_Number_CIDR = scrapy.Field() 
	Country_Code_Text = scrapy.Field() 
	Regional_Internet_Registries = scrapy.Field()
	Autonomous_System_Number_date = scrapy.Field()  
	Information_Text = scrapy.Field()

class MayhemListItem(scrapy.Item):
	Address_IP = scrapy.Field()
	Malware_Types_List = scrapy.Field()
	Domain_Name = scrapy.Field()
	Blacklist_Type_Text = scrapy.Field()

class GetCountriesItem(scrapy.Item):
	country = scrapy.Field()


	



class BlacklistEnrichmentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AntispamImpItem(scrapy.Item):
	Count_Number = scrapy.Field()
	Address_IP = scrapy.Field()
	Unix_Time = scrapy.Field()
	Local_Timestamp = scrapy.Field()
	Hits_Number = scrapy.Field()
	Host_Name_Text = scrapy.Field()


class TorIpResolutionItem(scrapy.Item):
    Source_Name = scrapy.Field()
    Router_Name = scrapy.Field()
    Bandwidth_in_kb = scrapy.Field()
    Up_Time_in_seconds = scrapy.Field()
    Host_Name_Text = scrapy.Field()
    Dir_Port_Text = scrapy.Field()
    OR_Port_Number = scrapy.Field()
    is_Bad_Exit = scrapy.Field()
    First_Seen_date = scrapy.Field()
    AS_Name_Text = scrapy.Field()
    AS_Number_Text = scrapy.Field()
    Autonomous_System_Number = scrapy.Field()
    Consensus_Bandwidth_in_kb = scrapy.Field()
    OR_Address_Text = scrapy.Field()
    ip_Text = scrapy.Field()
    Country_Name = scrapy.Field()
    Platform_Version_Number = scrapy.Field()
    Platform_Text = scrapy.Field()
    Exit_Node_Code = scrapy.Field()
    Date_Published_List_of_dates = scrapy.Field()
    Time_Published_List_of_times = scrapy.Field()
    Last_Status_Date_list_of_dates = scrapy.Field()
    Last_Status_Time_list_of_times = scrapy.Field()
    Exit_Address = scrapy.Field()
    Exit_Address_date = scrapy.Field()
    Exit_Address_time = scrapy.Field()
    Fingerprint_Code = scrapy.Field()
    Exit_url = scrapy.Field()
    is_Authority = scrapy.Field()
    is_Bad_Directory = scrapy.Field()
    is_Bad_Exit = scrapy.Field()
    is_Exit = scrapy.Field()
    is_Fast = scrapy.Field()
    is_Guard = scrapy.Field()
    is_Hibernating = scrapy.Field()
    is_Named = scrapy.Field()
    is_Stable = scrapy.Field()
    is_Running = scrapy.Field()
    is_Valid = scrapy.Field()
    is_V2Dir = scrapy.Field()
    is_Exit_Accept = scrapy.Field()
    is_Exit_Reject = scrapy.Field()
    Onion_Key_Code = scrapy.Field()
    Signing_Key_Code = scrapy.Field()
    Individual_Name = scrapy.Field()
    Individual_Email = scrapy.Field()
    Family_Members_list_of_codes = scrapy.Field()
    Descriptor_Publish_date = scrapy.Field()
    Descriptor_Publish_time = scrapy.Field()
    Bandwidth_Units = scrapy.Field()
    Site_Operator_Name = scrapy.Field()
    Inet_Num_range = scrapy.Field()
    Net_Name = scrapy.Field()
    Description_Text = scrapy.Field()
    Administrative_Contacts_List = scrapy.Field()
    Technical_Contacts_List = scrapy.Field()
    Status_Text = scrapy.Field()
    Maintainer_References_Text = scrapy.Field()
    Organisation_Text = scrapy.Field()
    Organisation_Name = scrapy.Field()
    Organisation_Type_Text = scrapy.Field()
    Postal_Address_List = scrapy.Field()
    Remarks_Text = scrapy.Field()
    mnt_ref_List = scrapy.Field()
    Abuse_Contact_Text = scrapy.Field()
    Person_Name = scrapy.Field()
    Node_Operator_Phone = scrapy.Field()
    Node_Operator_Fax = scrapy.Field()
    Nic_Handle_List = scrapy.Field()
    Route_Text = scrapy.Field()
    List_of_Origins = scrapy.Field()
    Member_Of_Text = scrapy.Field()
    Latitude_as_Single = scrapy.Field()
    Longitude_as_Single = scrapy.Field()
    Calling_Code = scrapy.Field()
    List_of_Currencies = scrapy.Field()
    Capital_Name = scrapy.Field()
    Region_Text = scrapy.Field()
    Language_Name = scrapy.Field()




class SSLExtendedItem(scrapy.Item):
	UTC_Listing_Timestamp = scrapy.Field()
	MD5_Referencing_Sample_Text = scrapy.Field()
	Destination_IP = scrapy.Field()	
	Destination_Port_Number = scrapy.Field()
	SSL_Certificate_SHA1_Fingerprint_Text = scrapy.Field()	
	Listing_Reason_Text = scrapy.Field()


class MalwareDomainList(scrapy.Item):
	UTC_Listing_Timestamp = scrapy.Field()
	Domain_url = scrapy.Field()
	Address_IP = scrapy.Field()
	Reverse_Lookup_url = scrapy.Field()
	Description_Text = scrapy.Field()
	Registrant_email = scrapy.Field()
	Autonomous_System_Number = scrapy.Field()
	Number = scrapy.Field()
	Country_Code_Text = scrapy.Field()
	Extra_test = scrapy.Field()

class BlacklistEnrichmentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SSLExtendedItem(scrapy.Item):
	UTC_Listing_Timestamp = scrapy.Field()
	MD5_Referencing_Sample_Text = scrapy.Field()
	Destination_IP = scrapy.Field()	
	Destination_Port_Number = scrapy.Field()
	SSL_Certificate_SHA1_Fingerprint_Text = scrapy.Field()	
	Listing_Reason_Text = scrapy.Field()


class MalwareDomainListItem(scrapy.Item):
	UTC_Listing_Timestamp = scrapy.Field()
	Domain_url = scrapy.Field()
	Address_IP = scrapy.Field()
	Reverse_Lookup_url = scrapy.Field()
	Description_Text = scrapy.Field()
	Registrant_email = scrapy.Field()
	Autonomous_System_Number = scrapy.Field()
	Number = scrapy.Field()
	Country_Code_Text = scrapy.Field()
	Extra_test = scrapy.Field()


class CyberCrimeTrackerItem(scrapy.Item):
	#Boolean values - check if there is a corresponding entry for the following
	#Corresponding entry data fields are listed under each boolean data field

	#COLUMN 1
	is_Spamhaus = scrapy.Field()
	#http://www.spamhaus.org/query/ip/104.232.3.33"
	is_SBL = scrapy.Field() #listed in SBL
	is_PBL = scrapy.Field() #listed in PBL
	is_XBL = scrapy.Field() #listed in XBL

	#COLUMN 2
	is_WhoIs = scrapy.Field()
	#"http://whois.domaintools.com/104.232.3.33"
	#need password to access this

	#COLUMN 3
	is_Geoiptool = scrapy.Field()
	#"http://www.geoiptool.com/fr/?IP=104.232.3.33" 
	# Hostname: 104.210.12.29
	# IP Address: 104.210.12.29
	# Country:   United States
	# Country Code: US (USA)
	# Region: Virginia
	# City: Boydton
	# Local time: 26 Feb 11:07 (EST-0500)  #convert to timestamp
	# Postal Code: 23917
	# Latitude: 36.6648
	# Longitude: -78.3715

	#COLUMN 4
	is_Robtex = scrapy.Field()
	#"http://www.robtex.com/dns/104.232.3.33.html" 

	#COLUMN 5
	is_BFK = scrapy.Field()
	#"http://www.bfk.de/bfk_dnslogger.html?query=104.232.3.33#result

	#COLUMN 6
	is_Web_Archive = scrapy.Field()
	#"http://web.archive.org/web/*/104.232.3.33"

	#COLUMN 7
	is_Siteadvisor = scrapy.Field()
	#"http://siteadvisor.com/lookup/?q=104.232.3.33"

	#COLUMN 8
	is_Toolbar_Netcraft = scrapy.Field()
	#"http://toolbar.netcraft.com/site_report?url=http://104.232.3.33"

	#COLUMN 9
	is_Zeustracker = scrapy.Field()
	#"https://zeustracker.abuse.ch/monitor.php?host=104.232.3.33"

	#COLUMN 10
	is_Plotip = scrapy.Field()
	#"http://www.plotip.com/domain/104.232.3.33"

	#COLUMN 11
	is_Virustotal = scrapy.Field()
	#"https://www.virustotal.com/en-gb/ip-address/104.232.79.22/information/"


class MayhemListItem(scrapy.Item):
	Address_IP = scrapy.Field()
	Malware_Types_List = scrapy.Field()
	Domain_Name = scrapy.Field()
	Blacklist_Type_Text = scrapy.Field()


class ManituPartnersItem(scrapy.Item):
	DNS_Configuration_Type_Text = scrapy.Field()
	DNS_Server_URL = scrapy.Field()
	IP_List = scrapy.Field()
	Provider_Name = scrapy.Field()
	Provider_Address = scrapy.Field()
	Provider_Telephone = scrapy.Field()
	Provider_Fax = scrapy.Field()
	Provider_Email = scrapy.Field()
	Provider_Website = scrapy.Field()

     
class IpWhoIsQueryItem(scrapy.Item):    #using IPWhois
	###MAIN DATA FIELDS###
	Autonomous_System_Number = scrapy.Field()  #: '57010',
	Autonomous_System_Number_Cidr_Text = scrapy.Field()  #': '62.76.184.0/21',
	Autonomous_System_Number_Country_Code_Text = scrapy.Field()  #': 'RU',
	Autonomous_System_Number_date = scrapy.Field()  #': '',
	Autonomous_System_Number_Registry_Text = scrapy.Field()   #': 'ripencc',
 
	Entities_List = scrapy.Field()  #': [u'AR23823-RIPE'],

	#7* 'network':

	Network_Cidr_IP = scrapy.Field()   #: '62.76.176.0/20',   => network_cidr
	Network_Country_Text = scrapy.Field()  # : u'RU',           => network_country
	Network_End_Address_IP = scrapy.Field()  #': '62.76.191.255', => network_end_address

	#7D**'events': 

	Network_Events_Action_Text = scrapy.Field()  #': u'last changed',  => network_events_action
	Network_Events_Actor_Text = scrapy.Field()  #': None, => network_events_actor
	Network_Events_Timestamp = scrapy.Field()  #': u'2014-07-04T12:18:11Z'}], =>  network_events_timestamp

	Network_Handle_IP_Range = scrapy.Field()  #': u'62.76.176.0 - 62.76.191.255', =>  network_handle
	Network_IP_Version_Text = scrapy.Field()  #': u'v4', => network_ip_version

	Network_Links_List = scrapy.Field()  #': [u'https://rdap.db.ripe.net/ip/62.76.186.48',   =>  network_links
	            #u'http://www.ripe.net/data-tools/support/documentation/terms'],
	Network_Name = scrapy.Field()  #': u'Clodo-Cloud',  => network_name
	             
	#7I**'notices': 

	Network_Notices_Description_Text = scrapy.Field()  #[{'description': u'This output has been filtered.',  => network_notices_description
	Network_Notices_Links_List = scrapy.Field()  #': None,  =>  network_notices_links
	Network_Notices_Title_Text = scrapy.Field()  #': u'Filtered'},  => network_notices_title  [list of dictionaries]
	                         

	Network_Parent_Handle_Text = scrapy.Field()  #': None,  => network_parent_handle
	Network_Raw = scrapy.Field()  #': None,  => network_raw

	###Network_Remarks_Text => contains a list of dictionaries###
	Network_Remarks_Description_Text = scrapy.Field()
	Network_Remarks_Links_List = scrapy.Field()
	Network_Remarks_Title_Text = scrapy.Field()

	Network_Start_Address_IP = scrapy.Field()  #': '62.76.176.0',  => network_start_address
	Network_Status_Text = scrapy.Field()  #': None,  => network_status
	Network_Type = scrapy.Field()  #': u'ASSIGNED PA'},  => network_type


	#8*'objects': 

	#8A**{u'AR23823-RIPE': 
	#8AA***{'contact': 
	#8AAA****{'address': 
	

	#replace with RIPE_Code
	Objects_RIPE_Code_Contact_Address_Type_Text = scrapy.Field()   #{'type': None,  => objects_AR23823-RIPE_contact_address_type
	Objects_RIPE_Code_Contact_Address = scrapy.Field()  #': u'7, Kalyazinskaya,\n194017, St. Petersburg'}],  => objects_AR23823-RIPE_contact_address_value

	#8AAB****'email': [list of dictionaries]

	Objects_RIPE_Code_Contact_Email_Type_Text = scrapy.Field()  #[{'type': None,  => objects_AR23823-RIPE_contact_email_type 
	Objects_RIPE_Code_Contact_Email = scrapy.Field()   #': u'admin@clodo.ru'},  =>  objects_AR23823-RIPE_contact_email_value

	                                           
	Objects_RIPE_Code_Kind_Text = scrapy.Field()  #: u'group',  =>  objects_AR23823-RIPE_kind
	Objects_RIPE_Code_Name = scrapy.Field()  #': u'Abuse-C Role',  => objects_AR23823-RIPE_name
	Objects_RIPE_Code_Phone = scrapy.Field()  #': None,  => objects_AR23823-RIPE_phone
	Objects_RIPE_Code_Role_Text = scrapy.Field()  #': None,  =>  objects_AR23823-RIPE_role
	Objects_RIPE_Code_Title_Text = scrapy.Field()  #': None},  => objects_AR23823-RIPE_title


	Objects_Entities_List = scrapy.Field()  #': [u'ITHOUSE-MNT', u'ROSNIIROS-MNT'],  [list]   => objects_entities
	Objects_Events = scrapy.Field()  #': None,  => objects_events
	Objects_Events_Actor_Text = scrapy.Field()  #': None,  =>  objects_events_actor
	Objects_Handle = scrapy.Field()  #': u'AR23823-RIPE',  => objects_handle
	Objects_Links_List = scrapy.Field()  #': None,  =>  objects_links
	Objects_Notices_List = scrapy.Field()  #': None,  =>  objects_notices
	Objects_Raw_Text = scrapy.Field()  #': None,  =>  objects_raw
	Objects_Remarks_Text = scrapy.Field()  #': None, =>  objects_remarks
	Objects_Roles_List = scrapy.Field()  #': [u'abuse'],  => objects_roles  [list]
	Objects_Status_Text = scrapy.Field()  #': None}},  =>  objects_status

	Query_IP = scrapy.Field()  #': '62.76.186.48',  => query
	Raw_Text = scrapy.Field()  #': None}  => raw


class WhoIsItem(scrapy.Item):
	updated_date = scrapy.Field()
	status = scrapy.Field()
	name = scrapy.Field()
	dnssec = scrapy.Field()
	city = scrapy.Field()
	expiration_date = scrapy.Field()
	zipcode = scrapy.Field()
	domain_name = scrapy.Field()
	country = scrapy.Field()
	whois_server = scrapy.Field()
	state = scrapy.Field()
	registrar = scrapy.Field()
	referral_url = scrapy.Field()
	address = scrapy.Field()
	name_servers = scrapy.Field()
	org = scrapy.Field()
	creation_date = scrapy.Field()
	emails = scrapy.Field()
	ip_Address_Text = scrapy.Field()
	Blacklist_Type_Name = scrapy.Field()


class NewBlacklistSchemaItem(scrapy.Item):

	#[red – compulsory]
	confidence_score = scrapy.Field()
	ipaddress = scrapy.Field() 
	ipaddress_int = scrapy.Field() 
	offenderclass = scrapy.Field()
	first_observed_date = scrapy.Field() 
	first_observed_time = scrapy.Field() 
	most_recent_observation_date = scrapy.Field() 
	most_recent_observation_time = scrapy.Field() 
	total_observations = scrapy.Field() 

	#[blue – pull out of datasources]
	countryabbrv = scrapy.Field() 
	country = scrapy.Field() 
	city = scrapy.Field()
	coordinates = scrapy.Field() 
	geo_longitude = scrapy.Field() 
	geo_latitude = scrapy.Field() 
	isp = scrapy.Field()
	domain = scrapy.Field() 
	netspeed = scrapy.Field() 
	network_asn = scrapy.Field() 
	network_class = scrapy.Field() 
	network_type = scrapy.Field()

	#[black – not essential]
	piplelineid = scrapy.Field()
	datauploadid = scrapy.Field()
	uuid = scrapy.Field()
	referential = scrapy.Field()
	datasourcename = scrapy.Field()
	date = scrapy.Field()
	cog = scrapy.Field() 
	model = scrapy.Field()
	concept = scrapy.Field() 
	segment = scrapy.Field() 
	pedigree = scrapy.Field()
	blranking = scrapy.Field() 
	threat_score = scrapy.Field()
	total_capabilities = scrapy.Field() 
	commvett = scrapy.Field() 
	commdatevett = scrapy.Field() 
	govvett = scrapy.Field() 
	govdatevett = scrapy.Field() 
	active_boolean = scrapy.Field()
	insrtdttm = scrapy.Field() 
	updtdttm = scrapy.Field() 


	# #[red – compulsory]
	# Confidence_Score_Number = scrapy.Field()
	# IP_Address_Text = scrapy.Field()   #
	# IP_Address_Int_Number = scrapy.Field() 
	# Offender_Class_Text = scrapy.Field() #?
	# First_Observed_date = scrapy.Field() #listing timestamp?
	# First_Observed_time = scrapy.Field() #listing timestamp?
	# Most_Recent_Observation_date = scrapy.Field() #listing timestamp?
	# Most_Recent_Observation_time = scrapy.Field() #listing timestamp?
	# Total_Observations_Number = scrapy.Field() 

	# #As,Ip_Adress,Bgp_Prefix,Country_Code,Registry,Listing_Timestamp,asn_Name

	# #[blue – pull out of datasources]  #do a whois query to get this info - using python query libraries
	# Country_Abbrv_Text = scrapy.Field()  #
	# Country_Name = scrapy.Field() 
	# City_Name = scrapy.Field() 
	# Coordinates_Text = scrapy.Field() #check these?
	# Geo_Longitude = scrapy.Field() 
	# Geo_Latitude = scrapy.Field() 
	# ISP_Text = scrapy.Field() 
	# Domain_Name = scrapy.Field() 
	# Net_Speed_Number = scrapy.Field() 
	# Network_Autonomous_System_Number = scrapy.Field() 
	# Network_Class_Text = scrapy.Field() 
	# Network_Type_Text = scrapy.Field() 

	# #[black – not essential]  explanations for these from client?
	# Pipleline_ID_Text = scrapy.Field()
	# Data_Upload_ID_Text = scrapy.Field()
	# UUID_Text = scrapy.Field()
	# Referential_Text = scrapy.Field()
	# Datasource_Name = scrapy.Field()
	# Date = scrapy.Field()
	# Cog = scrapy.Field()
	# Model = scrapy.Field() 
	# Concept = scrapy.Field()
	# Segment = scrapy.Field() 
	# Pedigree_Number = scrapy.Field() 
	# BL_Ranking_Number = scrapy.Field() 
	# Threat_Score_Number = scrapy.Field() 
	# Total_Capabilities = scrapy.Field() 
	# commvett = scrapy.Field() 
	# commdatevett = scrapy.Field() 
	# govvett = scrapy.Field() 
	# govdatevett = scrapy.Field() 
	# Active_Boolean = scrapy.Field()
	# insrtdttm = scrapy.Field()
	# updtdttm = scrapy.Field() 




	

    
    
    



