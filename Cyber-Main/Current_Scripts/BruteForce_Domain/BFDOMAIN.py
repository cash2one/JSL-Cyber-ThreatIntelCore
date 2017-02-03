import tldextract

data = open('input')

lines = data.readlines()
elements = []
for line in lines:
    elements.append([element for element in line.strip().split(' ') if len(element) > 2])

nodes = {}

for element in elements:

    if element[1] in nodes.keys():

        nodes[element[1]] += ';' + (element[0])
    else:
        nodes[element[1]] = element[0]

# print nodes


print 'data_source_name,date,confidence_score,ipaddress,offenderclass,first_observed_date,most_recent_observation_date,most_recent_observation_time,total_observations,domain name,hostname,subdomains'

data_source_name = 'jsl'
date = '20160516'
confidence = '7'
offenderclass = 'dns_bl'
first_observed_date = '20160516'
most_recent_observation_date = '20160516'
most_recent_observation_time = '16:00'
total_observations = '1'
domain_name = ''
hostname = ''

for node in nodes.items():
    extracted = tldextract.extract(node[1].split(';')[0])
    domain_name = "{}.{}".format(extracted.domain, extracted.suffix)
    print '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
    data_source_name, date, confidence, node[0].replace(',', ''), offenderclass
    , first_observed_date, most_recent_observation_date, most_recent_observation_time,
    total_observations, domain_name, hostname, node[1])
