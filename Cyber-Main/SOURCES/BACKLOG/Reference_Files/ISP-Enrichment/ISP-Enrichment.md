#ISP ENRICHMENT

## Summary
This provides detailed profile on ISP providers in relationship to the traffic generated by hosts on designated NetBlock. The core focus of the data set is to give a granular approach to pinpointing malicious activity down to the actual geo spatial characteristics of target host and/or ISP. 

## Description
This provides a detailed perspective on the host and the host’s ISP. Combined with a growing profile of the ISP, a method of anticipating the origin of attacks can become an option.


## Facts
- Date Created: 2016-02-11
- Date Modified: 2016-03-03
- Version: 2016.1
- Update Frequency: 72 hours
- Temporal Coverage: 2016-02 to 2016-03
- Spatial Coverage: ISP Enrichment
- Sources:  ISP ENRICHMENT
- Source URL: -
- Source License Requirements: None
- Source Citation: ISP_ENRICHMENT_OUTPUT.CSV
- Keywords:
  - Geolocate
  - Active Directory DNS
  - Longitude
  - Latitude
  - ISP
  - Spatial
  - Time Zone
- Other Titles and Uses:
  - Black List
  - TOR IP Resolution
  - Zone Field Transfer


## Schema
- Country_Code    
  - ISP/host location by country.
  - Type: Integer
    
- Internet_Service_Provider
  - Internet service provider name.
  - Type: String

- Longitude
  - Longitude in degrees for target Host/ISP.
  - Type: Integer
 
- Zip_Code  
  - Zip code of ISP/Host.
  - Type: Integer

- Region_Name
  - State Location.
  - Type: String

- City_Name
  - ISP/host location by city.
  - Type: String

- Region_Code 
  - State Abbreviation
  - Type: String    

- Country_Code
  - Two digit Country code.
  - Type: String

- Latitude   
  - Latitude in degrees for target Host/ISP.
  - Type: Integer

- IP_Address_Text
  - IP Address.
  - Type: Integer

- Autonomous_System_Name   
  - The ‘autonomous system name’ or 'as-name' , is should be a short name associated with the Autonomous System (AS).
  - Type: String