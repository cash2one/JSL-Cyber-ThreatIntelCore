#Zone Field Analysis

## Summary
Zone Field Analysis logging provides a domain history, linking it not only to Internet Protocol(IP) addresses, but to domain registrars, ISPs and geographic locations. This Dataset will provide demonstrate an applied logging utility by tracing DNS records through pivots and relationships to Internet Service Providers(ISP). It will also show how ‘bullet-proof’ hosters layer their products form their legitimate bases of operations, package them, and provide resiliency to illegitimate purposes. The ultimate goal is to provide techniques for incident responders to employ defense techniques, either for efficiency or completeness, against an identified, mapped threat. 

## Description
This Dataset combines all the IPs, Domains, and Hostnames from every Data Set to run queries against. These queries are commonly known to be NSLOOKUP , DIG, and HOST. With these queries combined, a significantly complex profile of activity can be gathered.


## Facts
- Date Created: 2016-02-18
- Date Modified: 2016-03-07
- Version: 2016.1
- Update Frequency: 72 hours
- Temporal Coverage: 2016-03 to 2016-05 
- Spatial Coverage: Zone Field Analysis
- Sources:  Zone Field Analysis
- Source URL: -
- Source License Requirements: None
- Source Citation: Zone_Field_Analysis_output.csv
- Keywords: 
	- Malware
  - DNS Flux
  - Double DNS flux
  - TTL
  - DDNS
  - ISP
  - NSLOOKUP
  - UDP 53
  - NS queries
  - PTR
  - SOA
  - TXT
  - DNSSEC
  - CNAME
  - MX
- Other Titles and Uses: 
  - Blacklists
  - TOR IP Resolution
  - ISP Enrichment


## Schema
- ip_address                           
  - ip address corresponding to the malicious domain.
  - Type: String  
    
- asn_number       
  - AS Number stands for “Autonomous System Number”. Every public AS (Autonomous System) has an AS Number associated with it. This is a globally unique number, which is used both in the exchange of exterior routing information, (between neighboring Autonomous Systems), and also as an “identifier” of the AS itself. There are two types of AS Numbers: (i) Public AS Numbers, (ii) Private AS Numbers.
  - Type: Integer

- bgp_block   
  - Internet netbook routing protocol Border Gate
  - Type: String  
 
- country_code    
  - Country Code corresponding to the malicious domain.
  - Type: String  
     
- registry 
  - Specifies one of the five Regional Internet Registries: AFRINIC, APNIC, ARIN, LACNIC, RIPE NCC, where the data for a particular malicious domain has originated.   
  - Type: String 

- date_allocated   
  - Data corresponding to when information on malicious domain was published.
  - Type: Date
      
- as_name
  - The ‘autonomous system name’ or 'as-name' , is should be a short name associated with the Autonomous System (AS).
  - Type: String
       
- ptr   
  - Pointer Resource Record. A variable-length domain name. This is a name “pointed to” by the resource record RFC 1035.
  - Type: String
      
- mx
  - Mail Exchange Resource Record. This special record contains information about the mail server(s) to be used for sending 
  e-mail to the domain RFC1035. 
  - Type: Integer
      
- txt
  - Text Resource Record. This descriptive record contains additional descriptive information about the named object
  - Type: String
     
- SOA 
  - State of authority
  - Type: String
       
- CNAME
  - Conical Name Record. The CNAME record specifies a domain name that has to be queried in order to resolve the original DNS query. Therefore, CNAME records are used for creating aliases of domain names. CNAME records are truly useful when we want to alias our domain to an external domain. In other cases, we can remove CNAME records and replace them with A records and even decrease performance overhead RFC 1035.
  - Type: String

- A
  - Address Record. The record A specifies IP address (IPv4) for given host. A records are used for conversion of domain names to corresponding IP addresses. RFC 1035.
  - Type: String

- Server_name 
  - Name of DNS used to perform query
  - Type: String

- AAAA
  - IPv6. The record AAAA (also quad-A record) specifies IPv6 address for given host. So it works the same way as the A record and the difference is the type of IP address. RFC3595.
  - Type: String

- Host_information_records  
  - HINFO records are used to acquire general information about a host. The record specifies type of CPU and OS. The HINFO record data provides the possibility to use operating system specific protocols when two hosts want to communicate. For security reasons the HINFO records are not typically used on public servers.
  - Type: String

-  ns STRING
  - The NS record specifies an authoritative name server for given host.
  - Type: String