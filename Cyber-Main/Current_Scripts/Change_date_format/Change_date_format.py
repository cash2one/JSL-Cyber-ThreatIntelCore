
import datetime
import glob
import shutil
import os
import csv

def split(filehandler, delimiter=',', row_limit=10000,
          output_name_template='output_%s.csv', output_path='.', keep_headers=True):
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)

def write_final_output(dico, outputname):
    # if not os.path.exists('./splited/'+outputname + '_modified'):
    #   os.makedirs('./splited/'+outputname + '_modified')

    f = open('./splited/' + outputname + '_', 'w')
    f.write(
        'pipelineid' + ',' + 'datauploadid' + ',' + 'uuid' + ',' + 'referential' + ',' + 'datasourcename' + ',' + 'date' + ',' + 'cog' + ',' + 'model' + ',' + 'concept' \
        + ',' + 'segment' + ',' + 'pedigree' + ',' + 'confidence_score' + ',' + 'ipaddress' + ',' + 'ipaddress_int' + ',' + 'offenderclass' + ',' + 'first_observed_date' + ',' + 'first_observed_time' + ',' + \
        'most_recent_observation_date' + ',' + 'most_recent_observation_time' + ',' + 'total_observations' + ',' + 'blranking' + ',' + 'threat_score' + ',' + 'total_capabilities' + ',' + \
        'commvett' + ',' + 'commdatevett' + ',' + 'govvett' + ',' + 'govdatevett' + ',' + 'countryabbrv' + ',' + 'country' + ',' + 'city' + ',' + 'coordinates' + ',' + 'geo_longitude' + ',' + 'geo_latitude' \
        + ',' + 'isp' + ',' + 'domain' + ',' + 'netspeed' + ',' + 'network_asn' + ',' + 'network_class' + ',' + 'network_type' + ',' + 'active boolean' + ',' + 'insrtdttm' + ',' + 'updtdttm' + '\n')

    for entry in dico:
        active_boolean = 'active boolean'
        if 'active_boolean' in entry.keys():
            active_boolean = 'active_boolean'

        try:
            f.write(str(entry['pipelineid']) + ',' + str(entry['datauploadid']) + ',' + str(entry['uuid']) + ',' + str(
            entry['referential']) + ',' + str(entry['datasourcename']) + ',' + str(entry['date']) + ',' + str(
            entry['cog']) + ',' + str(entry['model']) + ',' + str(entry['concept']) \
                    + ',' + str(entry['segment']) + ',' + str(entry['pedigree']) + ',' + str(
            entry['confidence_score']) + ',' + str(entry['ipaddress']) + ',' + str(entry['ipaddress_int']) + ',' + str(
            entry['offenderclass']) + ',' + str(entry['first_observed_date']) + ',' + str(
            entry['first_observed_time']) + ',' + \
                    str(entry['most_recent_observation_date']) + ',' + str(
            entry['most_recent_observation_time']) + ',' + str(entry['total_observations']) + ',' + str(
            entry['blranking']) + ',' + str(entry['threat_score']) + ',' + str(entry['total_capabilities']) + ',' + \
                    str(entry['commvett']) + ',' + str(entry['commdatevett']) + ',' + str(entry['govvett']) + ',' + str(
            entry['govdatevett']) + ',' + str(entry['countryabbrv']) + ',' + str(entry['country']) + ',' + str(
            entry['city']) + ',' + str(entry['coordinates']) + ',' + str(entry['geo_longitude']) + ',' + str(
            entry['geo_latitude']) \
                    + ',' + str(entry['isp']) + ',' + str(entry['domain']) + ',' + str(entry['netspeed']) + ',' + str(
            entry['network_asn']) + ',' + str(entry['network_class']) + ',' + str(entry['network_type']) + ',' + str(
                entry[active_boolean]) + ',' + str(entry['insrtdttm']) + ',' + str(entry['updtdttm']) + '\n')
        except:
            import traceback
            # traceback.print_exc()
            # print entry.keys()
            # print active_boolean

def datemodify(filename):
    name = filename
    with open('./splited/' + filename) as f:
        reader = csv.reader(f, skipinitialspace=True)
        header = next(reader)
        a = [dict(zip(header, map(str, row))) for row in reader]
    for key in a:
        # print key
        first_date = 'first_observed_date '
        if first_date not in key.keys():
            first_date = 'first_observed_date'
        try:
            date = key[first_date]
        except:
            print key
            print filename
        date = date.strip()
        print date
        if 'c    2007-10-' in date:
            print key
            date = "2007-10-01"
        if date.endswith('-'):
            date += "01"
        if date.startswith('c'):
            date = date[5:]
        if date.endswith('-0'):
            date += '1'
        if date.endswith('C') or date.endswith('S') or date.endswith('E') or date.endswith('B') or date.endswith(
                'U') or date.endswith('K') or date.endswith('R') \
                or date.endswith('A') or date.__contains__('T') or date.endswith('D'):
            print date + "***********"
            date = date[:-3]
            print date + "***********"
            date = '2' + date
        if date.startswith('00'):
            date = '2' + date

        if date in first_date or len(date) == 1 or len(date) == 2:
            continue
        if "-" not in date:
            print filename
            if len(date.split('/')[2]) > 2:
                date = datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%Y%m%d")
                key[first_date] = date
            else:
                date = datetime.datetime.strptime(date, "%m/%d/%y").strftime("%Y%m%d")
                key[first_date] = date

        else:
            if len(date) > 7:
                date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
                key[first_date] = date
            else:
                date = datetime.datetime.strptime(date, "%m-%d-%y").strftime("%Y%m%d")
                key[first_date] = date






                # date2 = key['most_recent_observation_date']

    #print name
    write_final_output(a, name)


# datemodify('test.csv')


def Load1(Folder):
    # Find Script Files:
    Files = glob.glob(os.path.join(Folder, "*.csv"))
    # print "Found %d  Files to change date" % (len(Files))

    # Load scripts:
    loaded = []
    for File in Files:
        # Get full module name:
        fileName = os.path.basename(File)
        folderName = os.path.basename(Folder)
        fullModuleName = "%s/%s" % (folderName, fileName)

        loaded.append(fullModuleName)

    return loaded

def Load(Folder):

    # Find Script Files:
    Files = glob.glob(os.path.join(Folder, "*.csv"))
    # print "Found %d Files to split" % (len(Files))

    # Load scripts:
    loaded = []
    for File in Files:
        # Get full module name:
        fileName = os.path.basename(File)
        folderName = os.path.basename(Folder)
        fullModuleName = "%s" % (fileName)

        loaded.append(fullModuleName)

    return loaded


def concat(outfilename, Folder):

    interesting_files = glob.glob(os.path.join(Folder, "*.csv_"))

    header_saved = False
    with open('./splited/' + outfilename + '_concatene', 'wb') as fout:
        for filename in interesting_files:
            with open(filename) as fin:
                header = next(fin)
                if not header_saved:
                    fout.write(header)
                    header_saved = True
                for line in fin:
                    fout.write(line)

loadedfiles = Load('')

if not os.path.exists('splited'):
    os.makedirs('splited')

for filenotsplited in loadedfiles:
    # print file+' est un csv a spliter'
    if not os.path.exists('./splited/' + filenotsplited + 'splited'):
        os.makedirs('./splited/' + filenotsplited + 'splited')
    split(open(filenotsplited, 'rU'), ',', 10000, filenotsplited + '_%s.csv', './splited/' + filenotsplited + 'splited',
          True)
    splited = Load1('./splited/' + filenotsplited + 'splited')
    for file in splited:
        # print file +'sa date va etre modifier'
        datemodify(file)
    #print filenotsplited + 'regardez moi ca'
    concat(filenotsplited, './splited/' + filenotsplited + 'splited')

#splited=Load1('./splited')

# for file in splited:
# print file +'sa date va etre modifier'
#datemodify(file)
