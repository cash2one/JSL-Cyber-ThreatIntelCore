#!/usr/bin/env bash
a=`cat <<-EOF
https://openphish.com/feed.txt > openphishoutput.csv
http://data.phishtank.com/data/online-valid.csv
http://mirror1.malwaredomains.com/files/domains.txt > malwaredomainsoutput.csv
EOF`
cd cd ../
for i in $a
do
wget --no-check-certificate $i
done
