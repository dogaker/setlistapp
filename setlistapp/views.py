from flask import render_template, request, url_for
from setlistapp import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import lastfmuserhistory as lastfm
import setlistfmfunc as setfm
import algorithm as algo
import pics

# at the moment I'm not adding things to postgres this will come soon
# user = 'doa'
# host = 'localhost'
# dbname = 'setlist_db'
# db = create_engine('postgres://%s%s/%s' % (user, host, dbname))
# con = None
# con = psycopg2.connect(database=dbname, user=user)


@app.route('/')
@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/output')
def output():
    # pull 'band_name' and 'user_name' from input field and store it
    artistname = request.args.get('band_name')
    username = request.args.get('user_name')
    print artistname, username

    setlistdf = setfm.main(artistname)
    print setlistdf[3]
    topsetsong = setlistdf[1].keys()
    topsetsong = topsetsong[0]
    topsetsongcount = setlistdf[1][topsetsong]
    print 'setlistdf: done'
    predictions = algo.predictsetlist(setlistdf[0])
    print 'predictions: done'
    usertopsongs = lastfm.main(username, artistname)
    print 'usertopsongs: done'
    fignames = pics.main(predictions[0], usertopsongs[1], username, artistname)
    print 'fignames: done'
    setsfigurename = fignames[0]
    usersongsfigname = fignames[1]
    imagepath1 = url_for('static', filename=str(setsfigurename))
    print imagepath1
    decisionratio = len(set(usertopsongs[1]['shorttrackname']).intersection(predictions[0][predictions[0]['results'] == 1]['shorttrackname_x'])) / float(len(predictions[0][predictions[0]['results']==1]['shorttrackname_x']))
    print decisionratio
    if decisionratio > 0.3:
        decision="GO!"
    else:
        decision="You might want to check out some of the songs the will play before you purchase a ticket."
    print decision
    return render_template('output.html', decision=decision, setsongs=setlistdf[4], band_name=artistname.title(), topsetsong=topsetsong, topsetsongcount=topsetsongcount, imagepath1=url_for('static', filename=str(setsfigurename)), imagepath2=url_for('static', filename=str(usersongsfigname)))
