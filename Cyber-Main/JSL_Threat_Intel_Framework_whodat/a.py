import csv


def write_final_output(dico):
    f = open("outputfile", 'w')
    f.write(
        'pipelineid' + ',' + 'datauploadid' + ',' + 'uuid' + ',' + 'referential' + ',' + 'datasourcename' + ',' + 'date' + ',' + 'cog' + ',' + 'model' + ',' + 'concept' \
        + ',' + 'segment' + ',' + 'pedigree' + ',' + 'confidence_score' + ',' + 'ipaddress' + ',' + 'ipaddress_int' + ',' + 'offenderclass' + ',' + 'first_observed_date' + ',' + 'first_observed_time' + ',' + \
        'most_recent_observation_date' + ',' + 'most_recent_observation_time' + ',' + 'total_observations' + ',' + 'blranking' + ',' + 'threat_score' + ',' + 'total_capabilities' + ',' + \
        'commvett' + ',' + 'commdatevett' + ',' + 'govvett' + ',' + 'govdatevett' + ',' + 'countryabbrv' + ',' + 'country' + ',' + 'city' + ',' + 'coordinates' + ',' + 'geo_longitude' + ',' + 'geo_latitude' \
        + ',' + 'isp' + ',' + 'domain' + ',' + 'netspeed' + ',' + 'network_asn' + ',' + 'network_class' + ',' + 'network_type' + ',' + 'active boolean' + ',' + 'insrtdttm' + ',' + 'updtdttm' + '\n')

    for entry in dico:
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
            entry['active boolean']) + ',' + str(entry['insrtdttm']) + ',' + str(entry['updtdttm']) + '\n')


with open('test.csv') as f:
    reader = csv.reader(f, skipinitialspace=True)
    header = next(reader)
    a = [dict(zip(header, map(str, row))) for row in reader]
write_final_output(a)
