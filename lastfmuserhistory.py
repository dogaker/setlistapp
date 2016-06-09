import json
import urllib2
import pandas as pd
import time

def lastfmuserhistory(username, artistname, apikey):
    # Based on the last.fm user_id and artist name, this code gets users history of the songs, album, time listened and artist MBID

    mbid = []
    page = 1
    songslistened = {}
    track = 1


    # I start with an infinite loop because despite having a totalpages item in the json document, the value is always 0 in the cases I tested.
    while True:
        userhistory = urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getartisttracks&user='
                                  + str(username) + '&artist=' + str(artistname).lower() + '&page=' + str(page) + '&api_key='
                                  + str(apikey) + '&format=json')
        data = json.load(userhistory)

        #this if clause is what breaks the data when the new page that is loaded in the api has no more new information to report

        if data['artisttracks']['track'] == []:
    #        print "success!!!"
            break


    # debugging code for test cases where I knew how many pages were supposed to load in total
    #     if page >= 16:
    #         print "page = 20. we failed!"
    #         break


    # this is where the code that actually scrapes the data begins
    # what this function does is given the artist name it gets the most listened tracks by the user.
    # it also gets the mbid code which is the standard code reported in all the API I'm using

        else:

            n = 0
            page += 1
            for inf in data['artisttracks']['track']:
                time.sleep(0.5)
                if mbid == []:
                    mbid = data['artisttracks']['track'][n]['artist']['mbid']
    # the mbidold here is mainly for debugging purposes in case there is multiple mbid's coded for one artist in last.fm
                    mbidold = mbid
    #                 trackname = {'trackname': data['artisttracks']['track'][n].get('name')}
    #                 albumname = {'albumname': data['artisttracks']['track'][n].get('name')}

#                     songslistened.append([{'trackname': data['artisttracks']['track'][n].get('name')}, {'albumname': data['artisttracks']['track'][n].get('name')}, {'time': data['artisttracks']['track'][n]['date'].get('#text')}, {'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}])
                    songslistened.update({"track"+str(track):{'trackname': data['artisttracks']['track'][n].get('name'), 'albumname': data['artisttracks']['track'][n].get('name'), 'time': data['artisttracks']['track'][n]['date'].get('#text'), 'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}})
#                    songslistened.update(songs)


                    print data['artisttracks']['track'][n]['artist']['mbid']
                    print data['artisttracks']['track'][n]['name'], data['artisttracks']['track'][n]['album']['#text'], data['artisttracks']['track'][n]['date']['#text']
                    n+=1
                    track +=1

                else:
                    if data['artisttracks']['track'][n]['artist']['mbid'] == mbidold:
#                         songslistened.append([{'trackname': data['artisttracks']['track'][n].get('name')}, {'albumname': data['artisttracks']['track'][n].get('name')}, {'time': data['artisttracks']['track'][n]['date'].get('#text')}, {'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}])
#                         songs = {"track"+str(track):{'trackname': data['artisttracks']['track'][n].get('name'), 'albumname': data['artisttracks']['track'][n].get('name'), 'time': data['artisttracks']['track'][n]['date'].get('#text'), 'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}}
#                         songslistened.update(songs)
                        songslistened.update({"track"+str(track):{'trackname': data['artisttracks']['track'][n].get('name'), 'albumname': data['artisttracks']['track'][n].get('name'), 'time': data['artisttracks']['track'][n]['date'].get('#text'), 'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}})





                        print data['artisttracks']['track'][n]['name'], data['artisttracks']['track'][n]['album']['#text'], data['artisttracks']['track'][n]['date']['#text']
                        n+=1
                        track +=1




                    else:
                        mbid = data['artisttracks']['track'][n]['artist']['mbid']
#                         songslistened.append([{'trackname': data['artisttracks']['track'][n].get('name')}, {'albumname': data['artisttracks']['track'][n].get('name')}, {'time': data['artisttracks']['track'][n]['date'].get('#text')}, {'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}])
#                         songs = {"track"+str(track):{'trackname': data['artisttracks']['track'][n].get('name'), 'albumname': data['artisttracks']['track'][n].get('name'), 'time': data['artisttracks']['track'][n]['date'].get('#text'), 'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}}
#                         songslistened.update(songs)
                        songslistened.update({"track"+str(track):{'trackname': data['artisttracks']['track'][n].get('name'), 'albumname': data['artisttracks']['track'][n].get('name'), 'time': data['artisttracks']['track'][n]['date'].get('#text'), 'mbid': data['artisttracks']['track'][n]['artist'].get('mbid')}})


                        print "Error! mbid conflict! old mbid: " + str(mbidold), "new mbid: " + str(mbid)
                        print data['artisttracks']['track'][n]['name'], data['artisttracks']['track'][n]['album']['#text'], data['artisttracks']['track'][n]['date']['#text']
                        n+=1
                        track +=1
    print "Success!"
    return mbid, songslistened
