import urllib2
import json
import time
import pandas as pd


def setlistdata(mbid):
    """Connects to the api and downloads all the setlists data for a band
    using the the mbid"""

    setlist = urllib2.urlopen('http://api.setlist.fm/rest/0.1/artist/' +
                              mbid + '/setlists.json?p=1')
    data = json.load(setlist)

    totalshows = int(data['setlists']['@total'])
    print totalshows

    pages = int(totalshows / 20)
    print pages

    data = []
    time.sleep(0.5)
    for page in range(1, pages):
        time.sleep(0.5)
        setlist = urllib2.urlopen('http://api.setlist.fm/rest/0.1/artist/' +
                                  mbid + '/setlists.json?p=' + str(page))
        data.append(json.load(setlist))

    return data


def getsetlists(data, mbid):
    """given the json dump, gives out a nice dict of dicts for placing in
    pandas"""

    setlistcount = 0
    emptysetlistcount = 0
    songcount = 0
    dictcount = 0
    metadata = {}
    setlist = {}
    concert = 1
    livesong = 1

    for i in range(0, len(data)):
        for g in range(0, len(data[i]['setlists']['setlist'])):
            meta = []

            # EventID
            if '@id' in data[i]['setlists']['setlist'][g]:
                eventID = data[i]['setlists']['setlist'][g].get('@id')

            # ArtistName
            if '@name' in data[i]['setlists']['setlist'][g]['artist']:
                artistName = data[i]['setlists'][
                    'setlist'][g]['artist'].get('@name')

            # Eventdate
            if '@eventDate' in data[i]['setlists']['setlist'][g]:
                eventDate = data[i]['setlists']['setlist'][g].get('@eventDate')

            # venueName
            if '@name' in data[i]['setlists']['setlist'][g]['venue']:
                venueName = data[i]['setlists'][
                    'setlist'][g]['venue'].get('@name')

            # venueID
            if '@id' in data[i]["setlists"]["setlist"][g]["venue"]:
                venueID = data[i]["setlists"]["setlist"][g]["venue"].get("@id")

            # cityName
            if '@name' in data[i]['setlists']['setlist'][g]['venue']['city']:
                city = data[i]['setlists']['setlist'][
                    g]['venue']['city'].get('@name')

            # stateCode
            if '@stateCode' in data[i]['setlists']['setlist'][g]['venue']['city']:
                stateCode = data[i]['setlists']['setlist'][
                    g]['venue']['city'].get('@stateCode')

            # countryName
            if '@name' in data[i]["setlists"]["setlist"][g]["venue"]["city"]["country"]:
                country = data[i]["setlists"]["setlist"][g][
                    "venue"]["city"]["country"].get("@name")

            # countryCode
            if '@code' in data[i]["setlists"]["setlist"][g]["venue"]["city"]["country"]:
                countryCode = data[i]["setlists"]["setlist"][
                    g]["venue"]["city"]["country"].get("@code")

            # tourName
            if '@tour' in data[i]['setlists']['setlist'][g]:
                tour = data[i]['setlists']['setlist'][g].get('@tour')

            meta = {'concert' + str(concert): {'eventID': eventID, 'artistName': artistName, 'mbID': mbid, 'eventDate': eventDate, 'venueName': venueName,
                                               'venueID': venueID, 'city': city, 'stateCode': stateCode, 'country': country, 'countryCode': countryCode, 'tour': tour}}
            metadata.update(meta)
            concert += 1

    # the rest of the code works on actually getting each song title,
    # whether they are a cover or not and makes a list of dictionaries
    # that matches each song to an eventid along with assigning them encore
    # status and the order the song was played in the set
    # hardcoding seemed to be the most efficient thing to do after various
    # debugging. the data is user generated and other methods resulted in a
    # lot of scraping faults. a lot of these if/then statements are for classes
    # such as a band playing a concert with multiple sets,
    # playing a concert with only one song sets, etc.

            if type(data[i]['setlists']['setlist'][g]['sets']) is dict:

                for z in range(0, len(data[i]['setlists']['setlist'][g]['sets']['set'])):

                    order = 0
                    setlistcount += 1
                    if type(data[i]['setlists']['setlist'][g]['sets']['set']) is list:
                        for w in range(0, len(data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'])):
                            song = []
                            if type(data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']) is list:
                                if type(data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w]) is dict:
                                    songname = data[i]['setlists']['setlist'][g][
                                        'sets']['set'][z]['song'][w].get('@name')
                                    if type(songname) is dict:
                                        print "this needs to be fixed"
                                        dictcount += 1
                                    print data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w]['@name']
                                    print i, g, z, w, setlistcount, songcount
                                    songcount += 1
                                    order += 1
                                    if 'cover' in data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w]:
                                        coverinfo = 1
                                    else:
                                        coverinfo = 0
                                    song = {'song' + str(livesong): {
                                        'eventID': eventID, 'order': order, 'songname': songname, 'coverinfo': coverinfo}}
                                    setlist.update(song)
                                    livesong += 1

                                else:
                                    print data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']
                                    print i, g, z, w, setlistcount, songcount
                                    songcount += 1
                                    print data['setlist']
                                    print 'error type: setsl[i][g]["song][z] is not dict'
                                    print data['setlist']
                                    print data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w]['@name']
                                    song = {'song' + str(livesong): {
                                        'eventID': eventID, 'order': order, 'songname': songname, 'coverinfo': coverinfo}}
                                    setlist.update(song)
                                    livesong += 1

                            elif type(data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']) is dict:
                                songname = data[i]['setlists']['setlist'][
                                    g]['sets']['set'][z]['song'].get('@name')
                                if type(songname) is dict:
                                    print "this needs to be fixed"
                                    dictcount += 1
                                print data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']['@name']
                                print i, g, z, w, setlistcount, songcount
                                songcount += 1
                                order += 1
                                if 'cover' in data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']:
                                    coverinfo = 1
                                else:
                                    coverinfo = 0
                                song = {'song' + str(livesong): {
                                    'eventID': eventID, 'order': order, 'songname': songname, 'coverinfo': coverinfo}}
                                setlist.update(song)
                                livesong += 1

                            else:
                                print i, g, z, w, setlistcount, songcount
                                print 'something weird here'
                                print data[i]['setlists']['setlist'][g]['sets'][z]['song'][w]['@name']
                                song = {'song' + str(livesong): {
                                    'eventID': eventID, 'order': order, 'songname': songname, 'coverinfo': coverinfo}}
                                setlist.update(song)
                                livesong += 1

                    elif type(data[i]['setlists']['setlist'][g]['sets']['set']) is dict:
                        if type(data[i]['setlists']['setlist'][g]['sets']['set']['song']) is list:
                            for z in range(0, len(data[i]['setlists']['setlist'][g]['sets']['set']['song'])):
                                if type(data[i]['setlists']['setlist'][g]['sets']['set']['song'][z]) is dict:
                                    songname = data[i]['setlists']['setlist'][
                                        g]['sets']['set']['song'][z].get('@name')
                                    if type(songname) is dict:
                                        print "this needs to be fixed"
                                        dictcount += 1
                                    print data[i]['setlists']['setlist'][g]['sets']['set']['song'][z]['@name']
                                    print i, g, z, setlistcount, songcount
                                    songcount += 1
                                    order += 1
                                    if 'cover' in data[i]['setlists']['setlist'][g]['sets']['set']['song'][z]:
                                        coverinfo = 1
                                    else:
                                        coverinfo = 0
                                    song = {'song' + str(livesong): {
                                        'eventID': eventID, 'order': order, 'songname': songname, 'coverinfo': coverinfo}}
                                    setlist.update(song)
                                    livesong += 1

                                else:
                                    print "something weird here"
                                    print i, g, z, setlistcount, songcount
                                    break

                        elif type(data[i]['setlists']['setlist'][g]['sets']['set']['song']) is dict:
                            print i, g, z, setlistcount, songcount
                            songname = data[i]['setlists']['setlist'][
                                g]['sets']['set']['song'].get('@name')
                            if type(songname) is dict:
                                print "this needs to be fixed"
                                dictcount += 1
                            print [data[i]['setlists']['setlist']
                                   [g]['sets']['set']['song']]
                            songcount += 1
                            order += 1
                            if 'cover' in data[i]['setlists']['setlist'][g]['sets']['set']['song']:
                                coverinfo = 1
                            else:
                                coverinfo = 0
                            song = {'song' + str(livesong): {'eventID': eventID, 'order': order,
                                                             'songname': songname, 'coverinfo': coverinfo}}
                            setlist.update(song)
                            livesong += 1

            elif data[i]['setlists']['setlist'][g]['sets'] is u"":
                emptysetlistcount += 1
                print "this setlist among with", emptysetlistcount, "setlists were discarded because they were empty."

            else:
                print "data[i]['setlists']['setlist'][g]['sets'] is not a dictionary, so what is it?"
                print 'weird stuff count:', i, g, setlistcount, songcount

    print "songs scraped:", songcount
    print "setlists scraped:", setlistcount
    print "empty setlists", emptysetlistcount
    print "dicts in songnames:", dictcount
    print "donedonedonedone"

    metadata = pd.DataFrame(metadata).T
    setlist = pd.DataFrame(setlist).T
    setlist_data = pd.merge(setlist, metadata, on=['eventID'])
    setlist_data['shorttrackname'] = setlist_data['songname'].str.strip(
    ).str.lower().str.replace(' ', '_').str[:15].str.replace('\_\(.*', '')
    setlist_data['eventDate'] = pd.to_datetime(setlist_data.eventDate)
    topsetsongs = setlist_data.groupby('shorttrackname')
    topsetsong = topsetsongs.count().sort_values(
        by='songname', ascending=[False]).head().index[0]
    topsetsong = topsetsongs.count().sort_values(
        by='songname', ascending=[False]).head().index[0]
    topsetsong = (setlist_data['songname'].loc[
                  setlist_data['shorttrackname'] == topsetsong]).iloc[0]
    topsetsongs = topsetsongs.count().sort_values(
        by='songname', ascending=[False]).index.tolist()
    counts = {'songs_scraped': songcount, 'setlists_scraped': setlistcount}
    return setlist_data, topsetsong, topsetsongs, counts
