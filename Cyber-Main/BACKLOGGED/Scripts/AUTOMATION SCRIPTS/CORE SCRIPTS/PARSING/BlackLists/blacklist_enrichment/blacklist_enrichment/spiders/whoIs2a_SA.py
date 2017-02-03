#Seraphina Anderson, John Snow Labs, 16/1/2016

#Spider for generating WhoIs URLs and scraping the corresponding data

# -*- coding: utf-8 -*-
import scrapy
import re
import json
import csv
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from blacklist_enrichment.items import TorIpResolutionItem



class TorWhoIs(CrawlSpider):

    name = "toripres_2"
    
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #loop through different urls, for IP addresses
        urls = ['https://torstatus.blutmagie.de']
        #https://check.torproject.org/exit-addresses  #start with this one
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_startingpoint)
            i += 1
        

    def parse_startingpoint(self, response):
        ###CREATE ITEM CONTAINER###
        dataRow = response.xpath('//tr[@class="r"]').extract()
        dataRow.remove(dataRow[0])


        ###generate item containers#################
        dataRow = [e.split('<td ') for e in dataRow]

        ip = [re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]).group(1) if re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]) else '' for k, e in enumerate(dataRow)]
        routerName = [re.match('.*>(.*?)<\/a><\/td>', dataRow[k][1]).group(1) if re.match('.*>(.*?)<\/a><\/td>', dataRow[k][1]) else '' for k, e in enumerate(dataRow)]
        #bandwidth
        bandwidth = [re.match('.*title="(.*?)">', dataRow[k][2]).group(1) if re.match('.*title="(.*?)">', dataRow[k][2]) else '' for k, e in enumerate(dataRow)]
        
        #upTimeSeconds
        uptime = [re.match('.*>(.*?)<\/td>', dataRow[k][4]).group(1) if re.match('.*>(.*?)<\/td>', dataRow[k][4]).group(1) else '' for k, e in enumerate(dataRow)]
        nums = [re.match('.*?(\d+).*', e).group(1) for e in uptime if re.match('.*?(\d+).*', e)]
        units = [re.match('.?\d+\s*?(\w+).*', e).group(1) if re.match('.?\d+\s*?(\w+).*', e) else '' for e in uptime]
        #test = [e for e in uptime if not re.match('\d+\s*?(\w+).*', e)]  #this gets anomaly
        #units = [re.match('\d+\s*?(\w+).*', e).group(1) if re.match('\d+\s*?(\w+).*', e) else '' for e in uptime]
        d = int(24*60*60)
        h = int(60*60)
        try:
            upTimeSeconds = [int(nums[i])*d if units[i] == 'd' else int(nums[i])*h for i, e in enumerate(uptime)]
        except:
            upTimeSeconds = ''


        #hostName
        hostName = [re.match('.*?class="iT">(.*?)\s*\[.*', dataRow[k][6]).group(1) if re.match('.*?class="iT">(.*?)\s*\[.*', dataRow[k][6]) else '' for k, e in enumerate(dataRow)]
        #ip
        ip = [re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]).group(1) if re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]) else '' for k, e in enumerate(dataRow)]
        #orPort
        orPort = ['' if dataRow[k][7] is None else re.match('.*>(\d+)<\/.*', dataRow[k][7]).group(1) for k, e in enumerate(dataRow)]
        #dirPort
        dirPort = ['' if not re.match('.*?(\d+).*', dataRow[k][8]) else re.match('.*?(\d+).*', dataRow[k][8]).group(1) for k, e in enumerate(dataRow)]
        #firstSeen
        firstSeen = [re.match('.*?>(\d{4}-\d{2}-\d{2}).*', dataRow[k][10]).group(1) if re.match('.*?>(\d{4}-\d{2}-\d{2}).*', dataRow[k][10]) else  '' for k, e in enumerate(dataRow)]
        #asName
        asName = [re.match('.*>(.*?)(?:<\/b>)?\/td>', dataRow[k][11]).group(1) if re.match('.*>(.*?)(?:<\/b>)?\/td>', dataRow[k][11]) else '' for k, e in enumerate(dataRow)]
        #asNumber
        asNumber = [re.match('.*?(\d+).*', dataRow[k][12]).group(1) if re.match('.*?(\d+).*', dataRow[k][12]) else '' for k, e in enumerate(dataRow)]
        #consensusBandwidth
        consensusBandwidth = [re.match('.*?(\d+).*', dataRow[k][13]).group(1) if re.match('.*?(\d+).*', dataRow[k][13]) else '' for k, e in enumerate(dataRow)]
        #orAddress
        orAddress = [re.match('.*?(\[.*?\]\s*:\s*\d+).*', dataRow[k][14]).group(1) if re.match('.*?(\[.*?\]\s*:\s*\d+).*', dataRow[k][14]) else '' for k, e in enumerate(dataRow)]

        ###LOOP THROUGH DATA FIELDS TO POPULATE ROWS FOR EACH DATA ITEM###
        i = 0
        while i < len(ip):
            item = TorIpResolutionItem()
            ###GENERATE WHOIS URLS###
            url = 'http://whois.ipchecker.info/' + str(ip[i])
            item['ip_Text'] = ip[i] #parse this itemfield
            item['Router_Name'] = routerName[i]
            item['Bandwidth_in_kb'] = bandwidth[i]
            try:
                item['Up_Time_in_seconds'] = upTimeSeconds[i]
            except:
                item['Up_Time_in_seconds'] = ''
            
            item['Host_Name_Text'] = hostName[i]
            item['OR_Port_Number'] = orPort[i]
            item['Dir_Port_Text'] = dirPort[i]
            item['First_Seen_date'] = firstSeen[i]
            item['AS_Name_Text'] = asName[i]
            item['Autonomous_System_Number'] = asNumber[i]
            item['Consensus_Bandwidth_in_kb'] = consensusBandwidth[i]
            item['OR_Address_Text'] = orAddress[i]
            yield Request(url, callback=self.parse_whois_data, meta=dict(item=item))
            i += 1

    
    def parse_whois_data(self, response):
        item = response.meta['item']
        
##        ###TEST FUNCTIONALITY - return corresponding url###
##        get_url = response #this gets us current URL crawling!
##        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
##        item['whoIs'] = url
        ###TEST FOR "INTERNAL SERVER ERROR"###
        #<h1>Internal Server Error</h1>


        #get LHS data
        results = response.xpath('//pre1').extract()
        if response.xpath('//pre1').re('.*?inetnum:\s*(.*)'):
            item['Inet_Num_range'] = response.xpath('//pre1').re('.*?inetnum:\s*(.*)')
            #inetNum = str(inetNum[0])

        if response.xpath('//pre1').re('.*?netname:\s*(.*)'):
            item['Net_Name'] = response.xpath('//pre1').re('.*?netname:\s*(.*)')
            #netName = str(netName[0])

        if response.xpath('//pre1').re('.*?descr:\s*(.*)'):
            item['Description_Text'] = response.xpath('//pre1').re('.*?descr:\s*(.*)')
            #description = str(description[0])

        if response.xpath('//pre1').re('.*?admin-?c:\s*(.*)'):
            item['Administrative_Contacts_List'] = response.xpath('//pre1').re('.*?admin-?c:\s*(.*)')
            #adminc = str(adminc[0])

        if response.xpath('//pre1').re('.*?tech-?c:\s*(.*)'):
            item['Technical_Contacts_List'] = response.xpath('//pre1').re('.*?tech-?c:\s*(.*)')
            #techc = str(techc[0])

        if response.xpath('//pre1').re('.*?status:\s*(.*)'):
            item['Status_Text'] = response.xpath('//pre1').re('.*?status:\s*(.*)')
            #status = str(status[0])

        if response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)'):
            item['Maintainer_References_Text'] = response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)')
            #mntby = str(mntby[0])

        if response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*'):
            item['Date_Published_List_of_dates'] = response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*')  #created
            #datePublished = str(datePublished[0])

        if response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
            item['Time_Published_List_of_times'] = response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
            #timePublished = str(timePublished[0])

        if response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*'):
            item['Last_Status_Date_list_of_dates'] = response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*') #last-modified
            #lastStatusDate = str(lastStatusDate[0])

        if response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
            item['Last_Status_Time_list_of_times'] = response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
            #lastStatusTime = str(lastStatusTime[0])

        if response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)'):
            item['Organisation_Text'] = response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)')
            #organisation = str(organisation[0])

        if response.xpath('//pre1').re('.*?org-name:\s*(.*)'):
            orgName = response.xpath('//pre1').re('.*?org-?name:\s*(.*)')
            item['Organisation_Name'] = orgName #str(orgName[0])

        if response.xpath('//pre1').re('.*?org-type:\s*(.*)'):
            orgType = response.xpath('//pre1').re('.*?org-?type:\s*(.*)')
            item['Organisation_Type_Text'] = orgType#str(orgType[0])

        if response.xpath('//pre1').re('.*?remarks:\s*(.*)'):
            remarks = response.xpath('//pre1').re('.*?remarks:\s*(.*)')
            item['Remarks_Text'] = remarks #str(remarks[0])

        if response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)'):
            mntRef = response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)')
            item['mnt_ref_List'] = mntRef#str(mntRef[0])

        if response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)'):
            abuseC = response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)')
            item['Abuse_Contact_Text'] = abuseC #str(abuseC[0])

        if response.xpath('//pre1').re('.*?person:\s*(.*)'):
            person = response.xpath('//pre1').re('.*?person:\s*(.*)')
            item['Person_Name'] = person#str(person[0])

        if response.xpath('//pre1').re('.*?address:\s*(.*)'):
            postalAddress = response.xpath('//pre1').re('.*?address:\s*(.*)')
            item['Postal_Address_List'] = [str(e) for e in postalAddress]

        if response.xpath('//pre1').re('.*?phone:\s*(.*)'):
            phone = response.xpath('//pre1').re('.*?phone:\s*(.*)')
            item['Node_Operator_Phone'] = [str(e) for e in phone]

        if response.xpath('//pre1').re('.*?fax-?no:\s*(.*)'):
            faxNo = response.xpath('//pre1').re('.*?fax-?no:\s*(.*)')
            item['Node_Operator_Fax'] = [str(e) for e in faxNo]

        if response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)'):
            nicHdl = response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)')
            item['Nic_Handle_List'] = [str(e) for e in nicHdl]

        if response.xpath('//pre1').re('.*?route:\s*(.*)'):
            route = response.xpath('//pre1').re('.*?route:\s*(.*)')
            item['Route_Text'] = route#str(route[0])

        if response.xpath('//pre1').re('.*?origin:\s*(.*)'):
            origin = response.xpath('//pre1').re('.*?origin:\s*(.*)')
            item['List_of_Origins'] = origin#str(origin[0])

        if response.xpath('//pre1').re('.*?member-?of:\s*(.*)'):
            memberOf = response.xpath('//pre1').re('.*?member-?of:\s*(.*)')
            item['Member_Of_Text'] = memberOf#str(memberOf[0])


        ###IP LOCATION###
        #get all location info
        location = response.xpath('//div[@class="span6"]//p//text()').extract()
        #populate data fields
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)'):
            item['Country_Name'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)')

        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)'):
            latitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)')
            item['Latitude_as_Single'] = str(latitude[0])

        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)'):
            longitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)')
            item['Longitude_as_Single'] = str(longitude[0])

        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)'):
            callingCode = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)')
            item['Calling_Code'] = str(callingCode[0])

        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)'):
            currency = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)')
            item['List_of_Currencies'] = str(currency[0])

        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)'):
            item['Capital_Name'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)')

        if response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)'):
            item['Region_Text'] = response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)')

        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)'):
            item['Language_Name'] = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)')


        #item['Source_Name'] = 'tordata5'
            
        yield item




###LIST OF ASSOCIATED CSVs###
#1 scrapy crawl toripres_2 -o toripres_2.csv

#debugging:
###ascii problems: country, address###

