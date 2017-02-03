#!/usr/bin/env bash
a=`cat <<-EOF

https://malc0de.com/bl/ZONES > malc0dezonesdomains.csv
https://www.dshield.org/feeds/suspiciousdomains_Low.txt > dshieldsusdomainslow.csv
https://www.dshield.org/feeds/suspiciousdomains_Medium.txt > dshieldsusdomainsmedium.csv
https://www.dshield.org/feeds/suspiciousdomains_High.txt > dshieldsushighdomains.csv
http://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt > ransomtrackerrwdombl.csv
http://www.nothink.org/blacklist/blacklist_malware_dns.txt > nothink_dnsbldomain.csv
EOF`
cd ../
for i in $a
do
wget --no-check-certificate $i
done
