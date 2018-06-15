## Open-Street-Map Data Wrangling

### Introduction

Map Area
Seattle WA, United States
https://www.openstreetmap.org/export#map=10/47.6258/-122.3252

### Problems Encountered in the Map
I have downloaded a small sample size of the Seattle area and run it, I noticed the following five
main problems:
• Misleading abbreviation for street names (“142nd Ave E”, “S River Rd”)
• Inconsistent postal codes (“98057-4040”, “98020”)

### Correcting Street Names
Once the data was imported to SQL, some basic querying revealed street name abbreviations
and postal code inconsistencies. To deal with correcting street names, I opted not use regular
expressions, and instead iterated over each word in an address, correcting them to their
respective mappings in audit.py using the following function:

### Postal Codes
Postal code strings are mostly 5 digits with 980 as starting number, but some are4-digit zip code
extensions following a hyphen (“98057-4040”). After standardizing inconsistent postal codes,
some altogether postal codes showed up in the following manner:
Here are the top ten results, beginning with the highest count:

### Overview of Data
### File Sizes
### Number of Ways
### Number of Unique Users
### Top 10 Contributing Users
### Number of Users Appearing only once (having 1 post)
### Additional Ideas
### Top 10 Appearing Amenities
### Biggest Religion
### Most Popular Cuisines

