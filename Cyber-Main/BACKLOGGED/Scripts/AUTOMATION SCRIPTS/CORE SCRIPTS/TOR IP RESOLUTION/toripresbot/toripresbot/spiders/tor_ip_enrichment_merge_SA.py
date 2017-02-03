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

#Note:
#'https://check.torproject.org/exit-addresses' => torProject4.py
#'https://torstatus.blutmagie.de' => whoIs2a.py


class ExitNodes(CrawlSpider):
    name = "toripresall"
   
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #url = 'https://check.torproject.org/exit-addresses'
        #yield Request(url, callback=self.parse_exitUrl)
        #test urls - feed all data sources here
        #Do we want to process one URL at a time, or loop through them here?
        urls = ['https://check.torproject.org/exit-addresses', 'https://torstatus.blutmagie.de']
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_Url)
            i += 1

    #tot. no. of data items: 1156
    def parse_Url(self, response):
        #get url, so we can test where to go...
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        if url == 'https://check.torproject.org/exit-addresses':
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
                yield Request(url, callback=self.parse_data1, meta=dict(item=item))
                i += 1


        else:
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
            nums = [re.match('.*?(\d+).*', e).group(1) for e in uptime]
            units = [re.match('\d+\s*?(\w+).*', e).group(1) for e in uptime]
            d = int(24*60*60)
            h = int(60*60)
            upTimeSeconds = [int(nums[i])*d if units[i] == 'd' else int(nums[i])*h for i, e in enumerate(uptime)]

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
                #url = 'http://whois.ipchecker.info/' + str(ip[i])
                url = 'https://torstatus.blutmagie.de'
                #item['ip'] = ip[i] #parse this itemfield
                item['routerName'] = routerName[i]
                item['bandwidth'] = bandwidth[i]
                item['upTimeSeconds'] = upTimeSeconds[i]
                item['hostName'] = hostName[i]
                item['orPort'] = orPort[i]
                item['dirPort'] = dirPort[i]
                item['firstSeen'] = firstSeen[i]
                item['asName'] = asName[i]
                item['asNumber'] = asNumber[i]
                item['consensusBandwidth'] = consensusBandwidth[i]
                item['orAddress'] = orAddress[i]
                yield Request(url, callback=self.parse_data1, meta=dict(item=item))
                i += 1



    def parse_data1(self, response):
        item = response.meta['item']
        #get url for testing where to go
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        if 'http://torstatus.rueckgr.at/router_detail.php' in url:

            #get info container
            info1 = response.xpath('//td[@class="TRSB"]/text()').extract()
        
            ###CONTACT INFORMATION###
            if re.match('(.*?)?\s*<.*', str(info1[2])):
                item['nameIndividual'] =  re.match('(.*?)?\s*<.*', str(info1[2])).group(1)

            if re.match('.*?\s*<(.*?)>', str(info1[2])):
                item['emailIndividual'] =  re.match('.*?\s*<(.*?)>', str(info1[2])).group(1)

            
        
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
        
            platformVersion = str(info1[8])

            item['platform']= str(info1[8])
        

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


        else:
            #'https://torstatus.blutmagie.de'
            #generate corresponding WhoIs urls
            ###CREATE ITEM CONTAINER###
            dataRow = response.xpath('//tr[@class="r"]').extract()
            dataRow.remove(dataRow[0])


            ###generate item containers#################
            dataRow = [e.split('<td ') for e in dataRow]
            ip = [re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]).group(1) if re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]) else '' for k, e in enumerate(dataRow)]
            i = 0
            while i < len(ip):
                item['ip'] = ip[i]
                url = 'http://whois.ipchecker.info/' + str(ip[i])
                yield Request(url, callback=self.parse_whois_data, meta=dict(item=item))
                i += 1

    def parse_whois_data(self, response):
        item = response.meta['item']
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        
        #http://torstatus.rueckgr.at/router_detail.php?FP=F94BCE1B6E3899FA4E4CBCC3B19C4FD8CC2B33BB
        if 'http://whois.ipchecker.info' in url:

            results = response.xpath('//pre1').extract()
        
            if response.xpath('//pre1').re('.*?inetnum:\s*(.*)'):
                item['inetNum'] = response.xpath('//pre1').re('.*?inetnum:\s*(.*)')
                #inetNum = str(inetNum[0])

            if response.xpath('//pre1').re('.*?netname:\s*(.*)'):
                item['netName'] = response.xpath('//pre1').re('.*?netname:\s*(.*)')
                #netName = str(netName[0])

            if response.xpath('//pre1').re('.*?descr:\s*(.*)'):
                item['description'] = response.xpath('//pre1').re('.*?descr:\s*(.*)')
                #description = str(description[0])

            if response.xpath('//pre1').re('.*?admin-?c:\s*(.*)'):
                item['adminc'] = response.xpath('//pre1').re('.*?admin-?c:\s*(.*)')
                #adminc = str(adminc[0])

            if response.xpath('//pre1').re('.*?tech-?c:\s*(.*)'):
                item['techc'] = response.xpath('//pre1').re('.*?tech-?c:\s*(.*)')
                #techc = str(techc[0])

            if response.xpath('//pre1').re('.*?status:\s*(.*)'):
                item['status'] = response.xpath('//pre1').re('.*?status:\s*(.*)')
                #status = str(status[0])

            if response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)'):
                item['mntby'] = response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)')
                #mntby = str(mntby[0])

            if response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*'):
                item['datePublished'] = response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*')  #created
                #datePublished = str(datePublished[0])

            if response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
                item['timePublished'] = response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
                #timePublished = str(timePublished[0])

            if response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*'):
                item['lastStatusDate'] = response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*') #last-modified
                #lastStatusDate = str(lastStatusDate[0])

            if response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
                item['lastStatusTime'] = response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
                #lastStatusTime = str(lastStatusTime[0])

            if response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)'):
                item['organisation'] = response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)')
                #organisation = str(organisation[0])

            if response.xpath('//pre1').re('.*?org-name:\s*(.*)'):
                orgName = response.xpath('//pre1').re('.*?org-?name:\s*(.*)')
                item['orgName'] = orgName #str(orgName[0])

            if response.xpath('//pre1').re('.*?org-type:\s*(.*)'):
                orgType = response.xpath('//pre1').re('.*?org-?type:\s*(.*)')
                item['orgType'] = orgType#str(orgType[0])

            if response.xpath('//pre1').re('.*?remarks:\s*(.*)'):
                remarks = response.xpath('//pre1').re('.*?remarks:\s*(.*)')
                item['remarks'] = remarks #str(remarks[0])

            if response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)'):
                mntRef = response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)')
                item['mntRef'] = mntRef#str(mntRef[0])

            if response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)'):
                abuseC = response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)')
                item['abuseC'] = abuseC #str(abuseC[0])

            if response.xpath('//pre1').re('.*?person:\s*(.*)'):
                person = response.xpath('//pre1').re('.*?person:\s*(.*)')
                item['person'] = person#str(person[0])

            if response.xpath('//pre1').re('.*?address:\s*(.*)'):
                postalAddress = response.xpath('//pre1').re('.*?address:\s*(.*)')
                item['postalAddress'] = [str(e) for e in postalAddress]

            if response.xpath('//pre1').re('.*?phone:\s*(.*)'):
                phone = response.xpath('//pre1').re('.*?phone:\s*(.*)')
                item['phone'] = [str(e) for e in phone]

            if response.xpath('//pre1').re('.*?fax-?no:\s*(.*)'):
                faxNo = response.xpath('//pre1').re('.*?fax-?no:\s*(.*)')
                item['faxNo'] = [str(e) for e in faxNo]
 
            if response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)'):
                nicHdl = response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)')
                item['nicHdl'] = [str(e) for e in nicHdl]

            if response.xpath('//pre1').re('.*?route:\s*(.*)'):
                route = response.xpath('//pre1').re('.*?route:\s*(.*)')
                item['route'] = route#str(route[0])

            if response.xpath('//pre1').re('.*?origin:\s*(.*)'):
                origin = response.xpath('//pre1').re('.*?origin:\s*(.*)')
                item['origin'] = origin#str(origin[0])

            if response.xpath('//pre1').re('.*?member-?of:\s*(.*)'):
                memberOf = response.xpath('//pre1').re('.*?member-?of:\s*(.*)')
                item['memberOf'] = memberOf#str(memberOf[0])



            ###IP LOCATION###
            #get all location info
            location = response.xpath('//div[@class="span6"]//p//text()').extract()
            #populate data fields
            if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)'):
                item['country'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)')
 
            if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)'):
                latitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)')
                item['latitude'] = str(latitude[0])

            if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)'):
                longitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)')
                item['longitude'] = str(longitude[0])

            if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)'):
                callingCode = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)')
                item['callingCode'] = str(callingCode[0])

            if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)'):
                currency = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)')
                item['currency'] = str(currency[0])

            if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)'):
                item['capital'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)')

            if response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)'):
                item['region'] = response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)')

            if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)'):
                item['language'] = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)')


            item['sourceName'] = 'tordata6'


            yield item


        else:
            #get LHS data
            results = response.xpath('//pre1').extract()
            if response.xpath('//pre1').re('.*?inetnum:\s*(.*)'):
                item['inetNum'] = response.xpath('//pre1').re('.*?inetnum:\s*(.*)')
                #inetNum = str(inetNum[0])

            if response.xpath('//pre1').re('.*?netname:\s*(.*)'):
                item['netName'] = response.xpath('//pre1').re('.*?netname:\s*(.*)')
                #netName = str(netName[0])

            if response.xpath('//pre1').re('.*?descr:\s*(.*)'):
                item['description'] = response.xpath('//pre1').re('.*?descr:\s*(.*)')
                #description = str(description[0])

            if response.xpath('//pre1').re('.*?admin-?c:\s*(.*)'):
                item['adminc'] = response.xpath('//pre1').re('.*?admin-?c:\s*(.*)')
                #adminc = str(adminc[0])

            if response.xpath('//pre1').re('.*?tech-?c:\s*(.*)'):
                item['techc'] = response.xpath('//pre1').re('.*?tech-?c:\s*(.*)')
                #techc = str(techc[0])

            if response.xpath('//pre1').re('.*?status:\s*(.*)'):
                item['status'] = response.xpath('//pre1').re('.*?status:\s*(.*)')
                #status = str(status[0])

            if response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)'):
                item['mntby'] = response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)')
                #mntby = str(mntby[0])

            if response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*'):
                item['datePublished'] = response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*')  #created
                #datePublished = str(datePublished[0])

            if response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
                item['timePublished'] = response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
                #timePublished = str(timePublished[0])

            if response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*'):
                item['lastStatusDate'] = response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*') #last-modified
                #lastStatusDate = str(lastStatusDate[0])

            if response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
                item['lastStatusTime'] = response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
                #lastStatusTime = str(lastStatusTime[0])

            if response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)'):
                item['organisation'] = response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)')
                #organisation = str(organisation[0])

            if response.xpath('//pre1').re('.*?org-name:\s*(.*)'):
                orgName = response.xpath('//pre1').re('.*?org-?name:\s*(.*)')
                item['orgName'] = orgName #str(orgName[0])

            if response.xpath('//pre1').re('.*?org-type:\s*(.*)'):
                orgType = response.xpath('//pre1').re('.*?org-?type:\s*(.*)')
                item['orgType'] = orgType#str(orgType[0])

            if response.xpath('//pre1').re('.*?remarks:\s*(.*)'):
                remarks = response.xpath('//pre1').re('.*?remarks:\s*(.*)')
                item['remarks'] = remarks #str(remarks[0])

            if response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)'):
                mntRef = response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)')
                item['mntRef'] = mntRef#str(mntRef[0])

            if response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)'):
                abuseC = response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)')
                item['abuseC'] = abuseC #str(abuseC[0])

            if response.xpath('//pre1').re('.*?person:\s*(.*)'):
                person = response.xpath('//pre1').re('.*?person:\s*(.*)')
                item['person'] = person#str(person[0])

            if response.xpath('//pre1').re('.*?address:\s*(.*)'):
                postalAddress = response.xpath('//pre1').re('.*?address:\s*(.*)')
                item['postalAddress'] = [str(e) for e in postalAddress]

            if response.xpath('//pre1').re('.*?phone:\s*(.*)'):
                phone = response.xpath('//pre1').re('.*?phone:\s*(.*)')
                item['phone'] = [str(e) for e in phone]

            if response.xpath('//pre1').re('.*?fax-?no:\s*(.*)'):
                faxNo = response.xpath('//pre1').re('.*?fax-?no:\s*(.*)')
                item['faxNo'] = [str(e) for e in faxNo]

            if response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)'):
                nicHdl = response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)')
                item['nicHdl'] = [str(e) for e in nicHdl]

            if response.xpath('//pre1').re('.*?route:\s*(.*)'):
                route = response.xpath('//pre1').re('.*?route:\s*(.*)')
                item['route'] = route#str(route[0])

            if response.xpath('//pre1').re('.*?origin:\s*(.*)'):
                origin = response.xpath('//pre1').re('.*?origin:\s*(.*)')
                item['origin'] = origin#str(origin[0])

            if response.xpath('//pre1').re('.*?member-?of:\s*(.*)'):
                memberOf = response.xpath('//pre1').re('.*?member-?of:\s*(.*)')
                item['memberOf'] = memberOf#str(memberOf[0])



            ###IP LOCATION###
            #get all location info
            location = response.xpath('//div[@class="span6"]//p//text()').extract()
            #populate data fields
            if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)'):
                item['country'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)')

            if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)'):
                latitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)')
                item['latitude'] = str(latitude[0])

            if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)'):
                longitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)')
                item['longitude'] = str(longitude[0])

            if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)'):
                callingCode = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)')
                item['callingCode'] = str(callingCode[0])

            if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)'):
                currency = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)')
                item['currency'] = str(currency[0])

            if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)'):
                item['capital'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)')

            if response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)'):
                item['region'] = response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)')

            if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)'):
                item['language'] = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)')


            item['sourceName'] = 'tordata5'
            
            yield item

        


#transfer to csv
#scrapy crawl exitnodes5a -o tor_exit_addresses7a.csv


