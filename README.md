## Open-Street-Map Data Wrangling

### Introduction
Extracted Map data for Seattle WA, United States
https://www.openstreetmap.org/export#map=10/47.6258/-122.3252

I have taken only a sample size of 10 MB from the Seattle area for this project

### Problems Encountered in the Map
    I noticed the following problems in the map data
    - Misleading abbreviation for street names (“142nd Ave E”, “S River Rd”)
    - Inconsistent postal codes (“98057-4040”, “98020”)

### Correcting Street Names
Once the data was imported to SQL, some basic querying revealed street name abbreviations
and postal code inconsistencies. To deal with correcting street names, I opted not use regular
expressions, and instead iterated over each word in an address string, correcting them to their
respective mappings using string functions

### Correcting Postal Codes
Postal code strings are mostly 5 digits with 980 as starting number, but some are 4-digit zip code
extensions following a hyphen (“98057-4040”), I have corrected such zip codes and standardized to 5 digits

### Overview of Data 

#### File Sizes
- Seattlemap.osm ......... 129 MB
- sample.osm ............. 13 MB
- output.osm ............. 13 MB
- seattle.db ............. 7 MB
- nodes.csv .............. 4 MB
- nodes_tags.csv ......... 267 KB
- ways.csv ............... 437 KB
- ways_tags.csv .......... 974 KB
- ways_nodes.cv .......... 1.7 MB

#### Number of Ways
    7266
    
#### Number of Unique Users
    436
    
#### Top 10 Contributing Users
    (u'Omnific', 19989), 
    (u'Grauer Elefant', 4687), 
    (u'Amoebabadass', 4468), 
    (u'STBrenden', 3977), 
    (u'Glassman', 3680), 
    (u'csytsma', 2836), 
    (u'woodpeck_fixbot', 2403), 
    (u'Geodesy99', 2245), 
    (u'Skybunny', 1766), 
    (u'zephyr', 1414)
    
#### Number of Users Appearing only once (having 1 post)
    107
    
### Additional Ideas
#### Top 10 Appearing Amenities
     (u'restaurant', 42), 
     (u'bench', 38),
     (u'fast_food', 34),
     (u'waste_basket', 20),
     (u'cafe', 19),
     (u'bank', 15),
     (u'doctors', 15),
     (u'fuel', 13),
     (u'dentist', 12),
     (u'school', 12)
     
#### Biggest Religion
    (u'christian', 6)
    
#### Most Popular Cuisines
    (u'pizza', 7), 
    (u'japanese', 4), 
    (u'chinese', 3), 
    (u'asian', 2), 
    (u'burger', 2), 
    (u'mexican', 2), 
    (u'thai', 2), 
    (u'american;savory_pancakes;pancake;breakfast', 1), 
    (u'barbecue', 1), 
    (u'burger;asian', 1), 
    (u'indian', 1), 
    (u'italian', 1), 
    (u'pancake;breakfast', 1), 
    (u'vietnamese', 1)

