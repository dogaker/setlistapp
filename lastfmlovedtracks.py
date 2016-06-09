# this gives us the list of songs that were favorites by the user. I need to
# work on this because for some reason this results in duplicates.
# I need to clean this code up to avoid duplicates

import json
import time
import urllib2


def lastfmlovedtracks(username, mbid, apikey):
    """Gives a list of loved songs in lastfm based on the band's mbid"""
    page = 1
    lovedtracks = {}
    track = 1

    userlovedtracks = urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=' + str(username) + '&page=' + str(page) + '&api_key=' + str(apikey) + '&format=json')
    data = json.load(userlovedtracks)

    totalpages = data['lovedtracks']['@attr']['totalPages']
    for page in range(1, int(totalpages)):
        time.sleep(0.5)
        userlovedtracks = urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=' + str(username) + '&page=' + str(page) + '&api_key=' + str(apikey) + '&format=json')

        n = 0
        for inf in data['lovedtracks']['track']:
            if data['lovedtracks']['track'][n]['artist']['mbid'] == mbid:
                print data['lovedtracks']['track'][n]['artist']['mbid'], data['lovedtracks']['track'][n]['artist']['name'], data['lovedtracks']['track'][n]['name']
                lovedtracks.update({"track"+str(track): {'trackname': data['lovedtracks']['track'][n].get('name'), 'albumname': data['lovedtracks']['track'][n]['artist'].get('name'), 'mbid': data['lovedtracks']['track'][n]['artist'].get('mbid')}})
                track += 1

    #         else:
    #             print "someone else"
            n += 1

    print "success!"
    return lovedtracks
