import requests
import re


pat = '(?:(?:[0-9][0-9][0-9])\\.){3}(?:[0-9][0-9][0-9])'
URL = "https://isc.sans.edu//top10.html"


def ipsFromTxt(dump):
    ips = re.findall(pat, dump)
    return ips


def cleanIps(ips):
    new_ips = []
    for ip in ips:
        parts = [int(p) for p in ip.split('.')]
        ipx = str(parts[0])
        for part in parts[1:]:
            ipx += '.'+str(part)

        new_ips.append(ipx)

    return new_ips


def isTopTen(ip):

    response = requests.get(URL)
    ips = ipsFromTxt(response.content)
    ips = cleanIps(ips)
    if ip in ips:
        return True
    else:
        return False


isTopTen("8.8.8.8")
isTopTen("4.4.4.4")
isTopTen("87.98.147.126")
