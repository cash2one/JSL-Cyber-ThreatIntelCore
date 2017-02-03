#!/bin/bash

# Setup S3 credentials
echo "access_key = $(echo $S3_CREDS | awk -F':' '{print $1}')" >> /root/.s3cfg
echo "secret_key = $(echo $S3_CREDS | awk -F':' '{print $2}')" >> /root/.s3cfg

if [ -z $CYLINE ]; then
  CYLINE=$(
  s3cmd ls s3://data.johnsnowlabs.com/cyber/IP_SPLIT/Split_$CYSPLIT/REFINED/ | gawk '
    END { print gensub(/.*_([[:digit:]]+.csv).gz/,"\\1", "g", $4) }')
fi

mkdir -p /app/data/$CYSPLIT
cd /app/data/$CYSPLIT
for chunk in `s3cmd ls s3://data.johnsnowlabs.com/cyber/IP_SPLIT/Split_$CYSPLIT/ | gawk '/_'$CYLINE'/,EOF { print $4 }'`;
  do
  if [[ $chunk =~ $CYLINE ]]; then
    continue
  fi
  FILE=$(echo $chunk | cut -b53-)
  rm -f $FILE REFINED/$FILE
  s3cmd get $chunk
  python /app/gio_3.py $FILE REFINED/$FILE >> REFINED/$FILE.log 2>&1
  gzip REFINED/$FILE
  s3cmd put REFINED/$FILE.gz s3://data.johnsnowlabs.com/cyber/IP_SPLIT/Split_$CYSPLIT/REFINED/
  rm -f $FILE REFINED/$FILE.gz
done

while true; do sleep 1; done
