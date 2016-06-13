from flask import render_template, request
from setlistapp import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import lastfmuserhistory

user = 'doa'
host = 'localhost'
dbname = 'setlist_db'
db = create_engine('postgres://%s%s/%s' % (user, host, dbname))
con = None
con = psycopg2.connect(database=dbname, user=user)


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template("index.html",
                           title='Home',
                           user=user)


@app.route('/db_fancy')
def userhistory_page_fancy():
    sql_query = """
               SELECT trackname, time FROM userhistory ORDER BY time DESC;
                """
    query_results = pd.read_sql_query(sql_query, con)
    tracks = []
    for i in range(0, query_results.shape[0]):
        print query_results.iloc[i]['trackname']
        print query_results.iloc[i]['time']
        tracks.append(dict(trackname=query_results.iloc[i]['trackname'].decode('utf-8'),
                           time=query_results.iloc[i]['time']))
    return render_template('userhistory.html', tracks=tracks)


@app.route('/input')
def userhistory_input():
    return render_template('input.html')


@app.route('/output')
def userhistory_output():
    # pull 'birth_month' from input field and store it
    artistname = request.args.get('band_name')
    username = request.args.get('user_name')
    print artistname, username

    # just select the Cesareans  from the birth dtabase for the month that the
    # user inputs
    query = lastfmuserhistory.lastfmuserhist(username, artistname,
                                             'ea12d08886bb0a05492c813a99164027')
    table = pd.DataFrame(query[1]).T
    tracks = []
    for i in range(0, table.shape[0]):
        print table.iloc[i]['trackname']
        print table.iloc[i]['albumname']
        print table.iloc[i]['time']
        tracks.append(dict(trackname=table.iloc[i]['trackname'].decode(
            'utf-8'), albumname=table.iloc[i]['albumname'].decode('utf-8'),
            time=table.iloc[i]['time']))
        the_result = lastfmuserhistory.usertopsong(table)
    return render_template('output.html', tracks=tracks, the_result=the_result, band_name = artistname, user_name = username)
