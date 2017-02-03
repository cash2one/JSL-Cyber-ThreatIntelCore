#TOR Exit Nodes

## Summary
This DataSet provides information for identifying TOR Exit Nodes by preprogramed Tags/Variables. The primary function for the outputted data is aimed at providing a highly granular Exit node Profiler for, but not limited to “Black Listing” and “Threat Intelligence “initiatives. Tor relays are also referred to as "routers" or "nodes”. They receive traffic on the Tor network and pass it along. An “exit relay” is the final relay that Tor traffic passes through before it reaches its destination. Exit relays advertise their presence to the entire Tor network, so any Tor users can use them. Because Tor traffic exits through these relays, the IP address of the exit relay is interpreted as the source of the traffic. 

## Description
The Data shown in this OutPut is aggregated from various Source URLS that provided very basic information on these Exit Node Addresses. The DataSet Schema was expanded by using, “WhoIs” and “FingerPrint” data on ExitNode addresses. By scraping this data and performing these additional searching queries, we were able to optimize the amount of information to profile these Exit Nodes.


## Facts
- Date Created: 2016-01-18
- Date Modified: 2016-03-06
- Version: 2016.1
- Update Frequency: 72 hours
- Temporal Coverage: 2016-03 to 2016-04
- Spatial Coverage: Global
- Sources: TOR Exit Nodes and TOR Exit Relay
- Source URL: -
- Source License Requirements: None
- Source Citation: TOR_IP_RESOLUTION_OUTPUT.csv
- Keywords:
  - TOR Relay
  - TOR Exit Nodes
  - TOR Routers
- Other Titles and Uses:
  - Cyber - TOR Exit Nodes
  - Cyber  - TOR Exit Relays
  - Cyber – TOR Exit IPs


## Schema
- Autonomous_System_Number 
  - Exit Node Reference Number - Onion Number Reference
  - Type: Integer

- IP_Address_Text String
  - Exit Node IP Address
  - Type: String

- Country_Code_Name 
  - Country Origin
  - Type: String

- Regional_Internet_Registry_Text
  - Indicates one of the five Regional Internet Registries from which the enrichment data has originated from.
  - Type: String

- Autonomous_System_Name 
  - Exit Node Name – Onion Name Reference
  - Type: String

- is_Authority
  - Router Flags – True/False Values
  - Type: Boolean

- Listing_Date
  - Date and time corresponding to when item was published.
  - Type: Date
      
- Source_Name
  - External Source Name.
  - Type: String

- Router_Name
  - Name Register for Router.
  - Type: Integer
 
- Bandwidth_in_kb
  - Amount of Bandwidth Usage
  - Type: Integer
 
- Up_Time_in_seconds
  - Days of up time of Exit Node
  - Type: Integer
 
- Host_Name
  - Host Name for TOR Exit Node
  - Type: Integer
 
- Dir_Port_Text
  - The port where Tor advertises the directory service:
    - "DirPort: onion proxies and onion routers speak http to this port, to pull down a directory of which nodes are currently available."
    - ref: https://svn.torproject.org/svn/tor/tags/tor-0_0_9/doc/FAQ
  - Type: Integer
 
- OR_Port_Number
  - NetworkPort use to make connection.
  - Type: Integer

- First_Seen_date INT 
  - First time ExitNode began
  - Type: Integer

- Consensus_Bandwidth_in_kb
  - Bandwidth Usage
  - Type: Integer

- Or_Address_Text
  - Exit Node - Onion Address
  - Type: Integer

- Platform_Text
  - Type and version of the operating system.
  - Type: String

- Platform_Version_Number
  - What Platform the Exit Node is currently running.
  - Type: String

- Date_Published_list_of_dates
  - Date of when ExitNode first began.
  - Type: Date

- Time_Published_list_of_times
  - Time of Exit Node up status.
  - Type: Time

- Last_Status_Date_list_of_dates
  - Date of last up status.
  - Type: Date

- Last_Status_Time_list_of_times
  - Times corresponding to last up status update.
  - Type: Time

- Exit_Address
  - Onion Exit Address
  - Type: String

- Exit_Address_date
  - Onion Exit Address Date.
  - Type: Date

- Exit_Address_time
  - Onion Exit Address time.
  - Type: Time

- Fingerprint_Code
  - Exit Node Identifier.
  - Type: String

- is_Bad_Directory 
  - Router Flags – True/False Values.
  - Type: Boolean

- is_Bad_Exit BOOLEAN   Fingerprint Information
  - Router Flags – True/False Values
  - Type: Boolean

- is_Exit
  - Router Flags – True/False Values
  - Type: Boolean

- is_Fast
  - Router Flags – True/False Values
  - Type: Boolean

- is_Guard
  - Router Flags – True/False Values
  - Type: Boolean

- is_Hibernating
  - Router Flags – True/False Values
  - Type: Boolean
 
- is_Named
  - Router Flags – True/False Values
  - Type: Boolean

- is_Stable
  - Router Flags – True/False Values
  - Type: Boolean

- is_Running
  - Router Flags – True/False Values
  - Type: Boolean

- is_Valid
  - Router Flags – True/False Values
  - Type: Boolean

- is_V2Dir
  - Router Flags – True/False Values
  - Type: Boolean

- is_Exit_Accept
  - Exit Policy info – Accept/Reject Values
  - Type: Boolean

- is_Exit_Reject
  - Exit Policy info – Accept/Reject Values
  - Type: Boolean

- Onion_Key_Code
  - Router Keys – RSA Public Key.
  - Type: String

- Signing_Key_Code
  - Router Keys – RSA Public Key.
  - Type: String

- Individual_Name
  - Contact Information – name of person associated with fingerprint.
  - Type: String

- Individual_Email
  - Contact Information – email of person associated with fingerprint.
  - Type: String

- Family_Members_list_of_codes
  - Contact Information – corresponding to fingerprint information.
  - Type: String

- Descriptor_Publish_date
  - Descriptor publish date - corresponding to fingerprint information.
  - Type: Date

- Descriptor_Publish_time
  - Descriptor publish time - corresponding to fingerprint information.
  - Type: Time

- Bandwidth_Units
  - Bandwidth units corresponding to fingerprint.
  - Type: Number
 
- Site_Operator_Name
  - Contact Information – Name of person operating website.
  - Type: String
 
- Inet_Num_range
  - The range of IP address space described by the object.
  - Type: String
 
- Net_Name
  - The name of a range of IP address space.
  - Type: String
 
- Description_Text
  - Description relating to Whois information.
  - Type: String
 
- Administrative_Contacts_List
  - List of administrative contacts relating to Whois information.
  - Type: String

- Technical_Contacts_List
  - List of technical contacts for Whois 
  - Type: String

- Status_Text
  - Assigned PA
  - Type: String

- Maintainer_References_Text
  - DTAG-NIC
  - Type: String
 
- Organization_Text
  - ORG-DTAG1-RIPE
  - Type: String

- Organization_Name
  - Deutsche Telekom AG
  - Type: String
 
- Organization_Type
  - Other
  - Type: String
 
- Postal_Address_List
  - Address of Exit Node 
  - Type: String  
 
- Remarks_Text
  - General remarks. May include a URL or instructions on where to send abuse complaints.
  - Type: String 

- Maintainer_References_List
  - An object is a database object used to authorize updates to the APNIC database.
  - Type: String 

- Abuse_Contact_Text
  - Example: DTAG4-RIPE
  - Type: String 

- Person_Name
  - Example: DTAG Global IP-Addressing
  - Type: String 

- Node_Operator_Phone
  - Node Operator Phone Number
  - Type: String
 
- Node_Operator_Fax
  - Node Operator Fax Number
  - Type: String

- Nic_Handle_List
  - A unique identifier that references RIPE Database objects containing contact details for a specific person or role.
  - Type: String
 
- Route_Text
  - Routing Address
  - Type: String
 
- List_of_Origins
  - The “origin:” attribute is the AS Number of the AS that originates the route into the InterAS routing system.
  - Type: String

- Member_Of_Text
  - Active Directory query tool to determine what groups a user is in.
  - Type: String

- Latitude_as_Single  INT   IP Location
  - Number value for Geo-Location Latitude
  - Type: Number
 
- Longitude_as_Single
  - Numerical value for Geo-Location Longitude
  - Type: Number
 
- Calling_Code
  - Country calling codes or country dial in codes are telephone dialing prefixes for the member countries of the International Telecommunication Union (ITU). They are defined by the ITU-T in standards E.123 and E.164. The prefixes enable international direct dialing (IDD), and are also referred to as international subscriber dialing (ISD) codes.
    - ref: https://en.wikipedia.org/wiki/List_of_country_calling_codes
  - Type: String

- List_of_Currencies
  - Currency in region
  - Type: String
 
- Capital_Name
  - Capital in region
  - Type: String
 
- Region_Text
  - Location of Country
  - Type: String
 
- Language_Name
  - Language of designated region 
  - Type: String
