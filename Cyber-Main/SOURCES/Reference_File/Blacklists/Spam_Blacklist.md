#Spam Black List


## Summary
Spam Datasets will discover the origin of spam emails and reports them to internet service providers. The Spam Black List is constructed from users, “spamtraps”, and other websites that use the blacklists to source the origin of these dodgy emails.


## Description
This data set includes information generated from Spam Blacklists.

Spam Blacklists consist of lists of ip addresses, host names and/or e-mail addresses, together with other information, such as the associated time the data was recorded. 'Spam' are unsolicited messages sent over the Internet, typically to large numbers of users, for the purposes of advertising, phishing, spreading malware, etc.

This data has been generated using the above mentioned Malware, Phishing and Spam Blacklists, from which ip addresses and domains have been scraped, as well as any other available information. The output has in turn been enriched by WhoIs information, obtained by querying data from one of the Regional Internet Registries, for each ip/domain: 

(1) American Registry for Internet Numbers—ARIN: Responsible for the administration of Internet addresses and domains for North America, including Canada, the United States and portions of the Caribbean.
(2) Rseaux IP Europens Network Coordination Centre—RIPE NCC: Responsible for the administration of Internet addresses and domains for Europe, the Middle East and Central Asia. RIPE NCC is considered the first official registry—the United States government was still too busy being actively involved with managing Internet addressing for much of North America 
at that time, and therefore was not first.
(3) The Asia-Pacific Network Information Centre—APNIC: Responsible for the administration of Internet addresses and domains for Asia and the Pacific Rim. Founded in Tokyo, Japan, APNIC was the second RIR to be established. APNIC relocated to Brisbane, 
Australia, in 1998.
(4) Latin American and Caribbean Internet Address Registry—LACNIC: Responsible for the administration of Internet addresses and domains for Latin America and the Caribbean. Headquartered in Montevideo, Uruguay.
(5) The African Network Information Centre—AfriNIC: Responsible for the administration of Internet addresses and domains for the African continent. Based in Ebene City, Mauritius, AfriNIC became operational in 2005.



## Facts
- Date Created: 2016-02-10
- Date Modified: 2016-02-17
- Version: 2016.2
- Update Frequency: 72 hours
- Temporal Coverage: 2016-02
- Spatial Coverage: N/A
- Sources:  Black Lists
- Source URL: -
- Source License Requirements: None
- Source Citation: BLACKLIST_Spam_OUTPUT.csv
- Keywords:
  - Google Safe Browsing List
  - Malware Blacklists
  - Phishing Blacklists
  - Spam Blacklists
  - DNS Blacklists
  - RBL
  - DNSBL
  - URI DNSBL
- Other Titles and Uses: 
  - Zone Field Analysis
  - ISP_Enrichment


## Schema
- Address_ip
  - IP address of an entry in the blacklist.
  - Type: String

- Autonomous_System_Number
  - An autonomous system number (ASN) is a unique number that's available globally to identify an autonomous system and which enables that system to exchange exterior routing information with other neighboring autonomous systems. The number of autonomous system numbers is limited. For autonomous system numbers to be assigned, current guidelines need the network to be multi-homed and have a unique routing policy. Autonomous system numbers can be assigned only through a request to the local Internet registry.
  - Type: Integer

- IP_Address_Text
  - IP address of an entry in the blacklist.
  - Type: String

- Business_Gate_Protocol_Text
  - Routing addresses
  - Type: String

- Country_Code_Text
  - Two letter representation of country corresponding to data item.
  - Type: String

- Regional_Internet_Registry_Text
  - Indicates one of the five Regional Internet Registries from which the enrichment data has originated from.
  - Type: String

- Listing_Date
  - Date corresponding to listing item.
  - Type: Date

- Autonomous_system_Name
  - The ‘autonomous system name’ or 'as-name', is should be a short name associated with the Autonomous System (AS).
  - Type: String