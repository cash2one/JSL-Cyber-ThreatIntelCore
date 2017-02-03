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

    with open(INPUT) as inputFile:

        lines = inputFile.readlines()
        Chunks = chunks(lines, 100)

        entries = []
        for lines in Chunks:
            i = 0
            data = '['
            for line in lines:
                line = line.replace('\n','')
                if not isIP(line):
                    if 'www.' in line:
                        line = line[4:]

                    try:
                        line = socket.gethostbyname(line)
                    except:
                        import traceback
                        traceback.print_exc()

                data += ('{"query":  "'+line+'"},')
            data = data[:-1]
            data += ']'

            url = "curl pro.ip-api.com/batch?key=Z9P32o57C0f7fye --data '"+str(data)+"'"

            data = os.popen(url).read()

            data = json.loads(data)
            for entry in data:
                    temp = Get_Data(entry)
                    if temp is not None:
                        entries.append(temp)
                    #print entries
        dictToCSV(entries, OUTPUT)


def Get_Data(data):
    start_time = time.time()

    Status = data['status']
    entry = {}
    if Status == 'success' :
        entry['enr_city'] = data['city']

        entry['enr_country_code'] = data['countryCode']
        entry['enr_country'] = data['country']

        entry['enr_isp'] = data['isp']
        entry['lat'] = data['lat']
        entry['lon'] = data['lon']

        entry['enr_time_zone'] = data['timezone']
        entry['enr_as'] = data['as']
        entry['enr_as'] = data['as']
        entry['enr_query'] = data['query']
        entry['enr_region'] = data['regionName']
        entry['enr_region_name'] = data['regionName']
        entry['enr_region'] = data['region']
        entry['enr_zip'] = data['zip']

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
