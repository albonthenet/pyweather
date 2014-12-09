#!/usr/bin/python
#Weather data extraction from online XML (aemet)


import xml.etree.ElementTree as etree
import urllib2

## Code starts here

#Download of the xml
xml_url = "http://www.aemet.es/xml/municipios/localidad_28079.xml"
xml_content = urllib2.urlopen(xml_url)
#xml_content = s.read()

tree = etree.parse(xml_content)
root = tree.getroot()


info_dia = root.find(".//dia[@fecha='2014-12-08']/temperatura")
print info_dia.find('minima').text
print info_dia.find('maxima').text

"""
#for temp in root.iter(".//dia[@fecha='2014-12-08']"):
for temp in root.iter("dia"):
    print temp.get('fecha')
    for temp2 in temp.iter('temperatura'):
        print temp2.find('maxima').text
        print temp2.find('minima').text
        

for temp in root.iter('temperatura'):
    t_max = temp.find('maxima').text
    t_min = temp.find('minima').text
    print t_max, t_min
    


#for temp in root.iter('temperatura'):
#    print temp.attrib, temp.text

#for child in root:
#        print child.tag, child.attrib
"""
