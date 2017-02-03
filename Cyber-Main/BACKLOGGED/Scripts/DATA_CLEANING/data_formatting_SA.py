# -*- coding: utf-8 -*-

import re
import os
import csv
import textwrap

schema = ['Data_Upload_ID_Text', 'Universally_Unique_Identifier_Text', 'Referential_Text', 'Data_Source_Name', 'Date', 'Cog', 'Model', 'Concept', 'Segment', 'Pedigree_Number', 'Confidence_Score_Number', 'IP_Address_Text', 'IP_Address_Integer', 'Offender_Class_Text', 'First_Observed_date', 'First_Observed_time', 'Most_Recent_Observation_date', 'Most_Recent_Observation_time', 'Total_Observations_Integer', 'Blacklist_Ranking_Integer', 'Threat_Score_Integer', 'Total_Capabilities_Integer', 'Commvett', 'Commdatevett', 'Govvett', 'Govdatevett', 'Country_Abbreviation_Text', 'Country_Text', 'City_Name', 'Coordinates_Number', 'Geographic_Longitude', 'Geographic_Latitude', 'ISP_Text', 'Domain_Name', 'Network_Speed_Number', 'Network_Autonomous_System_Number', 'Network_Class', 'Network_Type_Text', 'is_Active', 'Insrtdttm', 'Updtdttm']

#format reference file

##with open("schema_text") as f_old, open("test_output", "w") as f_new:
##    for i, line in enumerate(f_old):
##        line = '- ' + schema[i] + '\n'
##        f_new.write(line)
##        if '\n' in line:
##            f_new.write(" - extra stuff\n")


with open("schema_text") as f_old, open("test_output", "w") as f_new:
    for i, line in enumerate(f_old):
        if i == 0:
            line = '- ' + schema[i] + '\n'
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 1:
            line = '- ' + schema[i] + '\n'
            f_new.write(line)
            f_new.write(' - A universally unique identifier (UUID) is an identifier standard used in software construction. A UUID\n   consists of a 128-bit value. A UUID is formatted according to a specified variant and a specific version of\n   the variant, and the meaning of each bit is defined by any of several variants.\n')
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 2:
            line = '- ' + schema[i] + '\n'
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 3:
            line = '- ' + schema[i] + '\n'
            f_new.write(line)
            f_new.write(' - This is always "jsl"\n')
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 4:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Date of first uptime?\n')
            f_new.write(' - Type: Date\n')
            f_new.write('\n')
        if i == 5:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')          
        if i == 6:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 7:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 8:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 9:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Quality/integrity of data source\n')
            f_new.write(' - Type: Number\n')
            f_new.write('\n')
        if i == 10:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Number between 1 and 10 which defines the reliability of the data.\n')
            f_new.write(' - Type: Integer\n')
            f_new.write(' - Required\n')
            f_new.write('\n')
        if i == 11:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - IP address corresponding to entry on blacklist.\n')
            f_new.write(' - Type: String\n')
            f_new.write(' - Required\n')
            f_new.write('\n')
        if i == 12:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - IP address represented in integer notation. An IP address in string form can be converted to integer form by\n breaking it into four octets. We then perform a calculation on these. For example, given the IP address\n 213.122.92.232, we have:\n')
            f_new.write('   - First Octet:  213\n')
            f_new.write('   - Second Octet: 122\n')
            f_new.write('   - Third Octet:  92\n')
            f_new.write('   - Fourth Octet: 232\n')
            f_new.write('\n\n')
            f_new.write(' And then we can perform the calculation as follows:\n\n')
            f_new.write(' (first octet * 256³) + (second octet * 256²) + (third octet * 256) + (fourth octet)\n\n')
            f_new.write(' = (first octet * 16777216) + (second octet * 65536) + (third octet * 256) + (fourth octet)\n\n')
            f_new.write(' = (213 * 16777216) + (122 * 65536) + (92 * 256) + (232)\n\n')
            f_new.write(' = 3581566184.\n\n')
            f_new.write(' - Type: Integer\n')
            f_new.write(' - Required\n')
            f_new.write('\n')
        if i == 13:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - The offender class determines the type of blacklist. The offender class for this dataset is "dns_bl".\n')
            f_new.write(' - Type: String\n')
            f_new.write(' - Required\n')
            f_new.write('\n')
        if i == 14:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Date corresponding to the first time the item was observed.\n')
            f_new.write(' - Type: Date\n')
            f_new.write(' - Required\n')
            f_new.write('\n')
        if i == 15:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Time corresponding to the first time the item was observed.\n')
            f_new.write(' - Type: Time\n')
            f_new.write(' - Required\n')
            f_new.write('\n')
        if i == 16:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write('- Date corresponding to most recent observation of entry.\n')
            f_new.write(' - Type: Date\n')
            f_new.write(' - Required\n')
            f_new.write('\n')
        if i == 17:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 18:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 19:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 20:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 21:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 22:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 23:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 24:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 25:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 26:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 27:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 28:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 29:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 29:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 30:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 31:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 32:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 33:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 34:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 35:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 36:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 37:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 38:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 39:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
        if i == 40:
            line = '- ' + schema[i] + '\n'          
            f_new.write(line)
            f_new.write(' - Type: String\n')
            f_new.write('\n')
