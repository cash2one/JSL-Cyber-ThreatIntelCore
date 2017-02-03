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
#								               DNS BlackList
#==============================================================================
#==============================================================================
#https://malc0de.com/bl/ZONES
#==============================================================================
wget https://malc0de.com/bl/ZONES -O
/tmp/malc0de_zone_BADOM.txt --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/malc0de_zone_BADOM.txt 
cat /tmp/malc0de_zone_BADOM.txt  | sed -n '/^[0-9]/p' | sed 's/$/ /' >> 
/home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/malc0de_zone_BADOM.txt 
rm /tmp/malc0de_zone_BADOM.txt 
#==============================================================================
#https://www.dshield.org/feeds/suspiciousdomains_Low.txt
#==============================================================================
wget https://www.dshield.org/feeds/suspiciousdomains_Low.txt -O 
/tmp/suspiciousdomains_Low.txt --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/suspiciousdomains_Low.txt
cat /tmp/suspiciousdomains_Low.txt | sed -n '/^[0-9]/p' | sed 's/$/ /' >> 
/home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/suspiciousdomains_Low.txt
rm /tmp/suspiciousdomains_Low.txt
#==============================================================================
#https://www.dshield.org/feeds/suspiciousdomains_Medium.txt
#==============================================================================
wget https://www.dshield.org/feeds/suspiciousdomains_Medium.txt -O 
/tmp/suspiciousdomains_Medium.txt --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/suspiciousdomains_Medium.txt
cat /tmp/suspiciousdomains_Medium.txt | sed -n '/^[0-9]/p' | sed 's/$/ /' >> 
/home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/suspiciousdomains_Medium.txt
rm /tmp/suspiciousdomains_Medium.txt
#==============================================================================
#https://www.dshield.org/feeds/suspiciousdomains_High.txt
#==============================================================================
wget https://www.dshield.org/feeds/suspiciousdomains_High.txt -O 
/tmp/suspiciousdomains_High.txt --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/suspiciousdomains_High.txt
cat /tmp/suspiciousdomains_High.txt | sed -n '/^[0-9]/p' | sed 's/$/ /' >> 
/home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/suspiciousdomains_High.txt
rm /tmp/suspiciousdomains_High.txt
#==============================================================================
#http://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt
#==============================================================================
wget http://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt -O
/tmp/RW_DOMBL.txt --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/RW_DOMBL.txt
cat /tmp/RW_DOMBL.txt | sed -n '/^[0-9]/p' | cut -d',' -f1,3 | sed "s/,/ /" | sed 
's/$/ /' >> /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/RW_DOMBL.txt
rm /tmp/RW_DOMBL.txt
#==============================================================================
#http://ransomwaretracker.abuse.ch/downloads/RW_URLBL.txt
#==============================================================================
wget http://ransomwaretracker.abuse.ch/downloads/RW_URLBL.txt -O 
/tmp/RW_URLBL.txt --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/RW_URLBL.txt
cat /tmp/RW_URLBL.txt | sed -n '/^[0-9]/p' | sed 's/$/ /' >> 
/home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/RW_URLBL.txt
rm /tmp/RW_URLBL.txt
#==============================================================================
#http://www.nothink.org/blacklist/blacklist_malware_dns.txt  #! this is both domains and IPS
#==============================================================================
wget http://www.nothink.org/blacklist/blacklist_malware_dns.txt -O
/tmp/blacklist_malware_dns.txt --no-check-certificate -N
echo "# Generated: `date`" > /home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/blacklist_malware_dns.txt
cat /tmp/blacklist_malware_dns.txt | sed -n '/^[0-9]/p' | sed 's/$/ /' >> 
/home/cyberdev/AGGREGATION/BADDOMAINS/BLACKLISTS/DNS/sblacklist_malware_dns.txt
rm /tmp/blacklist_malware_dns.txt
