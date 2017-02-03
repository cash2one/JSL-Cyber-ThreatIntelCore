import os
import json
import time
import csv
import sys
import re
import socket
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

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


# noinspection PyBroadException,PyUnusedLocal,PyUnusedLocal
def main_1(iplist):

    OUTPUT = ""

    if len(sys.argv) == 4:
        INPUT = sys.argv[1]
        OUTPUT = sys.argv[2]
        OFFENDER = sys.argv[3]
    elif len(sys.argv) == 3:
        INPUT = sys.argv[1]
        OUTPUT = sys.argv[2]
    elif len(sys.argv) == 2:
        INPUT = sys.argv[1]
    else:
        print("\n"
              "usage :\n"
              "    python ISP_ENRCH.py input_filename [output_filename]\n")

    INPUT = iplist
    if OUTPUT == "":
        OUTPUT = iplist + '.csv'

    f = open(OUTPUT, 'w')
    f.write('ipaddress,' + \
            'country,' + \
            'city,' + \
            'geo_longitude,' + \
            'geo_latitude,' + \
            'countryabbrv,' + \
            'isp,' + \
            'network_asn' + \
            '\n')
    f.close()

    with open(INPUT) as inputFile:

        ips = []

        i = 1

        for line in inputFile:
            ips.append(line)
            x, y = divmod(i, 100)
            if y == 0:
                print i
                Run_Chunk(ips, OUTPUT)
                ips = []

            i = i + 1

        if i != 1 and len(ips) != 0:
            Run_Chunk(ips, OUTPUT)

def Run_Chunk(ips, OUTPUT):
    data = '['
    for line in ips:

        line = line.replace('\n', '')
        line = line.replace('\r', '')
        if not isIP(line):
            if 'www.' in line:
                line = line[4:]

            try:
                line = socket.gethostbyname(line)
                # print "###################"
                # print line
            except:
                import traceback
                traceback.print_exc()

        data += ('{"query":  "' + line + '"},')

    data = data[:-1]
    data += ']'


    url = "curl --stderr /dev/null pro.ip-api.com/batch?key=Z9P32o57C0f7fye --data '" + str(data) + "'"

    data = os.popen(url).read()

    data = json.loads(data)

    # entry['enr_zip'] = data['zip']

    # print DOMAINS
    # print data
    f = open(OUTPUT, 'a')
    for entry in zip(data):
        temp = Get_Data(entry)
        if temp is not None:
            f.write(str(temp['ipaddress']) + ',' + \
                    str(temp['country']) + ',' + \
                    str(temp['city']) + ',' + \
                    str(temp['geo_longitude']) + ',' + \
                    str(temp['geo_latitude']) + ',' + \
                    str(temp['countryabbrv']) + ',' + \
                    str(temp['isp']) + ',' + \
                    str(temp['network_asn']) +
                    '\n')


# noinspection PyUnusedLocal,PyUnusedLocal
def Get_Data(data):
    start_time = time.time()
    data = data[0]
    Status = data['status']
    entry = {}

    if Status == 'success':
        # print data
        #entry['pipelineid'] = ''
        #entry['datauploadid'] = ''
        #entry['uuid'] = ''
        #entry['referential'] = ''
        entry['city'] = data['city'].replace(',', '.')
        #entry['datasourcename'] = 'jsl'
        #entry['date'] = ''
        #entry['cog'] = ''
        #entry['model'] = ''
        #entry['concept'] = ''
        #entry['segment'] = ''
        #entry['pedigree'] = ''
        #entry['confidence_score'] = '7'
        entry['ipaddress'] = data['query']
        #entry['ipaddress_int'] = ''
        #entry['offenderclass'] = ''
        #entry['first_observed_date'] = ''
        #entry['first_observed_time'] = ''
        #entry['most_recent_observation_date'] = '20160427'
        #entry['most_recent_observation_time'] = '20:14'
        #entry['total_observations'] = '9'
        #entry['blranking'] = ''
        #entry['threat_score'] = ''
        #entry['total_capabilities'] = ''
        #entry['commvett'] = ''
        #entry['commdatevett'] = ''
        #entry['govvett'] = ''
        #entry['govdatevett'] = ''
        entry['countryabbrv'] = data['countryCode'].replace(',', '.')
        entry['country'] = data['country'].replace(',', '.')
        entry['city'] = data['city'].replace(',', '.')
        #entry['coordinates'] = ''
        entry['geo_longitude'] = data['lon']
        entry['geo_latitude'] = data['lat']
        entry['isp'] = data['isp'].replace(',', '.')
        #entry['domain'] = ''
        #entry['netspeed'] = ''
        AS_value = re.findall("AS(\d+)", data['as'])
        if len(AS_value) > 0:
            AS_value = AS_value[0]
        else:
            AS_value = ''

        entry['network_asn'] = AS_value.replace(',', '.')
        #entry['network_class'] = ''
        #entry['network_type'] = ''
        #entry['active_boolean'] = 'true'
        #entry['insrtdttm'] = ''
        #entry['updtdttm'] = ''

        # Query = data['query']
        Organization = data['org']

        return entry


def dictToCSV(dict, fname):
    keys = set().union(*(d.keys() for d in dict))
    # for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname + '.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dict)
        # print dict


if __name__ == "__main__":
    main_1(sys.argv[1])

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
