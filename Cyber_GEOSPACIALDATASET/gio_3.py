import os
import json
import time
import csv
import sys
import re
import socket
import sys
import threading
import Queue
import requests

reload(sys)
sys.setdefaultencoding("utf-8")

pat = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'

class Consumer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run(self):
        s = requests.Session()
        while True:
            ips = self._queue.get()
            if ips == 'quit':
                break
            Run_Chunk(ips,s)
	    self._queue.task_done()
        print self.getName() + " done!"

def build_worker_pool(queue, size):
	workers = []
	for _ in range(size):
		worker = Consumer(queue)
		worker.start()
		workers.append(worker)
	return workers

def isIP(entry):
    test = re.findall(pat, entry)
    if test:
        return True
    else:
        return False

OUTPUT = ""
CYKEY = ""

# noinspection PyBroadException,PyUnusedLocal,PyUnusedLocal
def main_1(iplist):
    global OUTPUT
    global CYKEY

    if os.environ.get('CYKEY') != None:
        CYKEY = os.environ.get('CYKEY')
    else:
        print("\n"
              "please provide api-ip.com batch key via CYKEY environment variale\n")
        sys.exit(1)

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
        sys.exit(1)

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

    queue = Queue.Queue(16)
    worker_threads = build_worker_pool(queue, 16)

    with open(INPUT) as inputFile:

        ips = []

        i = 1

        for line in inputFile:
            ips.append(line)
            x, y = divmod(i, 100)
            if y == 0:
                print i
                try:
                    queue.put(ips)
                except KeyboardInterrupt:
                    print "Ctrl-c"
                    for t in worker_threads:
                        queue.put('quit')
                    sys.exit(1)
                ips = []

            i = i + 1

        if i != 1 and len(ips) != 0:
            Run_Chunk(ips)
    for worker in worker_threads:
        queue.put('quit')
    for worker in worker_threads:
        worker.join()


def Run_Chunk(ips,s):
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

    r = s.post("https://pro.ip-api.com/batch?key=" + CYKEY, str(data))
    data = r.json()

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

if __name__ == "__main__":
    main_1(sys.argv[1])

