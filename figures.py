import matplotlib.pyplot as plt
import pandas as pd


def setsongsfig(setlistdf, artistname):
    plt.style.use('bmh')
    fig = plt.figure()
    df = setlistdf.sort_values(by='probability', ascending=False)

    df.loc[df.probability >= 0.5, 'colormap'] = 'g'
    df.loc[df.probability < 0.5, 'colormap'] = 'y'
    df.loc[df.probability < 0.2, 'colormap'] = 'r'

    df = df.iloc[:30].sort_values(by='probability', ascending=True)
    colormap = df['colormap'].tolist()
    df2.plot.barh(x='songname', y='probability', color=colormap)
    setsfigurename = str(artistname + '-predsongs.png')
    fig.savefig('static/img/'+ setsfigurename)
    return setsfigurename

def usersongsfig(setlistdf, usersongsdf, username, artistname):
    plt.style.use('bmh')
    fig = plt.figure()

    df = usersongsdf.merge(setlistdf, left_on='shorttrackname', right_on='shorttrackname_x')
    df.loc[df3.probability >= 0.5, 'colormap'] = 'g'
    df.loc[df3.probability < 0.5, 'colormap'] = 'y'
    df.loc[df3.probability < 0.2, 'colormap'] = 'r'

    df = df.iloc[:30].sort_values(by='counts', ascending=True)
    colormap = df3['colormap'].tolist()
    df3.plot.barh(x='songname', y='probability', color=colormap)
    usersongsfigname = str(username + '-' + artistname + '-predsongs.png')
    fig.savefig('static/img/'+ usersongsfigname)
    return usersongsfigname.show()

def main(setlistdf, usersongsdf, username, artistname):
    setsfigurename = setsongsfig(setlistdf, artistname)
    usersongsfigname = usersongsfig(setlistdf, usersongsdf, username, artistname)
    return setsfigurename, usersongsfigname
