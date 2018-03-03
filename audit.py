import xml.etree.cElementTree as ET

def get_user(element):
    return
# typecasting
# Where is ET defined?
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if (element.tag == "node" or element.tag == "way" or element.tag == "relation" ):
            users.add(element.attrib['uid'])
            
            element.attrib['id'] =   int(float(element.attrib['id']))
            
            #element.attrib['lat'] =  float(element.attrib['lat'])
            #element.attrib['lon'] =  float(element.attrib['lon'])
            
            element.attrib['uid'] =   int(float(element.attrib['uid']))
            element.attrib['version'] = int(float(element.attrib['version']))
            element.attrib['changeset'] = int(float(element.attrib['changeset'])) 
            element.attrib['timestamp'] = str(element.attrib['timestamp'])
            
           

    return users



