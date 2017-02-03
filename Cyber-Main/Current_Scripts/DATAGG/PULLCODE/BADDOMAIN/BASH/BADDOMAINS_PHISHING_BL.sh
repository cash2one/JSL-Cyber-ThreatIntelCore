#!/bin/bash 
#
#==============================================================================
#BADDOMAINS
#Last Revised At:
#Tuesday,May 3rd, 2016
#11:53 PM
#==============================================================================
unset LD_LIBRARY_PATH
#==============================================================================
#
#								   PHISHING BlackList
#==============================================================================
#==============================================================================
#https://openphish.com/feed.txt
#==============================================================================
wget https://openphish.com/feed.txt -O
/tmp/openphishfeed_BADDOM.txt --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/PHISHING/openphishfeed_BADDOM.txt
cat /tmp/openphishfeed_BADDOM.txt | sed -n '/^[0-9]/p' | sed 's/$/ /' >> 
/home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/PHISHING/openphishfeed_BADDOM.txt
rm /tmp/openphishfeed_BADDOM.txt
#==============================================================================
#http://data.phishtank.com/data/online-valid.csv
#==============================================================================
wget http://data.phishtank.com/data/online-valid.csv -O 
/tmp/phishtank_online-valid_BADDOM.csv --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/PHISHING/phishtank_online-valid_BADDOM.txt
cat /tmp/phishtank_online-valid_BADDOM.csv | sed -n '/^[0-9]/p' | cut -d',' -f1,3 | sed "s/,/ /" | sed 's/$/ /' >>
/home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/PHISHING/phishtank_online-valid_BADDOM.txt
rm /tmp/phishtank_online-valid_BADDOM.csv
