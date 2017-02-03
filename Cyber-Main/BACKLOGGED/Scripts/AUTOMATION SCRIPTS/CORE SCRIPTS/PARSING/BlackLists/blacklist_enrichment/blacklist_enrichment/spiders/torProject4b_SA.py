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
from blacklist_enrichment.items import TorIpResolutionItem


class ExitNodes(CrawlSpider):
    name = "toripres6b"
   
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
            item['fingerPrint'] = fingerPrints[i]
            #item['whoIs'] = urls[i]
            item['datePublished'] = datepublished[i]
            item['timePublished'] = timepublished[i]
            item['lastStatusDate'] = laststatusdate[i]
            item['lastStatusTime'] = laststatustime[i]
            #item['exitAddress'] = exitaddress[i]
            item['exitAddressDate'] = exitaddressdate[i]
            item['exitAddressTime'] = exitaddresstime[i]
            #item['exitUrl'] = 'https://globe.torproject.org/#/relay/' + str(fingerPrints[i]) #decision is to keep this hidden
            yield Request(url, callback=self.parse_fingerprints, meta=dict(item=item))
            i += 1

    def parse_fingerprints(self, response):
        item = response.meta['item']
##        item['country'] = 'spider is working!'   #test urls are working!
##        yield item

        #get info container
        info1 = response.xpath('//td[@class="TRSB"]/text()').extract()
        
        ###CONTACT INFORMATION###
        if re.match('(.*?)?\s*<.*', str(info1[2])):
            item['nameIndividual'] =  re.match('(.*?)?\s*<.*', str(info1[2])).group(1)
        else:
            item['nameIndividual'] = 'Null'
        if re.match('.*?\s*<(.*?)>', str(info1[2])):
            item['emailIndividual'] =  re.match('.*?\s*<(.*?)>', str(info1[2])).group(1)
        else:
            item['emailIndividual'] = 'Null'
            
        
        item['routerName'] = str(info1[0])
        item['fingerPrint'] = str(info1[1])
        ip = str(info1[3])
        item['ip'] = str(info1[3])
        item['hostName'] = str(info1[4])
        item['orPort'] = str(info1[5])
        item['dirPort'] = str(info1[6])
        item['country'] = str(info1[7])
        item['platformVersion'] = str(info1[8])
        
        
        ###DATES, TIMES, MEASUREMENTS###
        item['descriptorPublishDate'] = re.match('(.*?)?\d+:\d+:\d+', str(info1[9])).group(1)
        item['descriptorPublishTime'] = re.match('.*?(\d+:\d+:\d+)', str(info1[9])).group(1)
        item['upTime'] = str(info1[10])
        #get bandwidth values
        if re.match('(\d{8}).*?(\d{8}).*?(\d{8}).*', info1[11]):
            num1 = re.match('(\d{8}).*?(\d{8}).*?(\d{8}).*', info1[11]).group(1)
            num2 = re.match('(\d{8}).*?(\d{8}).*?(\d{8}).*', info1[11]).group(2)
            num3 = re.match('(\d{8}).*?(\d{8}).*?(\d{8}).*', info1[11]).group(3)
            item['bandwidth'] = str(num1) + ' / ' + str(num2) + ' / ' + str(num3)
        elif re.match('(\d{8}).*?(\d{8}).*', info1[11]):
            num1 = re.match('(\d{8}).*?(\d{8}).*', info1[11]).group(1)
            num2 = re.match('(\d{8}).*?(\d{8}).*', info1[11]).group(2)
            item['bandwidth'] = str(num1) + ' / ' + str(num2) 
        elif re.match('(\d{8}).*', info1[11]):
            num1 = re.match('(\d{8}).*', info1[11]).group(1)
            item['bandwidth'] = str(num1)
        else:
            item['bandwidth'] = 'Null'
       
        #get meta data
        meta = response.xpath('//td[@class="TRAR"]').extract()
        item['bandwidthUnits'] = re.match('.*?-\s*I?i?n\s*(.*?)\)\s*:.*', str(meta[11])).group(1)
        #get families
        data = response.xpath('//td[@class="TRSB"]').extract()
        families = data[12].replace('<td class="TRSB">$', '')
        families = families.replace('<br>', '')
        families = families.replace('</td>', '')
        families = families.replace('$', ',')
        if re.match('.*[A-Za-z0-9]{20,60}.*', families):
            item['familyMembers'] = str(families)
        else:
            item['familyMembers'] = 'Null'
            

        
        ###ROUTER FLAGS### #TRUE/FALSE VALUES###
        #F0 False, F1 True
        
        authority = response.xpath('//tr[@class="nr"]').re('.*?<b>Authority:</b></td>\n<td\s*class="(F\d+)">.*')
        authority = str(authority[0])
        if authority == 'F0':
            item['authority'] = 'False'
        if authority == 'F1':
            item['authority'] = 'True'  
        
        badDirectory = response.xpath('//tr[@class="nr"]').re('.*?<b>Bad\s*Directory:</b></td>\n<td\s*class="(F\d+)">.*')
        badDirectory = str(badDirectory[0])
        if badDirectory == 'F0':
            item['badDirectory'] = 'False'
        if badDirectory == 'F1':
            item['badDirectory'] = 'True'

        badExit = response.xpath('//tr[@class="nr"]').re('.*?<b>Bad\s*Exit:</b></td>\n<td\s*class="(F\d+)">.*')
        badExit = str(badExit[0])
        if badExit == 'F0':
            item['badExit'] = 'False'
        if badExit == 'F1':
            item['badExit'] = 'True'

        exitTrueFalse = response.xpath('//tr[@class="nr"]').re('.*?<b>Exit:</b></td>\n<td\s*class="(F\d+)">.*')
        exitTrueFalse = str(exitTrueFalse[0])
        if exitTrueFalse == 'F0':
            item['exitTrueFalse'] = 'False'
        if exitTrueFalse == 'F1':
            item['exitTrueFalse'] = 'True'

        fast = response.xpath('//tr[@class="nr"]').re('.*?<b>Fast:</b></td>\n<td\s*class="(F\d+)">.*')
        fast = str(fast[0])
        if fast == 'F0':
            item['fast'] = 'False'
        if fast == 'F1':
            item['fast'] = 'True'

        guard = response.xpath('//tr[@class="nr"]').re('.*?<b>Guard:</b></td>\n<td\s*class="(F\d+)">.*')
        guard = str(guard[0])
        if guard == 'F0':
            item['guard'] = 'False'
        if guard == 'F1':
            item['guard'] = 'True'

        hibernating = response.xpath('//tr[@class="nr"]').re('.*?<b>Hibernating:</b></td>\n<td\s*class="(F\d+)">.*')
        hibernating = str(hibernating[0])
        if hibernating == 'F0':
            item['hibernating'] = 'False'
        if hibernating == 'F1':
            item['hibernating'] = 'True'

        named = response.xpath('//tr[@class="nr"]').re('.*?<b>Named:</b></td>\n<td\s*class="(F\d+)">.*')
        named = str(named[0])
        if named == 'F0':
            item['named'] = 'False'
        if named == 'F1':
            item['named'] = 'True'

        stable = response.xpath('//tr[@class="nr"]').re('.*?<b>Stable:</b></td>\n<td\s*class="(F\d+)">.*')
        stable = str(stable[0])
        if stable == 'F0':
            item['stable'] = 'False'
        if stable == 'F1':
            item['stable'] = 'True'

        running = response.xpath('//tr[@class="nr"]').re('.*?<b>Running:</b></td>\n<td\s*class="(F\d+)">.*')
        running = str(running[0])
        if running == 'F0':
            item['running'] = 'False'
        if running == 'F1':
            item['running'] = 'True'

        valid = response.xpath('//tr[@class="nr"]').re('.*?<b>Valid:</b></td>\n<td\s*class="(F\d+)">.*')
        valid = str(valid[0])
        if valid == 'F0':
            item['valid'] = 'False'
        if valid == 'F1':
            item['valid'] = 'True'

        v2Dir = response.xpath('//tr[@class="nr"]').re('.*?<b>V2Dir:</b></td>\n<td\s*class="(F\d+)">.*')
        v2Dir = str(v2Dir[0])
        if v2Dir == 'F0':
            item['v2Dir'] = 'False'
        if v2Dir == 'F1':
            item['v2Dir'] = 'True'


        
        ####################################

    
        #Exit Policy info - ACCEPT/REJECT values
        exitpolicy = response.xpath('//b//text()').re('.*?(?:accept).*')
        item['exitAccept'] = [str(e) for e in exitpolicy]
        exitpolicy = response.xpath('//b//text()').re('.*?(?:reject).*')
        item['exitReject'] = [str(e) for e in exitpolicy]

        ###ROUTER KEYS###
        routerkeys = response.xpath('//td[@colspan="3"]//text()').extract()
        onion = routerkeys[3]
        onion = onion.replace('-----BEGIN RSA PUBLIC KEY-----\r\n', '')
        onion = onion.replace('\r\n-----END RSA PUBLIC KEY-----\r', '')
        onion = onion.replace('\r\n', '')
        item['onionKey'] = str(onion)  #RSA public key

        signing = routerkeys[6]
        signing = signing.replace('-----BEGIN RSA PUBLIC KEY-----\r\n', '')
        signing = signing.replace('\r\n-----END RSA PUBLIC KEY-----\r', '')
        signing = signing.replace('\r\n', '')
        item['signingKey'] = str(signing)  #RSA public key
    
        #site operator
        operator = response.xpath('//td[@class="TRC"]').re('.*?S?s?ite\s*O?o?perator.*')
        operator = re.match('.*?<strong>(.*?)?<\/strong>.*', operator[0]).group(1)
        item['siteOperator'] = str(operator) #name of person operating site
        item['sourceName'] = 'tordata6'

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
            item['inetNum'] = response.xpath('//pre1').re('.*?inetnum:\s*(.*)')
            #inetNum = str(inetNum[0])
        else:
            item['inetNum'] = 'Null'
        if response.xpath('//pre1').re('.*?netname:\s*(.*)'):
            item['netName'] = response.xpath('//pre1').re('.*?netname:\s*(.*)')
            #netName = str(netName[0])
        else:
            item['netName'] = 'Null'
        if response.xpath('//pre1').re('.*?descr:\s*(.*)'):
            item['description'] = response.xpath('//pre1').re('.*?descr:\s*(.*)')
            #description = str(description[0])
        else:
            item['description'] = 'Null'
        if response.xpath('//pre1').re('.*?admin-?c:\s*(.*)'):
            item['adminc'] = response.xpath('//pre1').re('.*?admin-?c:\s*(.*)')
            #adminc = str(adminc[0])
        else:
            item['adminc'] = 'Null'
        if response.xpath('//pre1').re('.*?tech-?c:\s*(.*)'):
            item['techc'] = response.xpath('//pre1').re('.*?tech-?c:\s*(.*)')
            #techc = str(techc[0])
        else:
            item['techc'] = 'Null'
        if response.xpath('//pre1').re('.*?status:\s*(.*)'):
            item['status'] = response.xpath('//pre1').re('.*?status:\s*(.*)')
            #status = str(status[0])
        else:
            item['status'] = 'Null'
        if response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)'):
            item['mntby'] = response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)')
            #mntby = str(mntby[0])
        else:
            item['mntby'] = 'Null'
        if response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*'):
            item['datePublished'] = response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*')  #created
            #datePublished = str(datePublished[0])
        else:
            item['datePublished'] = 'Null'
        if response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
            item['timePublished'] = response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
            #timePublished = str(timePublished[0])
        else:
            item['timePublished'] = 'Null'
        if response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*'):
            item['lastStatusDate'] = response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*') #last-modified
            #lastStatusDate = str(lastStatusDate[0])
        else:
            item['lastStatusDate'] = 'Null'
        if response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
            item['lastStatusTime'] = response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
            #lastStatusTime = str(lastStatusTime[0])
        else:
            item['lastStatusTime'] = 'Null'
        if response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)'):
            item['organisation'] = response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)')
            #organisation = str(organisation[0])
        else:
            item['organisation'] = 'Null'
        if response.xpath('//pre1').re('.*?org-name:\s*(.*)'):
            orgName = response.xpath('//pre1').re('.*?org-?name:\s*(.*)')
            item['orgName'] = orgName #str(orgName[0])
        else:
            item['orgName'] = 'Null'
        if response.xpath('//pre1').re('.*?org-type:\s*(.*)'):
            orgType = response.xpath('//pre1').re('.*?org-?type:\s*(.*)')
            item['orgType'] = orgType#str(orgType[0])
        else:
            item['orgType'] = 'Null'
        if response.xpath('//pre1').re('.*?remarks:\s*(.*)'):
            remarks = response.xpath('//pre1').re('.*?remarks:\s*(.*)')
            item['remarks'] = remarks #str(remarks[0])
        else:
            item['remarks'] = 'Null'
        if response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)'):
            mntRef = response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)')
            item['mntRef'] = mntRef#str(mntRef[0])
        else:
            item['mntRef'] = 'Null'
        if response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)'):
            abuseC = response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)')
            item['abuseC'] = abuseC #str(abuseC[0])
        else:
            item['abuseC'] = 'Null'
        if response.xpath('//pre1').re('.*?person:\s*(.*)'):
            person = response.xpath('//pre1').re('.*?person:\s*(.*)')
            item['person'] = person#str(person[0])
        else:
            item['person'] = 'Null'
        if response.xpath('//pre1').re('.*?address:\s*(.*)'):
            postalAddress = response.xpath('//pre1').re('.*?address:\s*(.*)')
            item['postalAddress'] = [str(e) for e in postalAddress]
        else:
            item['postalAddress'] = 'Null'
        if response.xpath('//pre1').re('.*?phone:\s*(.*)'):
            phone = response.xpath('//pre1').re('.*?phone:\s*(.*)')
            item['phone'] = [str(e) for e in phone]
        else:
            item['phone'] = 'Null'
        if response.xpath('//pre1').re('.*?fax-?no:\s*(.*)'):
            faxNo = response.xpath('//pre1').re('.*?fax-?no:\s*(.*)')
            item['faxNo'] = [str(e) for e in faxNo]
        else:
            item['faxNo'] = 'Null'
        if response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)'):
            nicHdl = response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)')
            item['nicHdl'] = [str(e) for e in nicHdl]
        else:
            item['nicHdl'] = 'Null'
        if response.xpath('//pre1').re('.*?route:\s*(.*)'):
            route = response.xpath('//pre1').re('.*?route:\s*(.*)')
            item['route'] = route#str(route[0])
        else:
            item['route'] = 'Null'
        if response.xpath('//pre1').re('.*?origin:\s*(.*)'):
            origin = response.xpath('//pre1').re('.*?origin:\s*(.*)')
            item['origin'] = origin#str(origin[0])
        else:
            item['origin'] = 'Null'
        if response.xpath('//pre1').re('.*?member-?of:\s*(.*)'):
            memberOf = response.xpath('//pre1').re('.*?member-?of:\s*(.*)')
            item['memberOf'] = memberOf#str(memberOf[0])
        else:
            item['memberOf'] = 'Null'


        ###IP LOCATION###
        #get all location info
        location = response.xpath('//div[@class="span6"]//p//text()').extract()
        #populate data fields
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)'):
            item['country'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)')
        else:
            item['country'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)'):
            latitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)')
            item['latitude'] = str(latitude[0])
        else:
            item['latitude'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)'):
            longitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)')
            item['longitude'] = str(longitude[0])
        else:
            item['longitude'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)'):
            callingCode = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)')
            item['callingCode'] = str(callingCode[0])
        else:
            item['callingCode'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)'):
            currency = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)')
            item['currency'] = str(currency[0])
        else:
            item['currency'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)'):
            item['capital'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)')
        else:
            item['capital'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)'):
            item['region'] = response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)')
        else:
            item['region'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)'):
            item['language'] = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)')
        else:
            item['language'] = 'Null'

        item['sourceName'] = 'tordata6'


        yield item
        


#transfer to csv
#scrapy crawl exitnodes5 -o tor_exit_addresses7a.csv


