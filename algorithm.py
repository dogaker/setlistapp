from sklearn import manifold
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, auc
import pandas as pd

def predictsetlist(data):

    df = data
    df = df.sort_values(by = 'eventDate')
    df = df.reset_index(drop=True)
    df['played'] = 1
    grouped = df.groupby('eventID')

    df['new_song']= 0
    df['old_song']= 0
    songs = []
    newsongscount = 0
    for index, row in df.iterrows():

        if row['shorttrackname'] not in songs:
            df.loc[index,'new_song'] = 1
            songs.append(row['shorttrackname'])
            newsongscount+=1
            row['new_song']
#            print songs
#            print newsongscount
        else:
            df.loc[index,'old_song'] = 1

    livesonglist = []
    for index, row in df.iterrows():
        if row['shorttrackname'] not in livesonglist:
            livesonglist.append(row['shorttrackname'])
    if "" in livesonglist:
        livesonglist.remove('')
#    len(livesonglist)


    eventidlist = []
    for index, row in df.iterrows():
        if row['eventID'] not in eventidlist:
            eventidlist.append(row['eventID'])
    #eventidlist
    #len(eventidlist)

    live_song_list_full = len(eventidlist)*livesonglist
    #len(live_song_list_full)
    live_song_full_df = pd.DataFrame({'shorttrackname': live_song_list_full})
    live_song_full_df = live_song_full_df.reset_index()
    event_id_list_full = len(livesonglist)*eventidlist
    #len(live_song_list_full), len(event_id_list_full)


    event_id_list_full_df = pd.DataFrame({'eventID': event_id_list_full})

    event_id_list_full_df = event_id_list_full_df.sort_values(by='eventID').reset_index()
    event_id_list_full_df = event_id_list_full_df.drop('index', axis=1)
    event_id_list_full_df = event_id_list_full_df.reset_index()



    mergeleft = event_id_list_full_df.merge(live_song_full_df, on = 'index')
    mergeleft['eventtrack'] = mergeleft['eventID']+mergeleft['shorttrackname']

    df['eventtrack']=df['eventID']+df['shorttrackname']
#    df = df.drop_duplicates(subset='eventtrack', keep='first')


    df_full = pd.merge(mergeleft, df, on='eventtrack', how='left')
    df_full = df_full[df_full.eventID_x != 0]
    df_full.sort_values(by='eventID_x')

    grouped_df_full = df_full.groupby('eventID_x')

    groupname = list()
    for group in grouped_df_full['eventDate']:
        if pd.isnull(group[1].first_valid_index()):
            groupname.append(group[0])

    df_full = df_full[~df_full['eventID_x'].isin(groupname)]
    grouped_df_full = df_full.groupby('eventID_x')
#    print len(grouped_df_full)

    df_full['eventDate'] = grouped_df_full['eventDate'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['artistName'] = grouped_df_full['artistName'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['tour'] = grouped_df_full['tour'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['venueName'] = grouped_df_full['venueName'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['city'] = grouped_df_full['city'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['country'] = grouped_df_full['country'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['countryCode'] = grouped_df_full['countryCode'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['eventDate'] = grouped_df_full['eventDate'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['mbID'] = grouped_df_full['mbID'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['stateCode'] = grouped_df_full['stateCode'].transform(lambda s: s.loc[s.first_valid_index()])
    df_full['played'] = grouped_df_full['played'].fillna(0)
    df_full['new_song'] = grouped_df_full['new_song'].fillna(0) # I need to change this so that it becomes left censored

    df_full = df_full.sort_values(by = ['eventDate', 'eventID_x', 'order']).reset_index()

    shorttrackname_x_dum = pd.get_dummies(df_full['shorttrackname_x'], prefix='song')
    tour_dum = pd.get_dummies(df_full['tour'], prefix = 'tour')
    eventID_x_dum = pd.get_dummies(df_full['eventID_x'], prefix = 'id')
    city_dum = pd.get_dummies(df_full['city'], prefix = 'city')
    country_dum = pd.get_dummies(df_full['countryCode'], prefix = 'country')

    result = pd.concat([df_full, eventID_x_dum, tour_dum, city_dum, country_dum, shorttrackname_x_dum], axis=1)

    cols = [[col for col in list(result) if col.startswith('tour_')],
              [col for col in list(result) if col.startswith('id_')],
              [col for col in list(result) if col.startswith('country_')],
              [col for col in list(result) if col.startswith('song_')]]

    flattened_cols = [val for sublist in cols for val in sublist]
    modeldata = result[flattened_cols]
    modeldata['new_song'] = result['new_song']
    modeldata['played'] = result['played']
    # modeldata['eventDate']=result['eventDate']
    modeldata = modeldata.dropna()
    train1 = modeldata[:-len(livesonglist)]
    test1 = modeldata[-len(livesonglist):]
    train1y = train1['played']
    train1x = train1.drop('played', 1)
    testx = test1.drop('played', 1)
    rf = RandomForestClassifier(min_samples_split=512)
    rf.fit(train1x, train1y.ravel())

    results = rf.predict(testx)
    test1['predictions'] = results
    test1.head()

    y_true = test1['played']
    y_scores = test1['predictions']
    roc_score = roc_auc_score(y_true, y_scores)
    songspredicted = test1[test1['predictions']>0]

    songspredicted = songspredicted.loc[:, (songspredicted != 0).any(axis=0)]
    songspredicted = [col for col in list(songspredicted) if col.startswith('song_')]
    print songspredicted
    if songspredicted:

        songspredicted = {'predictedsongs': songspredicted}
        songspredicted = pd.DataFrame(songspredicted)
        songspredicted['predictedsongs'] = songspredicted['predictedsongs'].str.replace('song_', '')
        songspredicted['predictedsongs'] = songspredicted['predictedsongs'].str.replace('_', ' ').str.title()
        return songspredicted, roc_score
    else:
        songspredicted = "I can't predict"
        return songspredicted, roc_score
