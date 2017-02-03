#!/usr/bin/python
# This will be used for ISP Enrichment

import unicodedata
import os
import json
import time
import csv
import sys
import requests
import re
import codecs

TOP_TEN = []
pat = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
patV4 = '(?:(?:[0-9][0-9][0-9])\\.){3}(?:[0-9][0-9][0-9])'
URL = "https://isc.sans.edu//top10.html"
protocols = {'tcp': 'False', 'udp': 'False', 'icmp': 'False'}
ports = {'ftp': 0, 'http': 0, 'smtp': 0, 'ssh': 0}


def ipsFromTxt(dump):
    ips = re.findall(patV4, dump)
    return ips


def cleanIps(ips):
    new_ips = []
    for ip in ips:
        parts = [int(p) for p in ip.split('.')]
        ipx = str(parts[0])
        for part in parts[1:]:
            ipx += '.'+str(part)
        new_ips.append(ipx)
    return new_ips


def getTopTen():
    response = requests.get(URL)
    ips = ipsFromTxt(response.content)
    return cleanIps(ips)


def isTopTen(ip):

    if ip in TOP_TEN:
        return True
    else:
        return False

def isIP(entry):
    test = re.findall(pat, entry)
    if test:
        return True
    else:
        return False


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def main_1(BGP, first_date, iplist, offenderClass, protocol, port):

    top_ten = getTopTen()

    '''
    if len(sys.argv) == 4:
        INPUT = sys.argv[1]
        OUTPUT = sys.argv[2]
        OFFENDER = sys.argv[3]
    else:
        print """
usage :
    python ISP_ENRCH.py input_filename output_filename
        """
    '''
    INPUT = iplist+'.ips'
    OUTPUT = iplist+'.gio'
    OFFENDER = offenderClass
    DOMAINS = open(iplist+'.domains').readlines()

    f = codecs.open(OUTPUT, 'a', 'utf-8')
    f.write('pipelineid,datauploadid,uuid,referential,datasourcename,date,cog,model,concept,segment,pedigree,confidence_score,ipaddress,ipaddress_int,offenderclass,first_observed_date,first_observed_time,most_recent_observation_date,most_recent_observation_time,total_observations,blranking,threat_score,total_capabilities,commvett,commdatevett,govvett,govdatevett,countryabbrv,country,city,coordinates,geo_longitude,geo_latitude,isp,domain,netspeed,network_asn,network_class,network_type,active_boolean,insrtdttm,updtdttm,tcp,udp,icmp,reports,targets,sources,topTen,dateCreated,port,verified,name,description,dateModified,categories\n'
    )
    with open(INPUT) as inputFile:

        lines = inputFile.readlines()
        ips = []

        for line in lines:
            ips.append(line)
            #dico[line.split(',')[0]] = line.split(',')[1]
        Chunks = chunks(ips, 100)
  	types = offenderClass
	entries = []
        for lines in Chunks:
            i = 0
            data = '['
            for line in lines:

                line = line.replace('\n','')
                line = line.replace('\r','')

                data += ('{"query":  "'+line+'"},')

            data = data[:-1]
            data += ']'
            url = "curl pro.ip-api.com/batch?key=Z9P32o57C0f7fye --data '"+str(data)+"'"
            data = os.popen(url).read()
            data = json.loads(data)

            for entry, bgp, first, domain in zip(data, BGP, first_date, DOMAINS):
                    temp = Get_Data(entry, types, f, bgp, first, domain, protocol, port)
                    if temp is not None:
                        entries.append(temp)


def Get_Data(data, types, f, bgp, first, domain, protocol, port):
    start_time = time.time()

    Status = data['status']
    entry = {}
    protocols[protocol] = True
    if Status == 'success' :

        AS_value = re.findall("AS(\d+)", data['as'])
        if len(AS_value) > 0:
            AS_value = AS_value[0]
        else:
            AS_value = ''

        entry['pipelineid'] = ''
        entry['datauploadid'] = ''
        entry['uuid'] = ''
        entry['referential'] = ''
        entry['datasourcename'] = 'jsl'
        entry['date'] = ''
        entry['cog'] = ''
        entry['model'] = ''
        entry['concept'] = ''
        entry['segment'] = ''
        entry['pedigree'] = ''
        entry['confidence_score'] = '7'
        entry['ipaddress'] = data['query']
        entry['ipaddress_int'] = ''
        entry['offenderclass'] = types
        entry['first_observed_date'] = first.strip().replace(',','.')
        entry['first_observed_time'] = ''
        entry['most_recent_observation_date'] = '20160511'
        entry['most_recent_observation_time'] = '18:17'
        entry['total_observations'] = '11'
        entry['blranking'] = ''
        entry['threat_score'] = ''
        entry['total_capabilities'] = ''
        entry['commvett'] = ''
        entry['commdatevett'] = ''
        entry['govvett'] = ''
        entry['govdatevett'] = ''
        entry['countryabbrv'] = data['countryCode'].replace(',', '.')
        entry['country'] = unicodedata.normalize('NFKD', data['country'].replace(',', '.')).encode('ascii','ignore')
        entry['city'] = unicodedata.normalize('NFKD', data['city'].replace(',', '.')).encode('ascii','ignore')
        entry['coordinates'] = ''
        entry['geo_longitude'] = data['lon']
        entry['geo_latitude'] = data['lat']
        entry['isp'] = unicodedata.normalize('NFKD', data['isp'].replace(',', '.')).encode('ascii','ignore')
        entry['domain'] = domain.strip().replace(',','.')
        entry['netspeed'] = ''
        entry['network_asn'] = AS_value.replace(',','.')
        entry['network_class'] = bgp.strip().replace(',','.')
        entry['network_type'] = ''
        entry['active_boolean'] = 'true'
        entry['insrtdttm'] = ''
        entry['updtdttm'] = ''
        entry['tcp'] = protocols['tcp']
        entry['udp'] = protocols['udp']
        entry['icmp'] = protocols['icmp']
        entry['reports'] = ''
        entry['targets'] = ''
        entry['sources'] = ''
        entry['topTen'] = str(isTopTen(data['query']))
        entry['dateCreated'] = ''
        entry['port'] = port
        entry['verified'] = ''
        entry['name'] = ''
        entry['description'] = ''
        entry['dateModified'] = ''
        entry['categories'] = ''



        string = str(entry['pipelineid']) + ',' + str(entry['datauploadid']) + ',' + str(entry['uuid']) + ',' + str(entry['referential']) + ',' + str(entry['datasourcename']) + ',' + str(entry['date']) + ',' + str(entry['cog']) + ',' + str(entry['model']) + ',' + str(entry['concept']) + ',' + str(entry['segment']) + ',' + str(entry['pedigree']) + ',' + str(entry['confidence_score']) + ',' + str(entry['ipaddress']) + ',' + str(entry['ipaddress_int']) + ',' + str(entry['offenderclass']) + ',' + str(entry['first_observed_date']) + ',' + str(entry['first_observed_time']) + ',' + str(entry['most_recent_observation_date']) + ',' + str(entry['most_recent_observation_time']) + ',' + str(entry['total_observations']) + ',' + str(entry['blranking']) + ',' + str(entry['threat_score']) + ',' + str(entry['total_capabilities']) + ',' + str(entry['commvett']) + ',' + str(entry['commdatevett']) + ',' + str(entry['govvett']) + ',' + str(entry['govdatevett']) + ',' + str(entry['countryabbrv']) + ',' + str(entry['country']) + ',' + entry['city'] + ',' + str(entry['coordinates']) + ',' + str(entry['geo_longitude']) + ',' + str(entry['geo_latitude']) + ',' + str(entry['isp']) + ',' + str(entry['domain']) + ',' + str(entry['netspeed']) + ',' + str(entry['network_asn']) + ',' + str(entry['network_class']) + ',' + str(entry['network_type']) + ',' + str(entry['active_boolean']) + ',' + str(entry['insrtdttm']) + ',' + str(entry['updtdttm']) + ',' + str(entry['tcp']) + ',' + str(entry['udp']) + ',' + str(entry['icmp']) + ',' + str(entry['reports']) + ',' + str(entry['targets']) + ',' + str(entry['sources']) + ',' + str(entry['topTen']) + ',' + str(entry['dateCreated']) + ',' + str(entry['port']) + ',' + str(entry['verified']) + ',' + str(entry['name']) + ',' + str(entry['description']) + ',' + str(entry['dateModified']) + ',' + str(entry['categories']) +'\n'

        f.write(string)
        Organization = data['org']

        return entry




if __name__ == "__main__":
    main_1()