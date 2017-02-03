#Seraphina Anderson, John Snow Labs, 17/1/2016

#Spider for generating Tor Project data from: https://check.torproject.org/exit-addresses
#as well as fingerprint data from urls of the following form:
#http://torstatus.rueckgr.at/router_detail.php?FP=<fingerprint>
#and WhoIs data from urls of form: http://whois.ipchecker.info/<IPAddress>

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
from toripresbot.items import TorIpResolutionItem


class ExitNodes(CrawlSpider):
    name = "toripres1"
   
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #url = 'https://check.torproject.org/exit-addresses'
        #yield Request(url, callback=self.parse_exitUrl)
        #test urls - feed all data sources here
        #Do we want to process one URL at a time, or loop through them here?
        urls = ['https://check.torproject.org/exit-addresses']
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_torProjectUrl)
            i += 1

    #tot. no. of data items: 1156
    def parse_torProjectUrl(self, response):
        #item = ExitNodesItem()
        data = response.xpath('//body//text()').extract()
        
        ###CREATE ITEM CONTAINER###
        entries = data[0].split('ExitNode')  
        entries.remove(entries[0])

        ###COLLECT DATA FOR EACH DATA FIELD###
        fingerPrints = [re.match('\s*(.*?)\\nPublished.*', str(e)).group(1) for e in entries if re.match('\s*(.*?)\\nPublished.*', e)]
        datepublished = [re.match('\s*.*?\\nPublished\s*(\d{4}-\d{2}-\d{2})\s*.*', str(e)).group(1) for e in entries if re.match('\s*.*?\\nPublished\s*(\d{4}-\d{2}-\d{2})\s*.*', e)]
        timepublished = [re.match('\s*.*?\\nPublished\s*\d{4}-\d{2}-\d{2}\s*?(\d{2}:\d{2}:\d{2}).*', str(e)).group(1) for e in entries if re.match('\s*.*?\\nPublished\s*\d{4}-\d{2}-\d{2}\s*?(\d{2}:\d{2}:\d{2}).*', e)]
        laststatusdate = [re.match('.*?\\n.*?\\nLastStatus\s*?(\d{4}-\d{2}-\d{2}).*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\nLastStatus\s*?(\d{4}-\d{2}-\d{2}).*', e)]
        laststatustime = [re.match('.*?\\n.*?\\nLastStatus\s*?\d{4}-\d{2}-\d{2}\s*(\d{2}:\d{2}:\d{2}).*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\nLastStatus\s*?\d{4}-\d{2}-\d{2}\s*(\d{2}:\d{2}:\d{2}).*', e)]
        #exitaddress = [re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*(\d+\.\d+\.\d+\.\d+)\s*.*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*(\d+\.\d+\.\d+\.\d+)\s*.*', e)]
        exitaddressdate = [re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*\d+\.\d+\.\d+\.\d+\s*(\d{4}-\d{2}-\d{2})\s*.*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*\d+\.\d+\.\d+\.\d+\s*(\d{4}-\d{2}-\d{2})\s*.*', e)]
        exitaddresstime = [re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*\d+\.\d+\.\d+\.\d+\s*\d{4}-\d{2}-\d{2}\s*(\d{2}:\d{2}:\d{2}).*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*\d+\.\d+\.\d+\.\d+\s*\d{4}-\d{2}-\d{2}\s*(\d{2}:\d{2}:\d{2}).*', e)]


        
    
        i = 0
        while i < len(fingerPrints):
            item = TorIpResolutionItem()

            #generate URLs here, from fingerprints
            url = 'http://torstatus.rueckgr.at/router_detail.php?FP=' + str(fingerPrints[i])
            #item['whoIs'] = urls[i]
            item['Date_Published_List_of_dates'] = datepublished[i]
            item['Time_Published_List_of_times'] = timepublished[i]
            item['Last_Status_Date_list_of_dates'] = laststatusdate[i]
            item['Last_Status_Time_list_of_times'] = laststatustime[i]
            #item['Exit_Address'] = exitaddress[i]
            item['Exit_Address_Date'] = exitaddressdate[i]
            item['Exit_Address_Time'] = exitaddresstime[i]
            #item['exitUrl'] = 'https://globe.torproject.org/#/relay/' + str(fingerPrints[i]) #decision is to keep this hidden
            yield Request(url, callback=self.parse_fingerprints, meta=dict(item=item))
            i += 1


            
  

    def parse_fingerprints(self, response):
        item = response.meta['item']
##        item['country'] = 'spider is working!'   #test urls are working!
##        yield item

        #get info container
        info1 = response.xpath('//td[@class="TRSB"]/text()').extract()
        
        ###CONTACT INFORMATION###    #test where url fails to load#
        if re.match('(.*?)?\s*<.*', str(info1[2])):
            item['Individual_Name'] =  re.match('(.*?)?\s*<.*', str(info1[2])).group(1)

        if re.match('.*?\s*<(.*?)>', str(info1[2])):
            item['Individual_Email'] =  re.match('.*?\s*<(.*?)>', str(info1[2])).group(1)

        
        item['Router_Name'] = str(info1[0])
        item['Fingerprint_Code'] = str(info1[1])
        ip = str(info1[3])
        item['ip_Text'] = str(info1[3])
        item['Host_Name'] = str(info1[4])
        item['OR_Port_Number'] = str(info1[5])
        item['Dir_Port_Text'] = str(info1[6])
        item['Country_Name'] = str(info1[7])
        #item['Platform_Version_Text'] = str(info1[8])
        
        
        ###DATES, TIMES, MEASUREMENTS###
        item['Descriptor_Publish_date'] = re.match('(.*?)?\d+:\d+:\d+', str(info1[9])).group(1)
        item['Descriptor_Publish_time'] = re.match('.*?(\d+:\d+:\d+)', str(info1[9])).group(1)
        
        platformVersion = str(info1[8])

        item['Platform_Text']= str(info1[8])
        
        #platform = re.match('\s*(?:Tor\s*\d+\.\d+\.\d+\.\d+)\s*on\s*(.*)', info1[8]).group(1)

        #test for these...

        #Bitrig = 1
        #Windows Server Vista = 2
        #Windows Server 2003 = 3
        #Windows Server 2008 = 4
        #Windows Server 8 = 5
        #Windows Server 7 = 6
        #Windows Vista = 7
        #FreeBSD = 8
        #Windows XP = 9
        #OpenBSD = 10
        #Linux = 11
        #Windows 7 = 12
        #Windows 8 = 13
        #Mac OS X = 14

        if re.match('.*?(?:B|b)itrig.*', platformVersion):  #Bitrig = 1
            item['Platform_Version_Text'] = 1
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*V?v?ista|W?w?indows\s*V?v?ista\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server Vista = 2
            item['Platform_Version_Text'] = 2
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*2003|W?w?indows\s*2003\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 2003 = 3
            item['Platform_Version_Text'] = 3
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*2008|W?w?indows\s*2008\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 2008 = 4
            item['Platform_Version_Text'] = 4
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*8|W?w?indows\s*8\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 8 = 5
            item['Platform_Version_Text'] = 5
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*7|W?w?indows\s*7\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 7 = 6
            item['Platform_Version_Text'] =  6
        elif re.match('.*?W?w?indows\s*V?v?ista.*', platformVersion):  #Windows Vista = 7
            item['Platform_Version_Text'] = 7
        elif re.match('.*?(?:FreeBSD|Freebsd|freebsd|freeBSD|freeBsd).*', platformVersion):  #FreeBSD = 8
            item['Platform_Version_Text'] = 8
        elif re.match('.*?W?w?indows\s*(?:XP|Xp|xP|xp).*', platformVersion):  #Windows XP = 9
            item['Platform_Version_Text'] = 9
        elif re.match('.*?o?O?pen(?:BSD|bSD|bsD|bsd|Bsd).*', platformVersion):  #OpenBSD = 10
            item['Platform_Version_Text'] = 10
        elif re.match('.*(?:L?l?inux|LINUX).*', platformVersion):  #Linux = 11
            item['Platform_Version_Text'] = 11
        elif re.match('.*?W?w?indows\s*7.*', platformVersion):  #Windows 7 = 12
            item['Platform_Version_Text'] = 12
        elif re.match('.*?W?w?indows\s*8.*', platformVersion):  #Windows 8 = 13
            item['Platform_Version_Text'] = 13
        elif re.match('.*?(?:M?m?ac\s*OS\s*(?:x|X)|MAC\s*OS\s*(?:X|x)).*', platformVersion):  #Mac OS X = 14
            item['Platform_Version_Text'] = 14
        else:
            item['Platform_Version_Text'] = 15  #miscellaneous


        uptime = str(info1[10])

        ###WORK OUT UPTIME IN SECONDS###
        uptime = uptime.split(',')
        uptime = [re.match('.*?(\d+).*', e).group(1) for e in uptime if re.match('.*?(\d+).*', e)]
    
        #test: print "initially we get: " + "days: " + str(uptime[0]) + ", hours: " + str(uptime[1]) + ", minutes: " + str(uptime[2]) + ", seconds: " + str(uptime[3])

        a = int(uptime[0])
        b = int(uptime[1])
        c = int(uptime[2])
        d = int(uptime[3])

        days = 24*60*60
        hrs = 60*60
        mins = 60
        secs = 1

        time_in_seconds = (days*a) + (hrs*b) + (mins*c) + (secs*d)

        #test:
        #print "test: " + "days: " + str((days*a)) + " / " + str((days*a)/(days)), ", hrs: " + str((hrs*b)) + " / " + str((hrs*b)/hrs) + ", mins: " + str((mins*c)) + " / " + str((mins*c)/mins) + ", secs: " + str((secs*d)) + " / " + str((secs*d)/secs)


        item['Up_Time_in_seconds'] = time_in_seconds


        #get bandwidth values
        if re.match('(\d{8}).*?(\d{8}).*?(\d{8}).*', info1[11]):
            num1 = re.match('(\d{8}).*?(\d{8}).*?(\d{8}).*', info1[11]).group(1)
            num2 = re.match('(\d{8}).*?(\d{8}).*?(\d{8}).*', info1[11]).group(2)
            num3 = re.match('(\d{8}).*?(\d{8}).*?(\d{8}).*', info1[11]).group(3)
            item['Bandwidth_in_kb'] = str(num1) + ' / ' + str(num2) + ' / ' + str(num3)
        elif re.match('(\d{8}).*?(\d{8}).*', info1[11]):
            num1 = re.match('(\d{8}).*?(\d{8}).*', info1[11]).group(1)
            num2 = re.match('(\d{8}).*?(\d{8}).*', info1[11]).group(2)
            item['Bandwidth_in_kb'] = str(num1) + ' / ' + str(num2) 
        elif re.match('(\d{8}).*', info1[11]):
            num1 = re.match('(\d{8}).*', info1[11]).group(1)
            item['Bandwidth_in_kb'] = str(num1)

       
        #get meta data
        meta = response.xpath('//td[@class="TRAR"]').extract()
        item['Bandwidth_Units'] = re.match('.*?-\s*I?i?n\s*(.*?)\)\s*:.*', str(meta[11])).group(1)
        #get families
        data = response.xpath('//td[@class="TRSB"]').extract()
        families = data[12].replace('<td class="TRSB">$', '')
        families = families.replace('<br>', '')
        families = families.replace('</td>', '')
        families = families.replace('$', ',')
        if re.match('.*[A-Za-z0-9]{20,60}.*', families):
            item['Family_Members_list_of_codes'] = str(families)


        
        ###ROUTER FLAGS### #TRUE/FALSE VALUES###
        #F0 False, F1 True
        
        authority = response.xpath('//tr[@class="nr"]').re('.*?<b>Authority:</b></td>\n<td\s*class="(F\d+)">.*')
        authority = str(authority[0])
        if authority == 'F0':
            item['is_Authority'] = 'False'
        if authority == 'F1':
            item['is_Authority'] = 'True'

        
        badDirectory = response.xpath('//tr[@class="nr"]').re('.*?<b>Bad\s*Directory:</b></td>\n<td\s*class="(F\d+)">.*')
        badDirectory = str(badDirectory[0])
        if badDirectory == 'F0':
            item['is_Bad_Directory'] = 'False'
        if badDirectory == 'F1':
            item['is_Bad_Directory'] = 'True'

        badExit = response.xpath('//tr[@class="nr"]').re('.*?<b>Bad\s*Exit:</b></td>\n<td\s*class="(F\d+)">.*')
        badExit = str(badExit[0])
        if badExit == 'F0':
            item['is_Bad_Exit'] = 'False'
        if badExit == 'F1':
            item['is_Bad_Exit'] = 'True'

        exitTrueFalse = response.xpath('//tr[@class="nr"]').re('.*?<b>Exit:</b></td>\n<td\s*class="(F\d+)">.*')
        exitTrueFalse = str(exitTrueFalse[0])
        if exitTrueFalse == 'F0':
            item['is_Exit'] = 'False'
        if exitTrueFalse == 'F1':
            item['is_Exit'] = 'True'

        fast = response.xpath('//tr[@class="nr"]').re('.*?<b>Fast:</b></td>\n<td\s*class="(F\d+)">.*')
        fast = str(fast[0])
        if fast == 'F0':
            item['is_Fast'] = 'False'
        if fast == 'F1':
            item['is_Fast'] = 'True'

        guard = response.xpath('//tr[@class="nr"]').re('.*?<b>Guard:</b></td>\n<td\s*class="(F\d+)">.*')
        guard = str(guard[0])
        if guard == 'F0':
            item['is_Guard'] = 'False'
        if guard == 'F1':
            item['is_Guard'] = 'True'

        hibernating = response.xpath('//tr[@class="nr"]').re('.*?<b>Hibernating:</b></td>\n<td\s*class="(F\d+)">.*')
        hibernating = str(hibernating[0])
        if hibernating == 'F0':
            item['is_Hibernating'] = 'False'
        if hibernating == 'F1':
            item['is_Hibernating'] = 'True'

        named = response.xpath('//tr[@class="nr"]').re('.*?<b>Named:</b></td>\n<td\s*class="(F\d+)">.*')
        named = str(named[0])
        if named == 'F0':
            item['is_Named'] = 'False'
        if named == 'F1':
            item['is_Named'] = 'True'

        stable = response.xpath('//tr[@class="nr"]').re('.*?<b>Stable:</b></td>\n<td\s*class="(F\d+)">.*')
        stable = str(stable[0])
        if stable == 'F0':
            item['is_Stable'] = 'False'
        if stable == 'F1':
            item['is_Stable'] = 'True'

        running = response.xpath('//tr[@class="nr"]').re('.*?<b>Running:</b></td>\n<td\s*class="(F\d+)">.*')
        running = str(running[0])
        if running == 'F0':
            item['is_Running'] = 'False'
        if running == 'F1':
            item['is_Running'] = 'True'

        valid = response.xpath('//tr[@class="nr"]').re('.*?<b>Valid:</b></td>\n<td\s*class="(F\d+)">.*')
        valid = str(valid[0])
        if valid == 'F0':
            item['is_Valid'] = 'False'
        if valid == 'F1':
            item['is_Valid'] = 'True'

        v2Dir = response.xpath('//tr[@class="nr"]').re('.*?<b>V2Dir:</b></td>\n<td\s*class="(F\d+)">.*')
        v2Dir = str(v2Dir[0])
        if v2Dir == 'F0':
            item['is_V2Dir'] = 'False'
        if v2Dir == 'F1':
            item['is_V2Dir'] = 'True'


        
        ####################################
    
        #Exit Policy info - ACCEPT/REJECT values
        exitpolicy = response.xpath('//b//text()').re('.*?(?:accept).*')
        item['is_Exit_Accept'] = [str(e) for e in exitpolicy]
        exitpolicy = response.xpath('//b//text()').re('.*?(?:reject).*')
        item['is_Exit_Reject'] = [str(e) for e in exitpolicy]

        ###ROUTER KEYS###
        routerkeys = response.xpath('//td[@colspan="3"]//text()').extract()
        onion = routerkeys[3]
        onion = onion.replace('-----BEGIN RSA PUBLIC KEY-----\r\n', '')
        onion = onion.replace('\r\n-----END RSA PUBLIC KEY-----\r', '')
        onion = onion.replace('\r\n', '')

        item['Onion_Key_Code'] = str(onion)  #RSA public key

        signing = routerkeys[6]
        signing = signing.replace('-----BEGIN RSA PUBLIC KEY-----\r\n', '')
        signing = signing.replace('\r\n-----END RSA PUBLIC KEY-----\r', '')
        signing = signing.replace('\r\n', '')
        item['Signing_Key_Code'] = str(signing)  #RSA public key
    
        #site operator
        operator = response.xpath('//td[@class="TRC"]').re('.*?S?s?ite\s*O?o?perator.*')
        operator = re.match('.*?<strong>(.*?)?<\/strong>.*', operator[0]).group(1)
        item['Site_Operator_Name'] = str(operator) #name of person operating site
        item['Source_Name'] = 'tordata8_i'

        #item['counter'] = i #for internal use

        #########################
        ###GENERATE WHOIS URL####
        #########################

        url = 'http://whois.ipchecker.info/' + str(ip)

        yield Request(url, callback=self.parse_whois_data, meta=dict(item=item))


    def parse_whois_data(self, response):
        item = response.meta['item']
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

        #item field used below
        #if response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*'):
            #item['Date_Published_List_of_dates'] = response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*')  #created
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



        #DATA MISSING FROM THIS DATASOURCE
        item['Dir_Port_Text'] = ''
        item['First_Seen_date'] = ''
        item['AS_Name_Text'] = ''
        item['AS_Number_Text'] = ''
        item['Consensus_Bandwidth_in_kb'] = ''
        item['OR_Address_Text'] = ''


        yield item
        


#transfer to csv
#scrapy crawl toripres1 -o TOR_IP_RESOLUTION_08_i.csv


