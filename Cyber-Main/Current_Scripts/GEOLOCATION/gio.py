#!/usr/bin/python
# This will be used for ISP Enrichment
import os
import json
import time
import csv
import sys
import re
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

pat = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'


def isIP(entry):
    test = re.findall(pat, entry)
    if test:
        return True
    else:
        return False


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def main_1(BGP, first_date, iplist, offenderClass):
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
    INPUT = iplist + '.ips'
    OUTPUT = iplist + '.gio'
    OFFENDER = offenderClass
    DOMAINS = open(iplist + '.domains').readlines()

    f = open(OUTPUT, 'w')
    f.write('pipelineid' + ',' + 'datauploadid' + ',' + 'uuid' + ',' + 'referential' + ',' + 'datasourcename' + ',' + 'date' + ',' + 'cog' + ',' + 'model' + ',' + 'concept'\
                    + ',' + 'segment' + ',' + 'pedigree' + ',' + 'confidence_score' + ',' + 'ipaddress' + ',' + 'ipaddress_int' + ',' + 'offenderclass' + ',' + 'first_observed_date' + ',' + 'first_observed_time' + ',' +\
                'most_recent_observation_date' + ',' + 'most_recent_observation_time' + ',' + 'total_observations' + ',' + 'blranking' + ',' + 'threat_score' + ',' + 'total_capabilities' + ',' +\
                'commvett' + ',' + 'commdatevett' + ',' + 'govvett' + ',' + 'govdatevett' + ',' +'countryabbrv' + ',' + 'country' + ',' +  'city' + ',' + 'coordinates' + ',' + 'geo_longitude' + ',' + 'geo_latitude'\
    + ',' + 'isp' + ',' +'domain' + ',' + 'netspeed' + ',' + 'network_asn' + ',' + 'network_class' + ',' + 'network_type' + ',' + 'active boolean' + ',' + 'insrtdttm' + ',' + 'updtdttm'+'\n')
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

            # entry['enr_zip'] = data['zip']

            # print DOMAINS
            # print data
            for entry, bgp, first, domain in zip(data, BGP, first_date, DOMAINS):
                temp = Get_Data(entry, types, f, bgp, first, domain)
                if temp is not None:
                        entries.append(temp)
                    #print entries

        #dictToCSV(entries, OUTPUT)


def Get_Data(data, types, f, bgp, first, domain):
    start_time = time.time()

    Status = data['status']
    entry = {}

    if Status == 'success' :
        #print data
        entry['pipelineid'] = ''
        entry['datauploadid'] = ''
        entry['uuid'] = ''
        entry['referential'] = ''
        entry['city'] = data['city'].replace(',', '.')
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
        entry['first_observed_date'] = first.strip().replace(',', '.')
        entry['first_observed_time'] = ''
        entry['most_recent_observation_date'] = '20160530'
        entry['most_recent_observation_time'] = '15:30'
        entry['total_observations'] = '14'
        entry['blranking'] = ''
        entry['threat_score'] = ''
        entry['total_capabilities'] = ''
        entry['commvett'] = ''
        entry['commdatevett'] = ''
        entry['govvett'] = ''
        entry['govdatevett'] = ''
        entry['countryabbrv'] = data['countryCode'].replace(',', '.')
        entry['country'] = data['country'].replace(',', '.')
        entry['city'] = data['city'].replace(',', '.')
        entry['coordinates'] = ''
        entry['geo_longitude'] = data['lon']
        entry['geo_latitude'] = data['lat']
        entry['isp'] = data['isp'].replace(',', '.')
        entry['domain'] = domain.strip().replace(',', '.')
        entry['netspeed'] = ''
        AS_value = re.findall("AS(\d+)",data['as'])
        if len(AS_value) > 0:
          AS_value = AS_value[0]
        else:
          AS_value = ''

        entry['network_asn'] = AS_value.replace(',', '.')
        entry['network_class'] = bgp.strip().replace(',', '.')
        entry['network_type'] = ''
        entry['active_boolean'] = 'true'
        entry['insrtdttm'] = ''
        entry['updtdttm'] = ''


        f.write(str(entry['pipelineid']) + ',' + str(entry['datauploadid']) + ',' + str(entry['uuid']) + ',' + str(entry['referential']) + ',' + str(entry['datasourcename']) + ',' + str(entry['date']) + ',' + str(entry['cog']) + ',' + str(entry['model']) + ',' + str(entry['concept'])\
        +','+ str(entry['segment']) + ',' + str(entry['pedigree']) + ',' + str(entry['confidence_score']) + ',' + str(entry['ipaddress']) + ',' + str(entry['ipaddress_int']) + ',' + str(entry['offenderclass']) + ',' + str(entry['first_observed_date']) + ',' + str(entry['first_observed_time']) + ',' +\
        str(entry['most_recent_observation_date']) + ',' + str(entry['most_recent_observation_time']) + ',' + str(entry['total_observations']) + ',' + str(entry['blranking']) + ',' + str(entry['threat_score']) + ',' + str(entry['total_capabilities']) + ',' +\
        str(entry['commvett']) + ',' + str(entry['commdatevett']) + ',' + str(entry['govvett']) + ',' + str(entry['govdatevett']) + ',' +str(entry['countryabbrv']) + ',' + str(entry['country']) + ',' +  str(entry['city']) + ',' + str(entry['coordinates']) + ',' + str(entry['geo_longitude']) + ',' + str(entry['geo_latitude'])\
        +','+str(entry['isp']) + ',' +str(entry['domain']) + ',' + str(entry['netspeed']) + ',' + str(entry['network_asn']) + ',' + str(entry['network_class']) + ',' + str(entry['network_type']) + ',' + str(entry['active_boolean']) + ',' + str(entry['insrtdttm']) + ',' + str(entry['updtdttm'])+'\n')

        #Query = data['query']
        Organization = data['org']


        return entry


def dictToCSV(dict, fname):
    keys = set().union(*(d.keys() for d in dict))
    #for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname+'.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dict)
        #print dict

if __name__ == "__main__":
    main_1()


"""
while ( True ) :

    if len(sys.argv) > 1:
            IP = sys.argv[1]
            if IP == 'myip'  or IP == 'ip' or IP == 'ownip' or IP == 'system' or IP == 'systemip' :
                IP = ''
    else:
            print ''
            IP = raw_input('Enter IP/Hostname : ')
            if IP :
                if IP == 'myip'  or IP == 'ip' or IP == 'ownip' or IP == 'system' or IP == 'systemip' :
                    IP = ''
                    Get_Data( IP )
                elif IP == 'exit' or IP == 'quit' :
                    print 'Good Bye ! '
                    time.sleep(1)
                    quit
                    break
                else :
                    Get_Data( IP )
"""
