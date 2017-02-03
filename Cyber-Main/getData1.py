#Seraphina Anderson, John Snow Labs, 8/1/2016

###useful links###
#list of countries: http://www.state.gov/misc/list/
#Realtime blacklist, DNSBL or RBL

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
from torbots.items import TorbotsItem



class DataSpider1(CrawlSpider):
    name = "data1"
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #test urls - feed all data sources here
        #Do we want to process one URL at a time, or loop through them here?
        urls = ['http://www.dshield.org/ipsascii.html?limit=3000',
                'http://www.malwaredomainlist.com/hostslist/hosts.txt',
                'http://www.spamhaus.org/rokso/',
                'http://multirbl.valli.org/list/',
                'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist']
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_everything)
            i += 1
        

    #collect links here
    def parse_everything(self, response):
        item = TorbotsItem()
        #get everything
        everything = response.xpath('//body').extract()

        #using http://www.state.gov/misc/list/ 
        #countries = response.xpath('//blockquote[@dir="ltr"]//a/text()').extract()
        country_checklist = ['afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas, the', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bhutan', 'bolivia', 'bosnia and herzegovina', 'botswana', 'brazil', 'brunei ', 'bulgaria', 'burkina faso', 'burma', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'central african republic', 'chad', 'chile', 'china', 'colombia', 'comoros', 'congo, democratic republic of the', 'congo, republic of the', 'costa rica', "cote d'ivoire", 'croatia', 'cuba', 'curacao', 'cyprus', 'czech republic', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'timor-leste', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'fiji', 'finland', 'france', 'gabon', 'gambia, the', 'georgia', 'germany', 'ghana', 'greece', 'grenada', 'guatemala', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'holy see', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea, north', 'korea, south', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macau', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'mauritania', 'mauritius', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'morocco', 'mozambique', 'namibia', 'nauru', 'nepal', 'netherlands', 'netherlands antilles', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'north korea', 'norway', 'oman', 'pakistan', 'palau', 'palestinian territories', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal', 'qatar', 'romania', 'russia', 'rwanda', 'saint kitts and nevis', 'saint lucia', 'saint vincent and the grenadines', 'samoa ', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south korea', 'south sudan', 'spain ', 'sri lanka', 'sudan', 'suriname', 'swaziland ', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand ', 'timor-leste', 'togo', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'uruguay', 'uzbekistan', 'vanuatu', 'venezuela', 'vietnam', 'yemen', 'zambia', 'zimbabwe ', 'united states']
        
        
        
        #dataSourceLink
        get_dataSourceLink = response #this gets us current URL crawling!
        dataSourceLink = re.match('<200\s*(.*?)>', str(get_dataSourceLink)).group(1)
        
        #loop through these results - may need to include different arguments here
        #IPs come in different formats, ref: http://www.doc.gold.ac.uk/~mas01rk/Teaching/CIS110/notes/IP-Address.html
        #Determine info from IP address: https://www.iplocation.net/
        if response.xpath('//body').re('\d{3}\.\d{3}\.\d{3}'):
            ipFrom = response.xpath('//body').re('\d{3}\.\d{3}\.\d{3}')
        if response.xpath('//body').re(''):
            ipFrom = response.xpath('//body').re('\d+\.\d+\.\d+\.\d+')

        #this section can be refined, ref: https://en.wikipedia.org/wiki/Date_format_by_country, and
        #can test for formats accordingly, i.e. (dd/mm/yyyy), (dd.mm.yyyy), (yyyy-mm-dd), etc...
        if response.xpath('//body').re('.*((?:19|20)\d{2}\s*-\s*\d{2}\s*-\s*\d{2}.*(?:19|20)\d{2}\s*-\s*\d{2}\s*-\s*\d{2}).*'):
            dates = response.xpath('//body').re('.*((?:19|20)\d{2}\s*-\s*\d{2}\s*-\s*\d{2}.*(?:19|20)\d{2}\s*-\s*\d{2}\s*-\s*\d{2}).*')
            dateCreate = [e.replace('\t',', ') for e in dates]
        #this gives date overall document was created
        if response.xpath('//body').re('l?L?ast\s*-?\s*u?U?pdated\s*:?\s*(.*)'):
            date = response.xpath('//body').re('l?L?ast\s*-?\s*u?U?pdated\s*:?\s*(.*)')
            date = [e.replace('\t',', ') for e in date]
        
        #dataSourceKind
        if response.xpath('//html'):
            dataSourceKind = 'html'

        #no of hits corresponding to given dates
        if response.xpath('//body').re('.*(?:\d{3}\.\d{3}\.\d{3})(.*?\d+.*?\d+).*'):
            hits = response.xpath('//body').re('.*(?:\d{3}\.\d{3}\.\d{3})(.*?\d+.*?\d+).*')
            things = [e.replace('\t',', ') for e in hits]
        if response.xpath('//a[@class="listmenu"]').extract():
            things = response.xpath('//a[@class="listmenu"]').extract()
            things = [re.match('.*?title(.*?)?href.*', e).group(1) for e in things if re.match('.*?title(.*?)?href.*', e)]
            things = [e.replace('\'', '') for e in things]

        #name
        if response.xpath('//a[@class="listmenu"]/b/text()').extract():
            names = response.xpath('//a[@class="listmenu"]/b/text()').extract()
        if response.xpath('//body').re('.*(\s*.*?(?:www\.)?.*?(?:\.info|\.net|\.com|\.\w+)).*'):
            domains = response.xpath('//body').re('(?:\d+\.\d+\.\d+\.\d+)\s*.*(?:\.info|\.net|\.com|\.\w+)|localhost')

        #sourceName
        if response.xpath('//span[@class="pagetitle"]//text()').extract():
            sourceName = response.xpath('//span[@class="pagetitle"]//text()').extract()
            sourceName = sourceName[0].strip()

        #countries
        stuff = response.xpath('//tr//text()').extract()
        stuff = [e.lower() for e in stuff]
        countries = [e for e in stuff if e in country_check]
        
            
        
        
        ###collect data###

            
        i = 0
        while i < len(ipFrom):
            #test for data field
            if dates:
                item['dateCreate'] = dateCreate[i]
            if date:
                item['dateCreate'] = date  
            else:
                item['dateCreate'] = 'Null'
            if ipFrom:
                item['ipFrom'] = ipFrom[i]
            else:
                item['ipFrom'] = 'Null'
            if name:
                item['name'] = name[i]
            else:
                item['name'] = 'Null'
            if hits:
                item['things'] = things[i]
            else:
                item['things'] = 'Null'
            if sourceName:
                item['sourceName'] = sourceName
            else:
                item['sourceName'] = 'Null'
            item['dataSourceKind'] = dataSourceKind
            item['dataSourceLink'] = dataSourceLink
            
            yield item
            i += 1

