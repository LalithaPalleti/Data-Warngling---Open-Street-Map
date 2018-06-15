import re
import xml.etree.cElementTree as ET
import pprint
import collections
import codecs
import cerberus
import schema
import csv
mapping = { "St": "Street",
            "St.": "Street",
            "st": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Rd" : "Road",
            "Blvd" : "Boulevard",
            "Dr"   : "Drive",
            "dr"   : "Drive",
            "Pl"   : "Place", 
            "Pkwy" : "Parkway",
            "S"    : "South",
            "E"    : "East",
            "NE"   : "NorthEast",
            "N"    : "North",
            "SE"   : "SouthEast" 

            }
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","South","East","NorthEast"]

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        
        if street_type not in expected:
            street_types[street_type].add(street_name) 
            
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = collections.defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

    
def update_name(name):
    parsed_name = name.split()    
    new_name = []  
    for i in parsed_name:
        if i in mapping.keys():
            i = mapping[i]
            new_name.append(i)
        else:
            new_name.append(i)

    string = ' '.join(new_name)
               
    print string
    return string
