
#####Features At A Glance

* Fetch intel from URL's using modular feed functions
* Extract domain, md5, sha1, sha256, IPv4, and YARA indicators
* Search through the current intel set by single IP or with an IOC file
* Generate JSON feeds for consumption by CarbonBlack
* Serves up a Simple HTTP JSON feed server for CarbonBlack

Requirements:
-------
*Requires Python 3!*
* argparse
* xlrd
* pdfminer3k
* colorama (for pretty colored output)

You can install all requirements with the included requirements.txt file
```
pip3 install -r requirements.txt
```

Feeds
--------

(Invoked with --feeds)

* 'list' -- Lists all feeds and allows user to choose a single feed to update.
* 'update' -- Updates all feed modules listed in foxtrot

Hunting
---------

(Invoked with --hunt)

* '-f [file path]' Provides the capability to search through the intel directory results for a specific list of indicators
* '-s [IPv4 address]' Searches through intel directory for a single IP address

Extraction
----------

(Invoked with --extract)

* Reads in a file and extracts IP addresss, domains, MD5/SHA1/SHA256 hashes, and YARA rules
* Places the extracted indicators into the intel directory
* Currently supported filetypes:
  * TXT
  * PDF
  * XLS/XLSX

Note:

* Prone to false positives when extracting indicators from PDF as whitepapers with indicators will normally also contain URL references
