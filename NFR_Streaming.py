#!/usr/bin/python

import feedparser
from BeautifulSoup import BeautifulSoup as BHTML
from geopy.geocoders import Nominatim

geolocator = Nominatim()

NFR_rss_url = "http://www.nanaimo.ca/fire_rescue_incidents/Rss"

feed = feedparser.parse(NFR_rss_url)

for incidents in feed['entries']:
    incidents
    print "Updated {time}".format(time = incidents['updated'])
    print "Title: {title}".format(title = incidents['title'])
    summary = incidents['summary'].split('\n')[0]
    responseType = BHTML(incidents['summary']).li.contents[0].strip()
    print "Summary: {summary}".format(summary = summary + " " + responseType)
    value = incidents['title_detail']['value']
    value = value.split(" - ")
    print "Original Address: {orig_address}".format(orig_address = value[0])
    address = value[0].replace(' BLOCK', '')
    location = geolocator.geocode(address + ", Nanaimo")
    print "Address: {address}".format(address = location.address)
    print "Latitude: {latit}, Longitude: {longit}".format(latit = location.latitude, longit=location.longitude)
    print "Response: {response}".format(response = value[1])
    print "Apparatus: {apparatus}".format(apparatus = responseType)
    print "Id: {idval}\n".format(idval = incidents['id'].split("/")[-1])
