
import csv

new_rows = []

#check against client schema
new_schema = ['datauploadid', 'uuid', 'referential', 'datasourcename', 'date', 'cog', 'model', 'concept', 'segment', 'pedigree', 'confidence_score', 'ipaddress', 'ipaddress_int', 'offenderclass', 'first_observed_date', 'first_observed_time', 'most_recent_observation_date', 'most_recent_observation_time', 'total_observations', 'blranking', 'threat_score', 'total_capabilities', 'commvett', 'commdatevett', 'govvett', 'govdatevett', 'countryabbrv', 'country', 'city', 'coordinates', 'geo_longitude', 'geo_latitude', 'isp', 'domain', 'netspeed', 'network_asn', 'network_class', 'network_type', 'active boolean', 'insrtdttm', 'updtdttm']

#Get header
#Get body of data
#Test against the following datasets:
##SSL_BL20160329.csv
##TOR_BL20160329.csv
##SPAM_BL20160324.csv
##DNS_BL20160324.csv
##PHISHING_BL20160324.csv
with open('SSL_BL20160329.csv', 'rb') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            header = row
        else:
            new_rows.append(row)

###TEST FOR TYPOS###

for i, e in enumerate(header):
    if new_schema[i] != e:
        print "Correct spelling: ", e, '=> ', new_schema[i]
    else:
        print "all good: ", e, new_schema[i], i


###CORRECT HEADER###

##new_headers = []
##for j, e in enumerate(header):
##    field = new_header[j]
##    new_headers.append(field)
##    
##dataset = []
##
###Generate new dataset, with correct headers
##dataset.append(new_headers)
##
##for e in new_rows:
##    dataset.append(e)
##
##
##
##with open('DNS_BL20160329_SA.csv', 'wb') as f:
##    # Overwrite the old file with the modified rows
##    writer = csv.writer(f)
##    writer.writerows(dataset)
##
##f.close()
##


###NEED TO CORRECT THE FOLLOWING##########################################
#1 Get rid of " " from headers
#2 Get rid of all spaces in headers
#3 Get rid of all illegal characters in header - i.e. "+"'s
#4 Remove '_' from filenames
#5 Empty columns
#6 Check for typos
##########################################################################















