from sklearn import manifold
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, auc
import pandas as pd


def predictsetlist(df):

    df = df.sort_values(by='eventDate')
    df = df.reset_index(drop=True)
    df['played'] = 1
    grouped = df.groupby('eventID')

    df['new_song'] = 0
    df['old_song'] = 0
    songs = []
    newsongscount = 0
    df.sort_values(by='eventDate')
    df['new_song'] = (df.groupby('shorttrackname').cumcount() == 0).astype(int)
    df['old_song'] = (df.groupby('shorttrackname').cumcount() != 0).astype(int)
    df = df[df.shorttrackname != '']
    hashnames = df.set_index('shorttrackname')['songname'].to_dict()
    livesonglist = list(hashnames.keys())
    hashedevents = df.set_index('eventID')['venueID'].to_dict()
    eventidlist = list(hashedevents.keys())

    live_song_list_full = len(eventidlist) * livesonglist
    # len(live_song_list_full)
    live_song_full_df = pd.DataFrame({'shorttrackname': live_song_list_full})
    live_song_full_df = live_song_full_df.reset_index()
    event_id_list_full = len(livesonglist) * eventidlist
    #len(live_song_list_full), len(event_id_list_full)

    event_id_list_full_df = pd.DataFrame({'eventID': event_id_list_full})

    event_id_list_full_df = event_id_list_full_df.sort_values(
        by='eventID').reset_index()
    event_id_list_full_df = event_id_list_full_df.drop('index', axis=1)
    event_id_list_full_df = event_id_list_full_df.reset_index()

    mergeleft = event_id_list_full_df.merge(live_song_full_df, on='index')
    mergeleft['eventtrack'] = mergeleft[
        'eventID'] + mergeleft['shorttrackname']

    df['eventtrack'] = df['eventID'] + df['shorttrackname']
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

    df_full['eventDate'] = grouped_df_full['eventDate'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['artistName'] = grouped_df_full['artistName'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['tour'] = grouped_df_full['tour'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['venueName'] = grouped_df_full['venueName'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['city'] = grouped_df_full['city'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['country'] = grouped_df_full['country'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['countryCode'] = grouped_df_full['countryCode'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['eventDate'] = grouped_df_full['eventDate'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['mbID'] = grouped_df_full['mbID'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['stateCode'] = grouped_df_full['stateCode'].transform(
        lambda s: s.loc[s.first_valid_index()])
    df_full['played'] = grouped_df_full['played'].fillna(0)
    # I need to change this so that it becomes left censored
    df_full['new_song'] = grouped_df_full['new_song'].fillna(0)

    df_full = df_full.sort_values(
        by=['eventDate', 'eventID_x', 'order']).reset_index()

    #limit to last 8000 songs due to memory problems
    df_full_truncated = df_full[-5000:]

    result = pd.get_dummies(df_full_truncated[['shorttrackname_x', 'tour', 'eventID_x', 'city', 'countryCode']], prefix=[
                            'song', 'tour', 'id', 'city', 'country'])
    cols = list(result.columns.values)
    cols.append('new_song')
    cols.append('played')
    df_full_truncated = df_full_truncated.join(result)
    modeldata = df_full_truncated[cols]

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
    probabilities = rf.predict_proba(testx)
    probabilities = pd.DataFrame(probabilities)

    probabilities['results'] = results
    test2 = test1.reset_index()
    probabilities = test2.join(probabilities)
    probabilities = probabilities.rename(columns={1: 'probability'})
    probabilities = probabilities.reset_index()
    df_full = df_full.rename(columns={"index": "oldindex"})
    df_full = df_full.reset_index()

    temp = df_full.merge(probabilities, on='index')
    temp
    predictions = temp[['shorttrackname_x', 'probability', 'results']]
    predictions['songname'] = predictions['shorttrackname_x']
    predictions = predictions.replace({'songname': hashnames})
    predictions['probabilitypercentage'] = pd.Series(["{0:.2f}%".format(
        val * 100) for val in predictions['probability']], index=predictions.index)

    test1['predictions'] = results
    test1.head()

    y_true = test1['played']
    y_scores = test1['predictions']
    roc_score = roc_auc_score(y_true, y_scores)
#    print test1
    print 'predictions complete!'
    return predictions, roc_score, hashnames, test1
