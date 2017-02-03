#Seraphina Anderson, John Snow Labs, 26/2/2016

# -*- coding: utf-8 -*-


import whois
import scrapy
import re
import json
import csv
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CSVFeedSpider
from blacklist_enrichment.items import SSLExtendedItem



class SSLExtendedSpider(CSVFeedSpider):
    name = 'ssextended'
    allowed_domains = ['sslbl.abuse.ch']
    start_urls = ['https://sslbl.abuse.ch/downloads/ssl_extended.csv']
    delimiter = ','
    quotechar = "'"
    headers = ['Timestamp of Listing (UTC)', 'Referencing Sample (MD5)', 'Destination IP', 'Destination Port', 'SSL certificate SHA1 Fingerprint', 'Listing reason']


    def parse_row(self, response, row):
        self.logger.info('Hi, this is a row!: %r', row)

        item = SSLExtendedItem()
        item['UTC_Listing_Timestamp'] = row['Timestamp of Listing (UTC)']
        item['MD5_Referencing_Sample_Text'] = row['Referencing Sample (MD5)']
        item['Destination_IP'] = row['Destination IP']
        item['Destination_Port_Number'] = row['Destination Port']
        item['SSL_Certificate_SHA1_Fingerprint_Text'] = row['SSL certificate SHA1 Fingerprint']
        item['Listing_Reason_Text'] = row['Listing reason']

        return item

