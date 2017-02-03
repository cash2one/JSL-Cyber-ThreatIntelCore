#Seraphina Anderson, John Snow Labs, 13/1/2016

#Spider for generating Tor Project data from: https://check.torproject.org/exit-addresses
#as well as fingerprint data from urls of the following form:
#http://torstatus.rueckgr.at/router_detail.php?FP=fingerprint

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
    name = "toripres4a"
   
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
        ip = [re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*(\d+\.\d+\.\d+\.\d+)\s*.*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*(\d+\.\d+\.\d+\.\d+)\s*.*', e)]
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
            item['ip'] = ip[i]
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
        item['ip'] = str(info1[3])
        item['hostName'] = str(info1[4])
        item['orPort'] = str(info1[5])
        item['dirPort'] = str(info1[6])
        item['country'] = str(info1[7])


        #item['platformVersion'] = str(info1[8])

        platformVersion = str(info1[8])

        item['platform']= str(info1[8])
        
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
            item['platformVersion'] = 1
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*V?v?ista|W?w?indows\s*V?v?ista\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server Vista = 2
            item['platformVersion'] = 2
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*2003|W?w?indows\s*2003\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 2003 = 3
            item['platformVersion'] = 3
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*2008|W?w?indows\s*2008\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 2008 = 4
            item['platformVersion'] = 4
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*8|W?w?indows\s*8\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 8 = 5
            item['platformVersion'] = 5
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*7|W?w?indows\s*7\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 7 = 6
            item['platformVersion'] =  6
        elif re.match('.*?W?w?indows\s*V?v?ista.*', platformVersion):  #Windows Vista = 7
            item['platformVersion'] = 7
        elif re.match('.*?(?:FreeBSD|Freebsd|freebsd|freeBSD|freeBsd).*', platformVersion):  #FreeBSD = 8
            item['platformVersion'] = 8
        elif re.match('.*?W?w?indows\s*(?:XP|Xp|xP|xp).*', platformVersion):  #Windows XP = 9
            item['platformVersion'] = 9
        elif re.match('.*?o?O?pen(?:BSD|bSD|bsD|bsd|Bsd).*', platformVersion):  #OpenBSD = 10
            item['platformVersion'] = 10
        elif re.match('.*(?:L?l?inux|LINUX).*', platformVersion):  #Linux = 11
            item['platformVersion'] = 11
        elif re.match('.*?W?w?indows\s*7.*', platformVersion):  #Windows 7 = 12
            item['platformVersion'] = 12
        elif re.match('.*?W?w?indows\s*8.*', platformVersion):  #Windows 8 = 13
            item['platformVersion'] = 13
        elif re.match('.*?(?:M?m?ac\s*OS\s*(?:x|X)|MAC\s*OS\s*(?:X|x)).*', platformVersion):  #Mac OS X = 14
            item['platformVersion'] = 14
        else:
            item['platformVersion'] = 15  #miscellaneous

        
        
        ###DATES, TIMES, MEASUREMENTS###
        item['descriptorPublishDate'] = re.match('(.*?)?\d+:\d+:\d+', str(info1[9])).group(1)
        item['descriptorPublishTime'] = re.match('.*?(\d+:\d+:\d+)', str(info1[9])).group(1)

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


        item['upTimeSeconds'] = time_in_seconds

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
        item['sourceName'] = 'tordata3'

        #item['counter'] = i #for internal use
        yield item


#transfer to csv
#scrapy crawl exitnodes3 -o tor_exit_addresses4a.csv

