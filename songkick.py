import time
import pandas as pd


def getgigs(mbid, apikey):
    venue_data_songkick = {}
    event_data_songkick = {}
    temp = urllib2.urlopen('http://api.songkick.com/api/3.0/artists/mbid:' +
                           mbid + '/gigography.json?apikey=' + apikey + '&order=desc')
    setlistdata = json.load(temp)
    venuecount = 0

    totalshows = int(setlistdata['resultsPage']['totalEntries'])
    print totalshows

    pages = int(totalshows / 50)
    print pages

    added_count = 0
    already_there_count = 0
    event_added_count = 0
    data = []
    venue_id_list = []
    time.sleep(0.2)

    for page in range(1, pages):
        time.sleep(0.2)
        setlist = urllib2.urlopen('http://api.songkick.com/api/3.0/artists/mbid:' +
                                  mbid + '/gigography.json?apikey=' + apikey + '&order=desc')
        data.append(json.load(setlist))
        for i in range(0, len(data)):
            time.sleep(0.2)
            for w in range(0, len(data[i]['resultsPage']['results']['event'])):

                if 'displayName' in data[i]['resultsPage']['results']['event'][w]:
                    gig_billing_title = data[i]['resultsPage'][
                        'results']['event'][w].get('displayName')
                else:
                    gig_billing_title = ""

                if 'id' in data[i]['resultsPage']['results']['event'][w]['venue']:
                    venue_id_songkick = data[i]['resultsPage'][
                        'results']['event'][w]['venue'].get('id')
                else:
                    venue_id_songkick = ""

                if 'displayName' in data[i]['resultsPage']['results']['event'][w]['venue']['displayName']:
                    venue_name = data[i]['resultsPage']['results'][
                        'event'][w]['venue'].get('displayName')
                else:
                    venue_name = ""

                if 'uri' in data[i]['resultsPage']['results']['event'][w]['uri']:
                    gig_uri = data[i]['resultsPage'][
                        'results']['event'][w].get('uri')
                else:
                    gig_uri = ""

                if 'date' in data[i]['resultsPage']['results']['event'][w]['start']:
                    event_date = data[i]['resultsPage'][
                        'results']['event'][w]['start'].get('date')
                else:
                    event_date = ""

                if 'city' in data[i]['resultsPage']['results']['event'][w]['location']:
                    event_city = data[i]['resultsPage']['results'][
                        'event'][w]['location'].get('city')
                else:
                    event_city = ''

                if 'performance' in data[i]['resultsPage']['results']['event'][w]:

                    for x in range(0, len(data[i]['resultsPage']['results']['event'][w]['performance'])):

                        if 'billingIndex' in data[i]['resultsPage']['results']['event'][w]['performance'][x]:
                            event_billing_index = data[i]['resultsPage']['results'][
                                'event'][w]['performance'][x].get('billingIndex')
                        else:
                            event_billing_index = ""
                        if 'id' in data[i]['resultsPage']['results']['event'][w]['performance'][x]:
                            event_id_songkick = data[i]['resultsPage'][
                                'results']['event'][w]['performance'][x].get('id')
                        else:
                            event_id_songkick = ""
                        if 'billing' in data[i]['resultsPage']['results']['event'][w]['performance'][x]:
                            event_billing = data[i]['resultsPage']['results'][
                                'event'][w]['performance'][x].get('billing')
                        else:
                            event_billing = ""
                        if 'artist' in data[i]['resultsPage']['results']['event'][w]['performance'][x]:

                            if 'displayName' in data[i]['resultsPage']['results']['event'][w]['performance'][x]['artist']:
                                artist_name = data[i]['resultsPage']['results']['event'][
                                    w]['performance'][x]['artist'].get('displayName')
                            else:
                                artist_name = ""
                            if 'id' in data[i]['resultsPage']['results']['event'][w]['performance'][x]['artist']:
                                artist_id_songkick = data[i]['resultsPage']['results'][
                                    'event'][w]['performance'][x]['artist'].get('id')
                            else:
                                artist_id_songkick = ""
                gig_metadata = {'gig' + str(event_added_count) + gig_billing_title: {'gig_billing_title': gig_billing_title,
                                                            'venue_id_songkick': venue_id_songkick,
                                                            'venue_name': venue_name, 'gig_uri': gig_uri,
                                                            'event_date': event_date, 'event_city': event_city,
                                                            'event_billing_index': event_billing_index,
                                                            'event_id_songkick': event_id_songkick,
                                                            'event_billing': event_billing,
                                                            'artist_name': artist_name, 'artist_id_songkick': artist_id_songkick}}

                if venue_id_songkick:
                    print "page:", page, 'i:',  i, 'w:', w
                    print data[i]['resultsPage']['results']['event'][w]['venue']['displayName']
                    if venue_id_songkick not in venue_id_list:
                        venue_id_list.append(venue_id_songkick)
                        time.sleep(0.2)
                        socket = urllib2.urlopen(
                            'http://api.songkick.com/api/3.0/venues/' + str(venue_id_songkick) + '.json?apikey=' + apikey)

                        venuedata = json.load(socket)
                        print i
                        if 'capacity' in venuedata['resultsPage']['results']['venue']:
                            venue_capacity = venuedata['resultsPage'][
                                'results']['venue'].get('capacity')
                        else:
                            venue_capacity = ""

                        if 'displayName' in venuedata['resultsPage']['results']['venue']['city']:
                            venue_city = venuedata['resultsPage']['results'][
                                'venue']['city'].get('displayName')
                        else:
                            venue_city = ""

                        if 'state' in venuedata['resultsPage']['results']['venue']['city']:
                            venue_state = venuedata['resultsPage']['results'][
                                'venue']['city']['state'].get('displayName')

                        else:
                            venue_state = ""

                        if 'displayName' in venuedata['resultsPage']['results']['venue']['city']['country']:
                            venue_country = venuedata['resultsPage']['results'][
                                'venue']['city']['country'].get('displayName')
                        else:
                            venue_country = ""

                        if 'id' in venuedata['resultsPage']['results']['venue']:
                            venue_id_songkick = venuedata['resultsPage'][
                                'results']['venue'].get('id')
                        else:
                            venue_id_songkick = ""

                        if 'lat' in venuedata['resultsPage']['results']['venue']:
                            venue_latitude = venuedata['resultsPage'][
                                'results']['venue'].get('lat')
                        else:
                            venue_latitude = ""

                        if 'lng' in venuedata['resultsPage']['results']['venue']:
                            venue_longitude = venuedata['resultsPage'][
                                'results']['venue'].get('lng')
                        else:
                            venue_longitude = ""

                        if 'displayName' in venuedata['resultsPage']['results']['venue']:
                            venue_display_name = venuedata['resultsPage'][
                                'results']['venue'].get('displayName')
                        else:
                            venue_display_name = ""

                        venue_metadata = {'venue' + str(venuecount) + venue_display_name: {'venue_capacity': venue_capacity, 'venue_city': venue_city, 'venue_state': venue_state, 'venue_country': venue_country,
                                                                         'venue_id_songkick': venue_id_songkick, 'venue_latitude': venue_latitude, 'venue_longitude': venue_longitude, 'venue_display_name': venue_display_name}}
                        venue_data_songkick.update(venue_metadata)
                        print venuecount
                        print venuedata['resultsPage']['results']['venue']['displayName']
                        venuecount += 1
                        print "ADDED IT", "added count:", added_count
                        added_count += 1
                    else:
                        print "ALREADY THERE!!!", "already there count:", already_there_count
                        already_there_count += 1

                event_data_songkick.update(gig_metadata)
                print "event_data_added", 'added count:', event_added_count
                print "items in event_data_added:", len(event_data_songkick)
                event_added_count += 1

    venue_df_songkick = pd.DataFrame(venue_data_songkick).T
    event_df_songkick = pd.DataFrame(event_data_songkick).T

    return venue_df_songkick, event_df_songkick, added_count, already_there_count, event_added_count
