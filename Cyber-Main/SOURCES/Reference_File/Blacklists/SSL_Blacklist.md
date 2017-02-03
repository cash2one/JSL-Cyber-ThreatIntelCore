#SSL Black Lists

## Summary
Each item in the list associates a certificate to the malicious operations in which attackers used it. The abuses include botnets, malware campaigns and banking malware. The archive behind the SSL Black List, which actually include more than 125 digital certificates, comprises SHA-1 fingerprints of each certificate with a description of the abuse. Many entries are associated with popular botnets and malware-based attacks.


## Description
This data set includes information generated from SSL Blacklists.


## Facts
- Date Created: 2016-02-10
- Date Modified: 2016-03-07
- Version: 2016.2
- Update Frequency: 72 hours
- Temporal Coverage: 2016-03 to 2016-05
- Spatial Coverage: N/A
- Sources: Black Lists
- Source URL: -
- Source License Requirements: None
- Source Citation: BLACKLIST_SSL_OUTPUT.csv
- Keywords:
  - Google Safe Browsing List
  - Malware Blacklists
  - Malware Blacklists
  - Phishing Blacklists
  - Spam Blacklists
  - DNS Blacklists
  - RBL
  - DNSBL
  - URI DNSBL
- Other Titles and Uses:
  - Zone Field Analysis
  - ISP Enrichment
  - Zone Field Analysis


## Schema
- Autonomous_System_Number
  - An autonomous system number (ASN) is a unique number that's available globally to identify an autonomous system and which enables that system to exchange exterior routing information with other neighboring autonomous systems. 
  The number of autonomous system numbers is limited. For autonomous system numbers to be assigned, current guidelines need the network to be multi-homed and have a unique routing policy. Autonomous system numbers can be assigned only through a request to the local Internet registry.
  - Type: Integer

- IP_Address_Text 
  - IP address of an entry in the blacklist.
  - Type: String

- Business_Gate_Protocol_Text  
  - Routing address.
  - Type: String

- Country_Code
  - Two letter country code.
  - Type: String

- Regional_Internet_Registry_Text
  - Nonprofit corporations that administer and register Internet Protocol (IP) address space and Autonomous System (AS) numbers within a defined region.
  - Type: String
 
- Listing_Date
  - Date of first uptime.
  - Type: Date
 
- Autonomous_System_Name
  - The ‘autonomous system name’ or 'as-name', is should be a short name associated with the Autonomous System (AS).
  - Type: String