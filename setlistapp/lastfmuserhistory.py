import json
import urllib2
import time
import pandas as pd
import apikeys

lastfmapikey = apikeys.lastfmapikey

def lastfmuserhist(username, artistname, apikey):
    """User history for the songs listened to by the artist"""
    # Based on the last.fm user_id and artist name, this code gets users
    # history of the songs, album, time listened and artist MBID
    mbid = []
    page = 1
    usersongs = {}
    track = 1

    try:
        # I start with an infinite loop because despite having a totalpages item in
        # the json document, the value is always 0 in the cases I tested.
        while True:
            userhistory = urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getartisttracks&user='
                                          + str(username) + '&artist='
                                          + str(artistname).lower()
                                          + '&page=' + str(page) + '&api_key='
                                          + str(apikey) + '&format=json')
            data = json.load(userhistory)

            # this if clause is what breaks the data when the new page that is
            # loaded in the api has no more new information to report
            if data['artisttracks']['track'] == []:
                # print "success!!!"
                break

        # this is where the code that actually scrapes the data begins
        # what this function does is given the artist name it gets the most
        # listened tracks by the user. also gets mbid code
            else:
                n = 0
                page += 1
                for inf in data['artisttracks']['track']:
                    time.sleep(0.1)
                    if mbid == []:
                        mbid = data['artisttracks'][
                            'track'][n]['artist']['mbid']

        # the mbidold here is mainly for debugging purposes in case there is
        # multiple mbid's coded for one artist in last.fm
                        mbidold = mbid
                        usersongs.update({"track" + str(track): {'trackname': data['artisttracks']['track'][n].get('name'), 'albumname': data['artisttracks']['track'][
                            n].get('name'), 'time': data['artisttracks']['track'][n]['date'].get('#text'), 'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}})
#                        print data['artisttracks']['track'][n]['artist']['mbid']
#                        print data['artisttracks']['track'][n]['name'], data['artisttracks']['track'][n]['album']['#text'], data['artisttracks']['track'][n]['date']['#text']
                        n += 1
                        track += 1

                    else:
                        if data['artisttracks']['track'][n]['artist']['mbid'] == mbidold:
                            usersongs.update({"track" + str(track): {'trackname': data['artisttracks']['track'][n].get('name'), 'albumname': data['artisttracks']['track'][
                                n].get('name'), 'time': data['artisttracks']['track'][n]['date'].get('#text'), 'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}})
#                            print data['artisttracks']['track'][n]['name'], data['artisttracks']['track'][n]['album']['#text'], data['artisttracks']['track'][n]['date']['#text']
                            n += 1
                            track += 1

                        else:
                            mbid = data['artisttracks'][
                                'track'][n]['artist']['mbid']
                            usersongs.update({"track" + str(track): {'trackname': data['artisttracks']['track'][n].get('name'), 'albumname': data['artisttracks']['track'][
                                n].get('name'), 'time': data['artisttracks']['track'][n]['date'].get('#text'), 'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}})
#                            print "Error! mbid conflict! old mbid: " + str(mbidold), "new mbid: " + str(mbid)
#                            print data['artisttracks']['track'][n]['name'], data['artisttracks']['track'][n]['album']['#text'], data['artisttracks']['track'][n]['date']['#text']
                            n += 1
                            track += 1
        print "Last.fm User History Retrieved Successfully!"
        return mbid, usersongs
    except KeyError:
        print "Last.fm Report: you haven't listened to any songs by this band"
        usersongs = {}
        mbid = []
        return mbid, usersongs


def usertopsong(usersongs):
    try:
        """given a dataframe with albumname with trackname column
        returns the top song listened by the user for the band"""

        # because there tends to be a lot of mismatch in song names when users
        # scrobble I strip them and limit the song names to 15 characters with
        # underscores. this aims at catching the number of the beast, and
        # the number of the beast(remastered) as the same song
        # it is not perfect and can be improved but it works good enough for
        # now. Example problem case is trooper, trooper (remastered), and
        # trooper (remixed). trooper and trooper (remastered) and trooper are
        # the same song, but trooper (remix) is a potentially an entirely
        # different song

        usersongs['shorttrackname'] = usersongs[
            'trackname'].str.strip().str.lower().str.replace(' ', '_')
        usersongs['shorttrackname'] = usersongs['shorttrackname'].str[:15]
        usersongs['shorttrackname'] = usersongs[
            'shorttrackname'].str.replace('\_\(.*', '')
        usersongs['counts'] = usersongs.groupby(['shorttrackname'])[
            'trackname'].transform('count')
        usersongs = usersongs.sort_values(by='counts', ascending=[False])
        topsongslist = usersongs.drop_duplicates(
            ['shorttrackname']).sort_values(by='counts', ascending=False)
        median = topsongslist['counts'].median()
        if len(topsongslist) > 15:
            topsongslist = topsongslist[['trackname',  'shorttrackname', 'counts']].iloc[
                :15][topsongslist['counts'] > median]
        else:
            topsongslist = topsongslist[['trackname',  'shorttrackname', 'counts']][
                topsongslist['counts'] > median]
        topsong = topsongslist.iloc[:1]
        topsong = topsong.set_index('trackname')['counts'].to_dict()
        return topsong, topsongslist
    except KeyError:
        topsong = "Unavailable"
        topsongslist = "Unavailable"
        return topsong, topsongslist


def main(username, artistname):
    usersongs = lastfmuserhist(
        username, artistname, apikeys.lastfmapikey)
    usertable = pd.DataFrame(usersongs[1]).T
    usertable['time'] = pd.to_datetime(usertable.time)
    usertable = usertable.sort_values(['time'], ascending=[False])
    usertopsongs = usertopsong(usertable)
    return usertopsongs
