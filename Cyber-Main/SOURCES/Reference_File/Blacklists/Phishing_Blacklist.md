#Phishing Black List


## Summary
This Data Set provides accurate, actionable information to anyone trying to identify bad actors, whether for themselves or for others (i.e., building security tools). The Data Set consists of verified phish data in its free recursive DNS service, as one source among many to identify phishing sites to block for its DNS users.


## Description
This data set includes information generated from Phishing Blacklists.

Phishing Blacklists typically contain lists of URLs associated with phishing activity, together with information such as the targeted brand. Phishing generally involves the fraudulent practice of sending emails purporting to be from reputable companies in order to induce individuals to reveal personal information, such as passwords and credit card numbers, online. The phishing websites themselves, or "spoofed" sites, are designed to resemble legitimate websites. You could land on such a site simply by clicking on a link in an e-mail, via search results or even by mistyping a web address.

This data has been generated using the above mentioned Phishing Blacklists, from which ip addresses and domains have been scraped, as well as any other available information. The output has in turn been enriched by WhoIs information, obtained by querying data from one of the Regional Internet Registries, for each ip/domain: 

(1) American Registry for Internet Numbers—ARIN: Responsible for the administration of Internet addresses and domains for North America, including Canada, the United States and portions of the Caribbean.
(2) Rseaux IP Europens Network Coordination Centre—RIPE NCC: Responsible for the administration of Internet addresses and domains for Europe, the Middle East and Central Asia. RIPE NCC is considered the first official registry—the United States government was still too busy being actively involved with managing Internet addressing for much of North America 
at that time, and therefore was not first.
(3) The Asia-Pacific Network Information Centre—APNIC: Responsible for the administration of Internet addresses and domains for Asia and the Pacific Rim. Founded in Tokyo, Japan, APNIC was the second RIR to be established. APNIC relocated to Brisbane, 
Australia, in 1998.
(4) Latin American and Caribbean Internet Address Registry—LACNIC: Responsible for the administration of Internet addresses and domains for Latin America and the Caribbean. Headquartered in Montevideo, Uruguay.
(5) The African Network Information Centre—AfriNIC: Responsible for the administration of Internet addresses and domains for the African continent. Based in Ebene City, Mauritius, AfriNIC became operational in 2005.


## Facts
- Date Created: 2016-02-06
- Date Modified: 2016-03-06
- Version: 2016.2
- Update Frequency: 72 hours
- Temporal Coverage: 2016-02
- Spatial Coverage: N/A
- Sources:  Black Lists
- Source URL: -
- Source License Requirements: None
- Source Citation: BlackList_Phishing.csv
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
  - ISP_Enrichment


## Schema
- Address_ip
  - IP address of an entry in the blacklist.
  - Type: String

- Phishing_url
  - The phish URL. This is always a string, and in the XML feeds may be a CDATA block.
  - Type: String

- Verification_timestamp
  - Verification timestamp corresponding to phish data.
  - Type: Timestamp
  
- is_Online
  - Whether or not the phish is online and operational. In these data files, this will always be the string 'yes' since we only supply online phishes in these files.
  - Type: Boolean

- Target_Text
  - The name of the company or brand the phish is impersonating, if it's known.
  - Type: String

- Autonomous_System_Number
  - An autonomous system number (ASN) is a unique number that's available globally to identify an autonomous system and which enables that system to exchange exterior routing information with other neighboring autonomous systems. The number of autonomous system numbers is limited. For autonomous system numbers to be assigned, current guidelines need the network to be multi-homed and have a unique routing policy. Autonomous system numbers can be assigned only through a request to the local Internet registry.
  - Type: Integer

- Business_Gate_Protocol_Text
  - Routing addresses.
  - Type: String

- Country_Code_Text
  - Two letter code for country.
  - Type: String

- Regional_Internet_Registry_Text
  - Indicates one of the five Regional Internet Registries from which the enrichment data has originated from.
  - Type: String

- Date_Allocated_timestamp
  - Date and time corresponding to item being published.
  - Type: Timestamp

- Autonomous_System_Name
  - The ‘autonomous system name’ or 'as-name', is should be a short name associated with the Autonomous System (AS).
  - Type: String