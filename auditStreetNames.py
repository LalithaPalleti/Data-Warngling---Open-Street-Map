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
            "Ave": "Avenue",
            "Rd.": "Road"
            }
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

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

def update_name(name, mapping):

    
    for key,value in mapping.iteritems():
        key_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
        m = key_type_re.search(name)
        if m:
            key_type = m.group()
        if key_type in mapping.keys():
            # substitute the street_type for its clean version in 'name'
            name = re.sub( key_type, mapping[key_type], name)
            

        return name
    

