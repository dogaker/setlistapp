import matplotlib.pyplot as plt
import pandas as pd


def setsongsfig(setlistdf, artistname):
    plt.style.use('bmh')
    fig = plt.figure
#    print setlistdf
    setlistdf = setlistdf.sort_values(by='probability', ascending=False)

    setlistdf.loc[setlistdf.probability >= 0.5, 'colormap'] = 'g'
    setlistdf.loc[setlistdf.probability < 0.5, 'colormap'] = 'y'
    setlistdf.loc[setlistdf.probability < 0.2, 'colormap'] = 'r'
    setlistdf = setlistdf.iloc[:15].sort_values(by='probability', ascending=True)
    colormap = setlistdf['colormap'].tolist()
    setlistdf.plot.barh(x='songname', y='probability', color=colormap, align='center', legend=False, title='Songs You Will Hear')
    ax = plt.gca()
    ax.tick_params(colors='white')
    ax.set_title(ax.get_title(), fontsize=26, color='white')
    ax.set_ylabel('')
    ax.set_xlim([0,1])
    labels = ['unlikely', '', '', '', '', 'very likely']
    ax.set_xticklabels(labels)
    setsfigurename = str(artistname + '-predsongs.png')

    plt.savefig('/Users/doa/Documents/git/insight/project/setlistapp/static/' + setsfigurename, transparent=True, bbox_inches='tight')
    return setsfigurename


def usersongsfig(setlistdf, usersongsdf, username, artistname):
    plt.style.use('bmh')
    fig = plt.figure
    mergeddf = usersongsdf.merge(
        setlistdf, left_on='shorttrackname', right_on='shorttrackname_x')
    mergeddf.loc[mergeddf.probability >= 0.5, 'colormap'] = 'g'
    mergeddf.loc[mergeddf.probability < 0.5, 'colormap'] = 'y'
    mergeddf.loc[mergeddf.probability < 0.2, 'colormap'] = 'r'
    mergeddf = mergeddf.iloc[:15].sort_values(by='counts', ascending=True)
    colormap = mergeddf['colormap'].tolist()
    mergeddf.plot.barh(x='songname', y='probability', color=colormap, align='center', legend=False, title="Your Top Songs' Chances")
    ax = plt.gca()
    ax.tick_params(colors='white')
    ax.set_title(ax.get_title(), fontsize=26, color='white')
    ax.set_ylabel('')
    ax.set_xlim([0,1])
    labels = ['unlikely', '', '', '', '', 'very likely']
    ax.set_xticklabels(labels)
    usersongsfigname = str(username + '-' + artistname + '-predsongs.png')
    plt.savefig('/Users/doa/Documents/git/insight/project/setlistapp/static/' + usersongsfigname, transparent=True, bbox_inches='tight')
    return usersongsfigname


def main(setlistdf, usersongsdf, username, artistname):
    setsfigurename = setsongsfig(setlistdf, artistname)
    usersongsfigname = usersongsfig(
        setlistdf, usersongsdf, username, artistname)
    return setsfigurename, usersongsfigname
