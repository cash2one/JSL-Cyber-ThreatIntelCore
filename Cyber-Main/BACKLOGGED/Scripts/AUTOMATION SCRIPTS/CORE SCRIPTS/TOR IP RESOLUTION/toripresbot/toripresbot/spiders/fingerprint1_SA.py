#Seraphina Anderson, John Snow Labs, 15/1/2016

#Spider for generating fingerprint urls, and collecting data from urls of form:
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
    name = "toripres2a"
    def start_requests(self):
        url = 'https://check.torproject.org/exit-addresses'
        yield Request(url, callback=self.parse_url)
        
        
        

    def parse_url(self, response):
        #item = ExitNodesItem()
        data = response.xpath('//body//text()').extract()
        
        ###CREATE ITEM CONTAINER###
        entries = data[0].split('ExitNode')  
        entries.remove(entries[0])

        ###COLLECT DATA FOR EACH DATA FIELD###
        fingerPrints = [re.match('\s*(.*?)\\nPublished.*', str(e)).group(1) for e in entries if re.match('\s*(.*?)\\nPublished.*', e)]
        
        #generate URLs here, from fingerprints
        i = 0
        while i < len(fingerPrints):
            url = 'http://torstatus.rueckgr.at/router_detail.php?FP=' + str(fingerPrints[i])
            yield Request(url, callback=self.parse_fingerprints)
            i += 1
        



    def parse_fingerprints(self, response):
        item = TorIpResolutionItem()
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
        item['platformVersion'] = str(info1[8])
        
        
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

        #item['counter'] = i #for internal use
        item['sourceName'] = 'tordata7'
        
        yield item

        ###number of data items expecting:  ###

        ###########################################
        ###DATA FILES CREATED FROM THIS SCRAPPER###
        ###########################################
        
        #scrapy crawl fingerprints -o tor_exit_addresses3a.csv

        
        

