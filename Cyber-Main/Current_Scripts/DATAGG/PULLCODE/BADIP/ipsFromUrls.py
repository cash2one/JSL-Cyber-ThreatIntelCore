import os
import zipfile
import re
import gzip
import requests
from cStringIO import StringIO
import sys

def ipsFromGzip(dump):

    results = gzip.GzipFile(fileobj=StringIO(dump))
    ips = re.findall(pat, results.read())
    return ips


def ipsFromZip(dump):
    zipinmemory = StringIO(dump)
    zip = zipfile.ZipFile(zipinmemory)
    ips = []
    for fn in zip.namelist():
            ips += re.findall(pat, zip.read(fn))
    return ips


def ipsFromTxt(dump):
    #print len(dump)
    #print len(dump.split('\n'))
    #print dump
    ips = re.findall(pat, dump)
    #print ips
    return ips

def ipsFromgzWget(url):
    length = len(url.split('/'))
    filename = url.split('/')[length-1]
    os.system("wget %s" % url)
    gzipped = open(filename)
    results = gzip.GzipFile(fileobj=StringIO(gzipped.read()))
    ips = re.findall(pat, results.read())
    os.remove(filename)
    return ips

pat = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'


def getIPAddresses(url):
    if 'wget' in url:
        
        return ipsFromgzWget(url)

    response = requests.get(url)

    if 'Content-Type' not in response.headers.keys():
        ips = ipsFromTxt(response.content)
    elif 'gz' in response.headers['Content-Type']:
        ips = ipsFromGzip(response.content)
    elif 'zip' in response.headers['Content-Type']:
        ips = ipsFromZip(response.content)
    else:
        ips = ipsFromTxt(response.content)
    print str(len(ips)) + " ips extracted from %s " % url
    return ips
def main():
  if len(sys.argv) != 3:
    print """USAGE :
                      python ipsFromUrls.py urlsFile output.iplist
                      """
    return


  inputFilename = sys.argv[1]

  outputFilename = sys.argv[2]

  inputF = open(inputFilename, 'r')
  outputF = open(outputFilename, 'w')

  ip = []
  for line in inputF.readlines():
      #print line.strip()
      ip += getIPAddresses(line.strip())

  #print len(ip)

  #ip = list(set(ip))
  
  #print len(ip)
  
  for ipp in ip:
      outputF.write(ipp+"\n")
  
  outputF.close()
  inputF.close()



if __name__ == "__main__":
    main()