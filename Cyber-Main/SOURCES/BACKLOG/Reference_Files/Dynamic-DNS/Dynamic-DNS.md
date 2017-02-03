#Dynamic DNS Resolution

## Summary
Dynamic DNS services are Internet sites built to serve users whose machines are regularly changing their IP address—perhaps because the address assigned by their ISP is not stable but is pulled from a pool of free addresses with every reconnect. By offering an API through which the user can offer her username, password, and new IP address, the DDNS service can update its database and point the user's domain name at the new IP. 

## Description
This a is a list of malicious domains that use a form of Dynamic DNS services to serve or perform illegal activity. Reverse lookups and common enumeration techniques can give a profile on these malicious domains.

## Facts
- Date Created: 2016-02-23
- Date Modified: 2016-03-06
- Version: 2016.1
- Update Frequency: 72 hours
- Temporal Coverage: 2016-03 to 2016-04
- Spatial Coverage: Dynamic DNS Resolution
- Sources: Dynamic DNS Resolution
- Source URL: -
- Source License Requirements: None
- Source Citation: Dynamic_DNS_OUTPUT.csv
- Keywords:
  - Malware
  - DNS Flux
  - Double DNS flux
  - TTL
  - DDNS
- Other Titles and Uses:
  - Blacklists


## Schema
- Autonomous_System_Number
  - AS Number stands for “Autonomous System Number”. Every public AS (Autonomous System) has an AS Number associated with it. This is a globally unique number, which is used both in the exchange of exterior routing information, (between neighboring Autonomous Systems), and also as an “identifier” of the AS itself. There are two types of AS Numbers: 
    - Public AS Numbers
    - Private AS Numbers
  - Type: Integer
  - Properties: DataSource Scrape Data
    
- IP_Address_Text  DataSource Scrape Data      
  - IP address corresponding to the malicious domain.
  - Type: String
  - Properties: DataSource Scrape Data

- Autonomous_System_Name  
  - Internet netbook routing protocol Border GateThe ‘autonomous system name’ or 'as-name' , is should be a short name associated with the Autonomous System (AS).
  - Type: String
  - Properties: DataSource Scrape Data
 
- Domain_Name
  - Domain name of an entry in the blacklist.
  - Type: String 
  - Properties: DataSource Scrape Data
     
