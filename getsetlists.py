def setlisthistory(data):
    ### bringing it all together

    count = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    metadata = {}
    setlist = {}
    concert = 1
    livesong = 1


    for i in range(0, len(data)):
        for g in range(0, len(data[i]['setlists']['setlist'])):
            meta = []

            # EventID
            if '@id' in data[i]['setlists']['setlist'][g]:
                eventID = [data[i]['setlists']['setlist'][g].get('@id')]

            #ArtistName
            if '@name' in data[i]['setlists']['setlist'][g]['artist']:
                artistName = [data[i]['setlists']['setlist'][g]['artist'].get('@name')]

            mbID = {'mbid': mbid}
            # Eventdate
            if '@eventDate' in data[i]['setlists']['setlist'][g]:
                eventDate = [data[i]['setlists']['setlist'][g].get('@eventDate')]

            #venueName
            if '@name' in data[i]['setlists']['setlist'][g]['venue']:
                venueName = [data[i]['setlists']['setlist'][g]['venue'].get('@name')]

            #venueID
            if '@id' in data[i]["setlists"]["setlist"][g]["venue"]:
                venueID = [data[i]["setlists"]["setlist"][g]["venue"].get("@id")]

            #cityName
            if '@name' in data[i]['setlists']['setlist'][g]['venue']['city']:
                city = [data[i]['setlists']['setlist'][g]['venue']['city'].get('@name')]

            #stateCode
            if '@stateCode' in data[i]['setlists']['setlist'][g]['venue']['city']:
                stateCode = [data[i]['setlists']['setlist'][g]['venue']['city'].get('@stateCode')]

            #countryName
            if '@name' in data[i]["setlists"]["setlist"][g]["venue"]["city"]["country"]:
                country = [data[i]["setlists"]["setlist"][g]["venue"]["city"]["country"].get("@name")]

            #countryCode
            if '@code' in data[i]["setlists"]["setlist"][g]["venue"]["city"]["country"]:
                countryCode = [data[i]["setlists"]["setlist"][g]["venue"]["city"]["country"].get("@code")]

            #tourName
            if '@tour' in data[i]['setlists']['setlist'][g]:
                tour = [data[i]['setlists']['setlist'][g].get('@tour')]

            meta = {'concert'+str(concert):{'eventID': eventID, 'artistName':artistName, 'mbID':mbID, 'eventDate':eventDate, 'venueName':venueName, 'venueID':venueID, 'city':city, 'stateCode':stateCode, 'country':country, 'countryCode':countryCode, 'tour':tour}}
            metadata.update(meta)
            concert += 1


    ### the rest of the code works on actually getting each song title, whether they are a cover or not and
    ### makes a list of dictionaries that matches each song to an eventid along with assigning them encore status
    ### and the order the song was played in the set

            if type(data[i]['setlists']['setlist'][g]['sets']) is dict:

                for z in range(0, len(data[i]['setlists']['setlist'][g]['sets']['set'])):

                    order = 0
                    count +=1
                    if type(data[i]['setlists']['setlist'][g]['sets']['set']) is list:
                        for w in range(0, len(data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'])):
                            song = []
                            if type(data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']) is list:
                                if type(data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w]) is dict:
                                    songname = data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w].get('@name')
                                    print data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w]['@name']
                                    print i, g, z, w, count, count4
                                    count4 += 1
                                    order += 1
                                    songorder = {'order':order}
                                    if 'cover' in data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w]:
                                        coverinfo = data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w].get('cover')
                                    else:
                                        coverinfo = {'cover': 0}
                                    song = {'song'+str(livesong):{'eventID':eventID, 'order':order, 'songname':songname, 'coverinfo':coverinfo}}
                                    setlist.update(song)
                                    livesong+=1

                                else:
                                    print data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']
                                    print i, g, z, w, count, count4
                                    count4 += 1
                                    print data['setlist']
                                    print 'error type: setsl[i][g]["song][z] is not dict'
                                    print data['setlist']
                                    print data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'][w]['@name']
                                    song = {'song'+str(livesong):{'eventID':eventID, 'order':order, 'songname':songname, 'coverinfo':coverinfo}}
                                    setlist.update(song)
                                    livesong+=1

                            elif type(data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']) is dict:
                                songname = {'songname':data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'].get('@name')}
                                print data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']['@name']
                                print i, g, z, w, count, count4
                                count4 += 1
                                order +=1
                                songorder = {'order':order}
                                if 'cover' in data[i]['setlists']['setlist'][g]['sets']['set'][z]['song']:
                                    coverinfo = {'cover':data[i]['setlists']['setlist'][g]['sets']['set'][z]['song'].get('cover')}
                                else:
                                    coverinfo = 0
                                song = {'song'+str(livesong):{'eventID':eventID, 'order':order, 'songname':songname, 'coverinfo':coverinfo}}
                                setlist.update(song)
                                livesong+=1

                            else:
                                print i, g, z, w, count, count4
                                print 'something weird here'
                                print data[i]['setlists']['setlist'][g]['sets'][z]['song'][w]['@name']
                                song = {'song'+str(livesong):{'eventID':eventID, 'order':order, 'songname':songname, 'coverinfo':coverinfo}}
                                setlist.update(song)
                                livesong+=1

                    elif type(data[i]['setlists']['setlist'][g]['sets']['set']) is dict:
                        if type(data[i]['setlists']['setlist'][g]['sets']['set']['song']) is list:
                            for z in range(0, len(data[i]['setlists']['setlist'][g]['sets']['set']['song'])):
                                if type(data[i]['setlists']['setlist'][g]['sets']['set']['song'][z]) is dict:
                                    songname = {'songname':data[i]['setlists']['setlist'][g]['sets']['set']['song'][z]}
                                    print data[i]['setlists']['setlist'][g]['sets']['set']['song'][z]['@name']
                                    print i, g, z, count, count4
                                    count4 += 1
                                    order +=1
                                    songorder = {'order': order}
                                    if 'cover' in data[i]['setlists']['setlist'][g]['sets']['set']['song'][z]:
                                        coverinfo = {'cover':data[i]['setlists']['setlist'][g]['sets']['set']['song'][z].get('cover')}
                                    else:
                                        coverinfo = 0
                                    song = {'song'+str(livesong):{'eventID':eventID, 'order':order, 'songname':songname, 'coverinfo':coverinfo}}
                                    setlist.update(song)
                                    livesong+=1

                                else:
                                    print "something weird here"
                                    print i, g, z, count, count4
                                    break

                        elif type(data[i]['setlists']['setlist'][g]['sets']['set']['song']) is dict:
                            print i, g, z, count, count4
                            songname = {'songname':data[i]['setlists']['setlist'][g]['sets']['set']['song'].get('@name')}
                            print [data[i]['setlists']['setlist'][g]['sets']['set']['song']]
                            count4 +=1
                            order += 1
                            songorder = {'order':order}
                            if 'cover' in data[i]['setlists']['setlist'][g]['sets']['set']['song']:
                                coverinfo = {'cover':data[i]['setlists']['setlist'][g]['sets']['set']['song'].get('cover')}
                            else:
                                coverinfo = 0
                            song = {'song'+str(livesong):{'eventID':eventID, 'order':order, 'songname':songname, 'coverinfo':coverinfo}}
                            setlist.update(song)
                            livesong+=1



            elif data[i]['setlists']['setlist'][g]['sets'] is u"":
                count2 +=1
                print "this setlist among with", count2, "setlists were discarded because they were empty."

            else:
                print "data[i]['setlists']['setlist'][g]['sets'] is not a dictionary, so what is it?"
                print 'weird stuff count:', i, g, count, count4
                count1 +=1
                setsl.append(data[i]['setlists']['setlist'][g]['sets'].get('set'))

    print "songs scraped:", count4
    print "setlists scraped:", count
    print "empty setlists", count2
    print "donedonedonedone"
    return setlist
