#!/usr/bin/python

import urllib2
import re
import datetime
from BeautifulSoup import BeautifulSoup as BHTML
from geopy.geocoders import Nominatim
from num2words import num2words

geolocator = Nominatim()

def FindIncidentForDayN(date):
   print "##############################################"
   print "Date; {date}".format(date = date)

   contenturl = "http://www.nanaimo.ca/fire_rescue_incidents/?Date="
   soup = BHTML(urllib2.urlopen(contenturl+date).read())

   table = soup.find('table')
   rows = table.findAll('tr')
   del rows[0]

   for incidents in rows:
       td = incidents.findAll('td')
       time = td[0].contents[0]
       address = td[1].contents[0]
       response = td[2].contents[0]
       apparatus = td[3].find('div').contents[0]

       print "Updated {time}".format(time = time)
       print "Title: {title}".format(title = address + " - " + response)
       print "Original Address: {orig_address}".format(orig_address = address)
       address = address.replace(' BLOCK', '')

       try:
          location = geolocator.geocode(address + ", Nanaimo")
          location.address #Check and see if location has found anything
       except:
          #Currently only handle the problem of not finding the ordinal name ie 5th != Fifth
          fixAddr = address.split(" ")[1:-1]

          print "Problem: {address} ###> NAME: {fixAddr}".format(address = address, fixAddr = fixAddr)
          ordinalWord = re.findall(r'\w*\d+\w*', str(fixAddr)) #Find the word with the Ordinal Value for future replacement

          if not ordinalWord:
             address = address[1:]
          else:
             ordinalVal = re.findall(r'\d+', str(ordinalWord[0])) #Find the number in the Ordinal value
             ordinalVal = int(ordinalVal[0])
             ordinalVal = num2words(ordinalVal, ordinal=True).title() #Get the Word form of the ordinal and title() makes the first character Capitalized for formality

             address = address.replace(ordinalWord[0], ordinalVal)

          print address
          location = geolocator.geocode(address + ", Nanaimo")

       print "Address: {address}".format(address = location.address)
       print "Latitude: {latit}, Longitude: {longit}".format(latit = location.latitude, longit=location.longitude)

       print "Response: {response}".format(response = response)
       print "Apparatus: {apparatus}".format(apparatus = apparatus)
       print "\n"
   print "##############################################"


##MAIN##
StartDate = datetime.date(2005, 01, 29)
EndDate = datetime.date(2005, 02, 03)
day = datetime.timedelta(days=1)

while StartDate < EndDate:
   FindIncidentForDayN(StartDate.strftime('%Y-%m-%d'))
   StartDate = StartDate + day


