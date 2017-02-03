import re
import csv


#i Read a .MD file, extract all data fields, make a list, clean list
#ii Read .CSV file, get header, and make into a list


#1 Read .CSV and get header
with open('DNS_BL20160329_SA.csv', 'rb') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            header = row

#Clean out any spaces
header = [e.replace(' ', '') for e in header]

#print header

#2 Read .MD and get data fields from schema
with open('DNS_Blacklist.md', 'rb') as f:
    reader = f.read()
    content = reader.split('\n')
    #print reader
    for i, row in enumerate(content):
        if '## Schema' in row:
            body = content[i:]
            #print body
        else:
            row


#3 Test for data fields, and extract them into a list
schema = []
for e in body:
    if re.match('-\s*(.*)', e):
        field = re.match('-\s*(.*)', e).group(1)
        schema.append(field)

#clean out any spaces
schema = [e.replace(' ', '') for e in schema]

test = []
#4 Compare "header" list and "schema" list
for j, f in enumerate(schema):
    if header[j] != f:
        result = 'mismatch'
        test.append(result)
        print 'mismatch: ', f, header[j]
    else:
        result = 'match'
        test.append(result)
        print 'match!', f, header[j]

#5 Confirm that order of data fields in schema and dataset consistent
if 'mismatch' not in test:
    print 'data fields in schema and dataset are consistent!'
else:
    print 'dataset/reference file needs fixing!'












        
        
    
