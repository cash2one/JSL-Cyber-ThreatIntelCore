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
    #print dump
    ips = []
    for line in dump.split('\n'):
      if not line.startswith('#'):
        ips += re.findall(pat, line)
    #print ips
    #print ips
    real_ips = []
    for ip in ips:

      print ip
      if not (ip.endswith('.txt') or ip.endswith('.php') or ip.endswith('.html') or ip.endswith('.jpeg') or ip.endswith('.bin') or ip.endswith('.jpg') ):
        ip_parts = ip.split('.')
        length = len(ip_parts)
        #if length > 2:
        #  ip = ip_parts[length-4] + '.' + ip_parts[length-1]

        real_ips.append(ip)
    print len(ips)
    return real_ips


def ipsFromgzWget(url):
    length = len(url.split('/'))
    filename = url.split('/')[length-1]
    os.system("wget %s" % url)
    gzipped = open(filename)
    results = gzip.GzipFile(fileobj=StringIO(gzipped.read()))
    ips = re.findall(pat, results.read())
    os.remove(filename)
    return ips

pat = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'


def getIPAddresses(url):
    if 'wget' in url:

        return ipsFromgzWget(url)


    response = requests.get(url)

    if 'Content-Type' not in response.headers.keys():
        return ipsFromTxt(response.content)

    elif 'gz' in response.headers['Content-Type']:
        return ipsFromGzip(response.content)
    elif 'zip' in response.headers['Content-Type']:
        return ipsFromZip(response.content)
    else:
        return ipsFromTxt(response.content)

def main():
  if len(sys.argv) != 3:
    print """USAGE :
                      python ipsFromUrls.py urlsFile output.iplist
                      """
    return


  inputFilename = sys.argv[1]
  print " regardez si on a ouvert le fichier"
  outputFilename = sys.argv[2]

  inputF = open(inputFilename, 'r')
  outputF = open(outputFilename, 'w')

  ip = []
  for line in inputF.readlines():
      #print line.strip()
      print line
      ip += getIPAddresses(line.strip())

  print len(ip)

  ip = list(set(ip))

  print len(ip)

  for ipp in ip:
      print ipp
      outputF.write(ipp+"\n")

  outputF.close()
  inputF.close()



if __name__ == "__main__":
    main()

