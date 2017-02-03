import os

URLs = [
    'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/bi_ssh_2_30d.ipset'
    'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/blocklist_de_ssh.ipset',
    'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/cruzit_web_attacks.ipset',
    'http://www.openbl.org/lists/base_all_ftp-only.txt',
    'http://www.openbl.org/lists/base_all_http-only.txt',
    'http://www.openbl.org/lists/base_all_mail-only.txt',
    'http://www.openbl.org/lists/base_all_smtp-only.txt',
    'http://www.openbl.org/lists/base_all_ssh-only.txt'
    'http://dragonresearchgroup.org/insight/sshpwauth.txt'
]


command = "python ThreatPort.py %s "

for url in URLs:
    os.system(command % url)