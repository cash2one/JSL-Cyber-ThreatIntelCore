import sys
from os import listdir
from os.path import isfile, join
import os

URLss = [
    'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/bi_ssh_2_30d.ipset'
    #'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/blocklist_de_ssh.ipset',
    #'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/cruzit_web_attacks.ipset',
    #'http://www.openbl.org/lists/base_all_ftp-only.txt',
    #'http://www.openbl.org/lists/base_all_http-only.txt',
    #'http://www.openbl.org/lists/base_all_mail-only.txt',
    #'http://www.openbl.org/lists/base_all_smtp-only.txt',
    #'http://www.openbl.org/lists/base_all_ssh-only.txt'
    #'http://dragonresearchgroup.org/insight/sshpwauth.txt'
]

PORTs = {
    'ftp': ['ftp'],
    'http': ['http-', 'web'],
    'ssh': ['ssh'],
    'smtp': ['smtp', 'mail']
}


def get_port(url):
    for key in PORTs.keys():
        for port in PORTs[key]:
            if port in url:
                return key



def main():

    URLs = [sys.argv[1]]

    DNS_RESOLUTION = "./dns_resolver -ip url.iplist -output url.dnslist"
    CLEAN_DNS_OUTPUT_1 = "grep ^[0-9] url.dnslist > tmp "
    CLEAN_DNS_OUTPUT_2 = "mv tmp url.dnslist"

    command = "python GIOWHOIS_threat.py url.dnslist threatport_bl %s %s"
    command_ = "echo %s > url"
    command_pullcode = 'python ipsFromUrls.py url url.iplist'
    command_rm = "rm url url.iplist"

    for url in URLs:

        port = get_port(url)
        protocol = 'tcp'

        os.system(command_ % url)
        os.system(command_pullcode)

        os.system(DNS_RESOLUTION)
        os.system(CLEAN_DNS_OUTPUT_1)
        os.system(CLEAN_DNS_OUTPUT_2)

        os.system(command % (protocol, port))
        os.system(command_rm)


if __name__ == '__main__':
    main()
