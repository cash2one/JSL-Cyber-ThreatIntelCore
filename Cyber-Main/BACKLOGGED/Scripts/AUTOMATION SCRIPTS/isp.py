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

def main():

    if len(sys.argv) == 3:
        INPUT = sys.argv[1]
        OUTPUT = sys.argv[2]
    else:
        print """
usage :
    python ISP_ENRCH.py input_filename output_filename
        """
        return
    f = open(OUTPUT, 'w')
    f.write('datauploadid' + ',' + 'uuid' + ',' + 'referential' + ',' + 'datasourcename' + ',' + 'date' + ',' + 'cog' + ',' + 'model' + ',' + 'concept'\
                    + ',' + 'segment' + ',' + 'pedigree' + ',' + 'confidence_score' + ',' + 'ipaddress' + ',' + 'ipaddress_int' + ',' + 'offenderclass' + ',' + 'first_observed_date' + ',' + 'first_observed_time' + ',' +\
                'most_recent_observation_date' + ',' + 'most_recent_observation_time' + ',' + 'total_observations' + ',' + 'blranking' + ',' + 'threat_score' + ',' + 'total_capabilities' + ',' +\
                'commvett' + ',' + 'commdatevett' + ',' + 'govvett' + ',' + 'govdatevett' + ',' +'countryabbrv' + ',' + 'country' + ',' +  'city' + ',' + 'coordinates' + ',' + 'geo_longitude' + ',' + 'geo_latitude'\
    + ',' + 'isp' + ',' +'domain' + ',' + 'netspeed' + ',' + 'network_asn' + ',' + 'network_class' + ',' + 'network_type' + ',' + 'active boolean' + ',' + 'insrtdttm' + ',' + 'updtdttm'+'\n')

    with open(INPUT) as inputFile:

        lines = inputFile.readlines()
        Chunks = chunks(lines, 100)
  	types = {}
	entries = []
        for lines in Chunks:
            i = 0
            data = '['
            for line in lines:
		types[line.split(',')[0]] = line.split(',')[1]
		line = line.split(',')[0]
                line = line.replace('\n','')
                if not isIP(line):
                    if 'www.' in line:
                        line = line[4:]

                    try:
                        line = socket.gethostbyname(line)
                    except:
                        import traceback
                        #traceback.print_exc()

                data += ('{"query":  "'+line+'"},')
            data = data[:-1]
            data += ']'

            url = "curl pro.ip-api.com/batch?key=Z9P32o57C0f7fye --data '"+str(data)+"'"

            data = os.popen(url).read()

            data = json.loads(data)


        #entry['enr_zip'] = data['zip']


            for entry in data:
                    temp = Get_Data(entry,types, f)
                    if temp is not None:
                        entries.append(temp)
                    #print entries

        #dictToCSV(entries, OUTPUT)


def Get_Data(data, types, f):
    start_time = time.time()

    Status = data['status']
    entry = {}
    if Status == 'success' :


        entry['city'] = data['city'].replace(',', '.')

        entry['countryabbrv'] = data['countryCode'].replace(',', '.')
        entry['country'] = data['country'].replace(',', '.')
        entry['piplelineid'] = ''
        entry['datauploadid'] = ''
        entry['uuid'] = ''
        entry['referential'] = ''
        entry['datasourcename'] = 'jsl'
        entry['date'] = ''
        entry['cog'] = ''
        #entry['cog'] = ''
        entry['model'] = ''
        entry['concept'] = ''
        entry['segment'] = ''
        entry['pedigree'] = ''
        entry['confidence_score'] = '7'
        entry['first_observed_date'] = ''
        entry['first_observed_time'] = ''
        entry['most_recent_observation_date'] = '20160317'
        entry['most_recent_observation_time'] = '1751'
        entry['total_observations'] = '2'
        entry['blranking'] = ''
        entry['threat_score'] = ''
        entry['total_capabilities'] = ''
        entry['commvett'] = ''
        entry['commdatevett'] = ''
        entry['govvett'] = ''
        entry['govdatevett'] = ''
        entry['coordinates'] = ''
        entry['domain'] = ''
        entry['netspeed'] = ''
        entry['network_class'] = ''
        entry['network_type'] = ''
        entry['active boolean'] = 'true'
        entry['insrtdttm'] = ''
        entry['updtdttm'] = ''

        entry['isp'] = data['isp'].replace(',', '.')
        entry['geo_latitude'] = data['lat']
        entry['geo_longitude'] = data['lon']

        #entry['enr_time_zone'] = data['timezone']
        #entry['enr_as'] = data['as']
        entry['network_asn'] = data['as'].replace(',', '.')
        entry['offenderclass'] = types[data['query']].replace('\n','')
        entry['ipaddress'] = data['query']
        entry['ipaddress_int'] = ''
        #entry['enr_region'] = data['regionName']
        #entry['enr_region_name'] = data['regionName']
        #entry['enr_region'] = data['region']
        #entry['enr_zip'] = data['zip']

        f.write(str(entry['datauploadid']) + ',' + str(entry['uuid']) + ',' + str(entry['referential']) + ',' + str(entry['datasourcename']) + ',' + str(entry['date']) + ',' + str(entry['cog']) + ',' + str(entry['model']) + ',' + str(entry['concept'])\
            +','+ str(entry['segment']) + ',' + str(entry['pedigree']) + ',' + str(entry['confidence_score']) + ',' + str(entry['ipaddress']) + ',' + str(entry['ipaddress_int']) + ',' + str(entry['offenderclass']) + ',' + str(entry['first_observed_date']) + ',' + str(entry['first_observed_time']) + ',' +\
        str(entry['most_recent_observation_date']) + ',' + str(entry['most_recent_observation_time']) + ',' + str(entry['total_observations']) + ',' + str(entry['blranking']) + ',' + str(entry['threat_score']) + ',' + str(entry['total_capabilities']) + ',' +\
        str(entry['commvett']) + ',' + str(entry['commdatevett']) + ',' + str(entry['govvett']) + ',' + str(entry['govdatevett']) + ',' +str(entry['countryabbrv']) + ',' + str(entry['country']) + ',' +  str(entry['city']) + ',' + str(entry['coordinates']) + ',' + str(entry['geo_longitude']) + ',' + str(entry['geo_latitude'])\
        +','+str(entry['isp']) + ',' +str(entry['domain']) + ',' + str(entry['netspeed']) + ',' + str(entry['network_asn']) + ',' + str(entry['network_class']) + ',' + str(entry['network_type']) + ',' + str(entry['active boolean']) + ',' + str(entry['insrtdttm']) + ',' + str(entry['updtdttm'])+'\n')

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
    main()


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


