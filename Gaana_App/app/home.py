from app import app, db
from flask import render_template
from sqlalchemy import and_
from flask import url_for, redirect, request, make_response,flash
from app.models import User, Songs, Category, Subcategory, Favourite, Follower, Cat_subcat, Playlist, Playlist_song, Uploaded_songs
import unicodedata
recently_played=[]

@app.route('/recent/<int:song_id>',methods=['GET','POST'])
def add_to_recent(song_id):
    temp=Songs.query.filter(Songs.sid==song_id).first()
    temp.count=temp.count+1
    db.session.commit()
    if song_id in recently_played:
        recently_played.remove(song_id)
    recently_played.insert(0,song_id)
    # print recently_played

    return 'None'

@app.route('/home')
def home():
    list_songs=[]
    for i in recently_played:
    	temp=Songs.query.filter(Songs.sid==i).first()
        list_songs.append(temp)
    list_trend=Songs.query.order_by(Songs.count.desc()).all()
    string_recent=''
    for i in list_songs:
        string_recent+=str(i.sid)+','
    string_trend=''
    for i in list_trend:
        string_trend+=str(i.sid)+','
    result=Songs.query.with_entities(Songs.artist).distinct(Songs.artist).all()
    list_artist=[]
    for i in result:
        tmp=str(i).split("'")
        list_artist.append(tmp[1])
    return render_template('home.html',var1=list_songs,var2=list_trend,var3=list_artist,song_recent=string_recent,song_trend=string_trend)

@app.route('/recent',methods=['GET','POST'])
def recent():
    list_songs=[]
    for i in recently_played:
        temp=Songs.query.filter(Songs.sid==i).first()
        list_songs.append(temp)
    string=''
    for i in list_songs:
		string+=str(i.sid)+','
    return render_template('songsall.html',var1=list_songs,var2=string)

@app.route('/trend',methods=['GET','POST'])
def trend():
    list_songs=Songs.query.order_by(Songs.count.desc()).all()
    string=''
    for i in list_songs:
		string+=str(i.sid)+','
    return render_template('songsall.html',var1=list_songs,var2=string)
@app.route('/artistAllHome',methods=['GET','POST'])
def artistAllHome():
    result=Songs.query.with_entities(Songs.artist).distinct(Songs.artist).all()
    list_artist=[]
    for i in result:
        tmp=str(i).split("'")
        list_artist.append(tmp[1])
    return render_template('artistAll.html',var1=list_artist)
