import os
import re
import csv
import json
PAT_IPV4 = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
PAT_IPV6 = '(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)'

def cleanse(input):

    input = input.replace('\t', '')
    input = input.replace('\n', '')
    input = input.replace('\r', '')
    input = input.replace('"', '')

    return input


def dictToCSV(dict, fname):
    temp = []

    for elmt in dict:
        if elmt is not None:
            temp.append(elmt)

    dict = temp

    keys = set().union(*(d.keys() for d in dict))
    #for i in range (0, len(keys)):
    #    keys[i] = keys[i].replace(' ', '_')
    with open(fname+'.csv', 'wb') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(dict)
        print dict


def Get_Data(ip):

    #url = 'http://ip-api.com/json/%s' %IP

    url = 'curl http://pro.ip-api.com/json/%s?key=Z9P32o57C0f7fye' % ip
    print url
    data = os.popen(url).read()


    #url = 'http://pro.ip-api.com/json/%s?key=Z9P32o57C0f7fye' %IP

    #data = json.load(urllib2.urlopen(url))
    data = json.loads(data)
    Status = data['status']
    entry = {}
    if Status == 'success' :

        entry['country_code'] = data['countryCode']
        entry['asn_number'] = data['as']

        return entry



def listToUSV(input):

    output = ""
    for element in input:
        output += element+"_"

    output = output[:-1]

    return output

def match_IPV(input, version):

    if version == 4:
        pat = PAT_IPV4
    elif version == 6:
        pat = PAT_IPV6

    test = re.findall(pat, input)
    if test:
       return test
    else:
       return None



CMD_PTR = "dig -x %s +short"
CMD_MX = "dig mx %s +short"
CMD_TXT = "dig -t txt %s +short"
CMD_SOA = "dig %s SOA +short"
CMD_A = "host -t A %s"
CMD_4A = "host -t AAAA %s "
CMD_CNAME = "host -t cname %s"
CMD_NS = "nslookup -query=ns %s"
CMD_SERVER_NAME = "nslookup %s "

IP = "80.88.15.48"

def process(IP):
    ENTRY = Get_Data(IP)

    ENTRY['ip_address'] = IP
    print CMD_PTR % IP
    host_name = os.popen(CMD_PTR % IP).read()
    print host_name
    print ""
    if 'no servers' in host_name:
        ENTRY['ptr'] = ''
        return ENTRY

    host_name = host_name.split('\n')
    host_name = [x for x in host_name if x]
    #host_name = host_name[:-1]
    print host_name
    print ""

    for i in range(len(host_name)):
        if 'www' in host_name[i]:

            host_name[i] = host_name[i][4:]

    ENTRY['ptr'] = listToUSV(host_name)

    if ENTRY['ptr'] == '' or ENTRY['ptr'] is None:
        return ENTRY

    print "########## PTR"

    all_mx_entries = []
    for host in host_name:

        print CMD_MX % host
        data = os.popen(CMD_MX % host).read()

        mx_entries = data.split('\n')
        for entry in mx_entries:
            if entry != '':
                all_mx_entries.append(entry)

    ENTRY['mx'] = listToUSV(all_mx_entries)
    print "########## MX"

    all_txt_entries = []
    for host in host_name:

        print CMD_TXT % host
        data = os.popen(CMD_TXT % host).read()
        #txt_entries = data.split('\n')
        #for entry in txt_entries:
        if data != '':

            all_txt_entries.append(cleanse(data))
    ENTRY['txt'] = listToUSV(all_txt_entries)

    print "########## TXT"

    all_soa_entries = []
    for host in host_name:
        print CMD_SOA % host
        data = os.popen(CMD_SOA % host).read()
        #soa_entries = data.split('\n')
        #for entry in soa_entries:
        if entry != '':
            all_soa_entries.append(data)

    ENTRY['SOA'] = listToUSV(all_soa_entries)
    print "########## SOA"

    all_a_entries = []
    for host in host_name:
        print CMD_A % host
        data = os.popen(CMD_A % host).read()
        if match_IPV(data, 4) is not None:
            all_a_entries += match_IPV(data, 4)
        #a_entries = data.split('\n')
        #for entry in a_entries:
        #    if entry != '':
        #        all_a_entries.append(entry)


    ENTRY['A'] = listToUSV(all_a_entries)
    print "########## A"

    all_4a_entries = []
    for host in host_name:

        print CMD_4A % host
        data = os.popen(CMD_4A % host).read()
        if match_IPV(data, 6) is not None:
            all_4a_entries += match_IPV(data, 6)
        #a4_entries = data.split('\n')
        #for entry in a4_entries:
        #    if entry != '':
        #        all_4a_entries.append(entry)
    ENTRY['AAAA'] = listToUSV(all_4a_entries)
    print "########## AAAA"

    all_cname_entries = []
    for host in host_name:

        print CMD_CNAME % host
        data = os.popen(CMD_CNAME % host).read()
        cname_entries = data.split('\n')
        for entry in cname_entries:
            if entry != '' and "no CNAME" not in entry and "not found" not in entry:
                all_cname_entries.append(entry)


    ENTRY['CNAME'] = listToUSV(all_cname_entries)

    print "########## CNAME"

    all_ns_entries = []
    for host in host_name:
        print CMD_NS % host
        data = os.popen(CMD_NS % host).read()
        ns_entries = data.split('\n')
        for entry in ns_entries:
            if entry != '':
                if 'nameserver' in entry:
                    entry = entry.split(" = ")[1]
                    all_ns_entries.append(entry)

    all_ns_entries = list(set(all_ns_entries))
    ENTRY['Ns'] = listToUSV(all_ns_entries)
    print "########## NS"

    all_sname_entries = []
    if True:
    #for host in host_name:
        print CMD_SERVER_NAME  % IP

        data = os.popen(CMD_SERVER_NAME % IP).read()
        sname_entries = data.split('\n')

        for entry in sname_entries:
            if 'Server:' in entry:
                entry = entry.split(":")[1]
                entry = entry.replace("\t", "")
                all_sname_entries.append(entry)
    all_sname_entries = list(set(all_sname_entries))
    ENTRY['Server_name'] = listToUSV(all_sname_entries)
    print "########## SERVER_NAME"
    return ENTRY

if __name__ == '__main__':

    with open("ips.txt") as inputFile:

        lines = inputFile.readlines()
        all_data = []
        for line in lines:
            line = line.replace('\n', '')

            all_data.append(process(line))

        dictToCSV(all_data, 'zone_field')
