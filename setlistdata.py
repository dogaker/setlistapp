# For getting the json dump for all the setlists of a band


import urllib2
import json
import time


def setlistdata(mbid):
    """Connects to the api and downloads all the setlists data for a band
    using the the mbid"""

    setlist = urllib2.urlopen('http://api.setlist.fm/rest/0.1/artist/' +
                              mbid + '/setlists.json?p=1')
    data = json.load(setlist)

    totalshows = int(data['setlists']['@total'])
    print totalshows

    pages = int(totalshows/20)
    print pages

    data = []
    time.sleep(0.5)
    for page in range(1, pages):
        time.sleep(0.5)
        setlist = urllib2.urlopen('http://api.setlist.fm/rest/0.1/artist/' +
                                  mbid + '/setlists.json?p=' + str(page))
        data.append(json.load(setlist))

    return data
