#BadDomainBruteForce

## Summary
This Datasets will be populated with all BadDomains and BadIps taken from the various Black-List outputs. Using DNS BruteForce scripts, the focus of this Datasets will be to enumerate and log all the SubDomains associated with a BadIp or BadDomains.


## Description
Brute force attacks on dns name to find out subdomains or domain suggestion, and it check domain status and dns records. Domain name system is a server which resolve dns name quiry into Ip Address and vice versa IP address to domain name. Most of dns servers have two part primary dns and secondery dns. Subdomain is a domain related with domain like www.aa.example.com is a subdomain of www.example.com.


## Facts
- Date Created: 2016-04-26
- Date Modified: 2016-04-26
- Version: 2016.2
- Update Frequency: 72 hours
- Temporal Coverage: 2016-02
- Spatial Coverage: N/A
- Sources:  All DataSets
- Source URL: -
- Source License Requirements: None
- Source Citation: BadDomainBruteForce.csv
- Keywords: 
  - Google Safe Browsing List
  - Malware Blacklists
  - Phishing Blacklists
  - Spam Blacklists
  - DNS Blacklists
  - RBL
  - DNSBL
  - Threat Ports
  - URI DNSBL
  - RFC 1918
- Other Titles and Uses: 
  - Zone Field Analysis
  - ISP_Enrichment



## Schema

- Data_Source_Name
  - This is always "jsl"
  - Type: String

- Date
  - Date of first uptime
  - Type: Date 


- Confidence_Score_Number
  - Number between 1 and 10 which defines the reliability of the data
  - Type: Integer
  - Required

- IP_Address_Text
  - IP address corresponding to entry on blacklist
  - Type: String
  - Required

- Offender_Class_Text
  - The offender class determines the type of blacklist. The offender class for this dataset is "dns_bl".
  - Type: String
  - Required

- First_Observed_date
  - Date corresponding to the first time the item was observed.
  - Type: Date
  - Required

- First_Observed_time
  - Time corresponding to the first time the item was observed
  - Type: Time
  - Required

- Most_Recent_Observation_date
  - Date corresponding to most recent observation of entry.
  - Type: Date
  - Required

- Most_Recent_Observation_time
  - Time corresponding to most recent observation of entry.
  - Type: Time
  - Required

- Total_Observations_Integer
  - Total number of times entry has been observed.
  - Type: Integer
  - Required


- Domain_Name
  - Domain name of an entry in the blacklist.
  - Type: String

- SubDomains
  - This will be the list of all SubDomains asscoiated with the BadIP or BadDomain
  - Type: String




