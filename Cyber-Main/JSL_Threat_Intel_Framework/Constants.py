def init():
    global aggregationreport
    aggregationreport = []

IPV4_REGEX = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
DOMAIN_NAME_REGEX = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
phase1report = 'This is the report of the phase 1 : data aggregation phase \n\n '

BADDOMAINS = {
    'malware': ['http://secure.mayhemiclabs.com/malhosts/malhosts.txt',
                      'http://www.urlvir.com/export-hosts/',
                    'http://isc.sans.edu/feeds/suspiciousdomains_Low.txt',
                    'http://isc.sans.edu/feeds/suspiciousdomains_Medium.txt',
                    'http://isc.sans.edu/feeds/suspiciousdomains_High.txt',
                    'https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist',
                    'https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist',
                    'https://zeustracker.abuse.ch/blocklist.php?download=compromised',
                    'http://osint.bambenekconsulting.com/feeds/c2-dommasterlist-high.txt',
                    'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/malwaredomainlist.ipset',
                    'https://www.dshield.org/feeds/suspiciousdomains_High.txt',
                    'https://lists.malwarepatrol.net/cgi/getfile?receipt=f1417692233&product=8&list=dansguardian',
                    'http://ransomwaretracker.abuse.ch/downloads/RW_URLBL.txt',
                    'http://vxvault.net/URL_List.php'
                ],

    'spam': [

        'http://www.joewein.de/sw/blacklist.htm#bl'

    ]

    , 'tor': [

    ]

    , 'ssl': [

    ]

    , 'phishing': [

        'https://openphish.com/feed.txt',
        'http://data.phishtank.com/data/online-valid.csv'

    ]

    , 'dns': [

    ]}

BADIPS = {

    'malware': [
        'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist',
        'http://www.urlvir.com/export-ip-addresses/',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/zeus.ipset',
        'http://www.malwaredomainlist.com/hostslist/ip.txt',
        'https://www.badips.com/get/list/any/2?age=7d',
        'http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist-high.txt',
        'http://osint.bambenekconsulting.com/feeds/dga-feed.txt',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/bambenek_suppobox.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/bitcoin_nodes_1d.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/hphosts_emd.ipset',
        'http://lists.blocklist.de/lists/all.txt',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/botscout_1d.ipset',
        'http://cinsscore.com/list/ci-badguys.txt',
        'http://isc.sans.edu/reports.html',
        'http://www.projecthoneypot.org/list_of_ips.php',
        'http://www.openbl.org/lists/base.txt',
        'http://www.nothink.org/blacklist/blacklist_malware_http.txt',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/malc0de.ipset',
        'https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist',
        'http://www.malwaredomainlist.com/hostslist/ip.txt',
        'http://rules.emergingthreats.net/blockrules/compromised-ips.txt',
        'http://rules.emergingthreats.net/blockrules/emerging-botcc.rules',
        # 'http://rules.emergingthreats.net/fwrules/emerging-PF-CC', url not found
        'http://rules.emergingthreats.net/blockrules/emerging-ciarmy.rules',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/ciarmy.ipset',
        'http://doc.emergingthreats.net/pub/Main/RussianBusinessNetwork/emerging-rbn-malvertisers.txt',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/ransomware_feed.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/cybercrime.ipset',
        'http://ransomwaretracker.abuse.ch/downloads/RW_IPBL.txt',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/iblocklist_malc0de.netset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/vxvault.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/pushing_inertia_blocklist.netset',
        # 'http://www.malwaregroup.com/ipaddresses'  url returns a php error
    ]
    , 'spam': [

        'http://sblam.com/blacklist.txt',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/sp_spammers.netset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/spamhaus_edrop.netset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/iblocklist_spamhaus_drop.netset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/virbl.ipset',
        'http://antispam.imp.ch/spamlist',
        'http://www.unsubscore.com/blacklist.txt:unsubscore-blacklist',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/botscout.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/et_spamhaus.netset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/php_harvesters.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/sp_spammers.netset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/nixspam.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/cleanmx_phishing.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/chaosreigns_iprep0.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/lashback_ubl.ipset',

    ]

    , 'tor': [

        'https://check.torproject.org/exit-addresses',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/tor_exits.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/bm_tor.ipset'

    ]

    , 'ssl': [

        'http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-1.uceprotect.net.gz',
        'http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-2.uceprotect.net.gz',
        'http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-3.uceprotect.net.gz',
        'http://www.openbl.org/lists/base_all.txt',
        'https://rules.emergingthreats.net/open/suricata/rules/emerging-dns.rules',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/openbl_1d.ipset'

    ]

    , 'phishing': [

        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/cleanmx_phishing.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/atlas_phishing.ipset'

    ]

    , 'dns': [

    ]

}
