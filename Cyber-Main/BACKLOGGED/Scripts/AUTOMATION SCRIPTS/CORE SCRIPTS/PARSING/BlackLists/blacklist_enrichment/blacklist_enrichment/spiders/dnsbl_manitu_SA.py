# -*- coding: utf-8 -*-

import scrapy
import re
import json
import csv
import socket
from socket import getaddrinfo  #use to check for valid domain   => i.e. result = getaddrinfo("www.google.com", None)
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from blacklist_enrichment.items import ManituPartnersItem



class MayhemSpider(CrawlSpider):
    name = "dnsbl_manitu"

    def start_requests(self):
        url  = 'http://www.dnsbl.manitu.net/partners.php?language=en'
        yield Request(url, callback=self.parse_manitu)

      
    def parse_manitu(self, response):
        
        getall = response.xpath('//body').extract()
        getrows = getall[0].split('<tr>')
        cleanrows = [e for e in getrows if '<td' in e]
        cleanrows = [e for e in cleanrows if 'class="list_' in e]

        getcells = [e.split('<td') for e in cleanrows]
        cleancells = [[f.replace('\n', '') for f in e] for e in getcells]
        cleancells = [[f.replace('\t', '') for f in e] for e in cleancells]


        types = [re.match('.*?>(.*?)?<.*', str(e[1])).group(1) for e in cleancells]
        dns_server = [re.match('.*?>(.*?)?<.*', str(e[2])).group(1) for e in cleancells]
        ips = [re.match('.*?>(.*(?:<br>)?.*)<.*', str(e[3])).group(1) for e in cleancells]
        clean_ips = [e.split('<br>') for e in ips]

        provider_info = [e[4] for e in cleancells]

        provider_name = [re.match('.*<span class="providercontact">(.*?)?<.*', e).group(1) for e in provider_info]
        provider_address = [re.match('.*?class="providercontact">.*?<br>(.*?)?Telefon.*', e).group(1) if re.match('.*?class="providercontact">.*?<br>(.*?)?Telefon.*', e) else '' for e in provider_info]

        clean_address = [e.replace('<br>', '') for e in provider_address]
        clean_address = [e.replace('\r', '') for e in clean_address]

        provider_telephone = [re.match('.*?Telefon\s*(.*?)?<br>.*', e).group(1) if re.match('.*?Telefon\s*(.*?)?<br>.*', e) else '' for e in provider_info]
        provider_fax = [re.match('.*?Telefax\s*(.*?)?<br>.*', e).group(1) if re.match('.*?Telefax\s*(.*?)?<br>.*', e) else '' for e in provider_info]

        provider_email = [re.match('.*?<a href="(?:mailto:)?(.*?@.*?)"?>.*', e).group(1) if re.match('.*?<a href="(.*?@.*?)"?>.*', e) else '' for e in provider_info]

        provider_website = [re.match('.*?<a href="((?:http://)?www\..*?)?".*', e).group(1) if re.match('.*?<a href="((?:http://)?www\..*?)?".*', e) else '' for e in provider_info]
        clean_website = [e.replace('%20', '') for e in provider_website]


        for i, e in enumerate(types):

            item = ManituPartnersItem()

            item['DNS_Configuration_Type_Text'] = types[i]
            item['DNS_Server_URL'] = dns_server[i]
            item['IP_List'] = clean_ips[i]
            item['Provider_Name'] = provider_name[i]
            item['Provider_Address'] = clean_address[i]
            item['Provider_Telephone'] = provider_telephone[i]
            item['Provider_Fax'] = provider_fax[i]
            item['Provider_Email'] = provider_email[i]
            item['Provider_Website'] = clean_website[i]


            yield item


    #         #scrapy crawl dnsbl_manitu -o dnsbl_manitu_SA.csv