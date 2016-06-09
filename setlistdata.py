def setlistdata(mbid):
    # Working code for downloading all of the data of setlists from setlist.fm for an artist

    setlist = urllib2.urlopen('http://api.setlist.fm/rest/0.1/artist/' + mbid + '/setlists.json?p=1')
    data = json.load(setlist)

    totalshows = int(data['setlists']['@total'])
    setlistsongsdetail = []
    setname = []
    print totalshows


    pages = int(totalshows/20)
    print pages
    data = []
    time.sleep(0.5)
    for page in range(1,pages):
        time.sleep(0.5)
        setlist = urllib2.urlopen('http://api.setlist.fm/rest/0.1/artist/' + mbid + '/setlists.json?p=' + str(page))
        data.append(json.load(setlist))


    print "done"
    return data
