#!/usr/bin/python
#Weather data extraction from online XML (aemet)


import xml.etree.ElementTree as etree
import urllib2
from datetime import date

## Code starts here

#We obtains today data
todaydate = date.today()

#Download of the xml
xml_url = "http://www.aemet.es/xml/municipios/localidad_28079.xml"
xml_content = urllib2.urlopen(xml_url)

#we obtain the whole XML tree
tree = etree.parse(xml_content)
root = tree.getroot()

#After converting the date string, we check the required fields
str_infodia = ".//dia[@fecha='" + str(todaydate) + "']/temperatura"
info_dia = root.find(str_infodia)
print info_dia.find('minima').text
print info_dia.find('maxima').text

for node in info_dia.iter('dato'):
    print "Temperatura periodo %s: %s" % (node.attrib.get('hora'), node.text)


