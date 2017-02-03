# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

###add example for each data field###

import scrapy

class SearchLinksItem(scrapy.Item):
    resultUrl = scrapy.Field()
    resultText = scrapy.Field()
    title = scrapy.Field()
    #counter = scrapy.Field()  #for internal use




class TorIpResolutionItem(scrapy.Item):
    Source_Name = scrapy.Field()
    Router_Name = scrapy.Field()
    Bandwidth_in_kb = scrapy.Field()
    Up_Time_in_seconds = scrapy.Field()
    Host_Name = scrapy.Field()
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
    Platform_Version_Text = scrapy.Field()
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
  


    



class MetaDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    dateModified = scrapy.Field()
    communities = scrapy.Field()
    memo = scrapy.Field()
    dataSourceKind = scrapy.Field()
    dataSourceLink = scrapy.Field()
    dateCreate = scrapy.Field()
    dataSourceScript = scrapy.Field()
    countries = scrapy.Field()
    otherReqt = scrapy.Field()
    password = scrapy.Field()
    ipToRange = scrapy.Field()
    sourceName = scrapy.Field()
    ipFrom = scrapy.Field()
    userName = scrapy.Field()
    longitude = scrapy.Field()
    pedigrees = scrapy.Field()
    portNumber = scrapy.Field()
    host = scrapy.Field()
    dataSourceKinds = scrapy.Field()
    dataTypes = scrapy.Field()
    places = scrapy.Field()
    persons = scrapy.Field()
    dataSourceDesc = scrapy.Field()
    ipFromRange = scrapy.Field()
    images = scrapy.Field()
    categories = scrapy.Field()
    things = scrapy.Field()
    latitude = scrapy.Field()
    isActive = scrapy.Field()   
    #pass

    

