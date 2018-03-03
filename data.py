
import schema
import re
import codecs
import csv
import cerberus
import xml.etree.cElementTree as ET
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema


NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    
    
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        
        if event == 'end' and elem.tag in tags:
            
            yield elem
            root.clear()

def validate_element(element, validator, schema=SCHEMA):
    #print(schema)
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))

class UnicodeDictWriter(csv.DictWriter, object):
    def writerow(self, row):
        #print(row)
        super(UnicodeDictWriter, self).writerow({
            
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems() })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
   

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    index = 0
    for child in element:
        if (child.tag == 'tag'):
            m = LOWER_COLON.search(child.attrib['k'])
            colon_type = []
            
            if m:
                colon_type = m.group()
            
            if (child.attrib['k'] in colon_type):
                colon_keys = child.attrib['k'].split(':')
                tags.append({'id': element.attrib['id'],
                'key': colon_keys[1],
                'value': child.attrib['v'],
                'type':colon_keys[0] })
            
            if (child.attrib['k'] not in colon_type ):
                if (child.attrib['k'].find(':')!=-1):
                    keys = child.attrib['k'].split(':',1)
                    tags.append({'id': element.attrib['id'],
                                'key': keys[1],
                                'value': child.attrib['v'],
                                 'type': keys[0] })
                else:
                    tags.append({'id': element.attrib['id'],
                                 'key': child.attrib['k'],
                                 'value': child.attrib['v'],
                                 'type': default_tag_type})
                    
        if (child.tag == 'nd'):
            way_nodes.append({'id':element.attrib['id'],
                              'node_id':child.attrib['ref'],
                              'position':index})
            index += 1;
           
    if element.tag == 'node':
        for field in node_attr_fields:
            node_attribs[field] = element.attrib[field]
        node_result = {}    
        for key,value in node_attribs.items():
            if value not in node_result.values() and value != " ":
                node_result[key] = value    
            
        return {'node': node_result, 'node_tags': tags}
    elif element.tag == 'way':
        for field in way_attr_fields:
            way_attribs[field] = element.attrib[field]
    
        way_result = {}
        
        for key,value in way_attribs.items():
            if value not in way_result.values():
                way_result[key] = value
            
        return {'way': way_result, 'way_nodes': way_nodes, 'way_tags': tags}
#here is the function

def process_map(file_in, validate = True):
          
    with codecs.open(NODES_PATH, 'wb') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'wb') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'wb') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'wb') as way_tags_file:
                nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
                node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
                ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
                way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
                way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)
                                               
        

                nodes_writer.writeheader()
                node_tags_writer.writeheader()
                ways_writer.writeheader()
                way_nodes_writer.writeheader()
                way_tags_writer.writeheader()

                validator = cerberus.Validator()

                for element in get_element(file_in, tags=('node', 'way')):
                    #print(element)
                    el = shape_element(element)
                    if el:
                        if validate is True:
                            validate_element(el, validator)

                        if element.tag == 'node':
                            nodes_writer.writerow(el['node'])
                            node_tags_writer.writerows(el['node_tags'])
                    
                        elif element.tag == 'way':
                            ways_writer.writerow(el['way'])
                            way_nodes_writer.writerows(el['way_nodes'])
                            way_tags_writer.writerows(el['way_tags'])


    
