from app import app, db
from flask import render_template,session
from sqlalchemy import and_
from app import home
from flask import url_for, redirect, request, make_response,flash
from app.models import User, Songs, Category, Subcategory, Favourite, Follower, Cat_subcat, Playlist, Playlist_song, Uploaded_songs
import unicodedata
from flask import jsonify

@app.route('/search',methods=['POST'])
def search():
	search=request.form["searchInput"]
	search='%'+search+'%'
	list_songs=Songs.query.filter(Songs.sname.like(search)).all()
	string=''
	for i in list_songs:
		string+=str(i.sid)+','
	result=Songs.query.with_entities(Songs.artist).filter(Songs.artist.like(search)).distinct(Songs.artist).all()
	list_artist=[]
	for i in result:
		tmp=str(i).split("'")
		list_artist.append(tmp[1])
	result=Songs.query.with_entities(Songs.album).filter(Songs.album.like(search)).distinct(Songs.album).all()
	list_album=[]
	for i in result:
		tmp=str(i).split("'")
		list_album.append(tmp[1])
	list_usr=User.query.filter(User.uname.like(search)).all()
	return render_template('search.html',search_var=search,var1=list_songs,var2=list_artist,var3=list_album,var4=list_usr,songs_sid=string)


@app.route('/songsall/<string:searched>',methods=['GET','POST'])
def songsall(searched):	
	list_songs=Songs.query.filter(Songs.sname.like(searched)).all()
	string=''
	for i in list_songs:
		string+=str(i.sid)+','
	return render_template('songsall.html',var1=list_songs,var2=string)

@app.route('/artistAll/<string:searched>',methods=['GET','POST'])
def artistAll(searched):
	search=searched
	result=Songs.query.with_entities(Songs.artist).filter(Songs.artist.like(search)).distinct(Songs.artist).all()
	list_artist=[]
	for i in result:
		tmp=str(i).split("'")
		list_artist.append(tmp[1])
	return render_template('artistAll.html',var1=list_artist)

@app.route('/songArtist/<string:searched>',methods=['GET','POST'])
def songArtist(searched):
	search=searched
	list_songs=Songs.query.filter(Songs.artist.like(search)).all()
	string=''
	for i in list_songs:
		string+=str(i.sid)+','
	return render_template('songsall.html',var1=list_songs,var2=string)

@app.route('/albumAll/<string:searched>',methods=['GET','POST'])
def albumAll(searched):
	search=searched
	result=Songs.query.with_entities(Songs.album).filter(Songs.album.like(search)).distinct(Songs.album).all()
	list_album=[]
	for i in result:
		tmp=str(i).split("'")
		list_album.append(tmp[1])
	return render_template('albumAll.html',var1=list_album)

@app.route('/songAlbum/<string:searched>',methods=['GET','POST'])
def songAlbum(searched):
	search=searched
	list_songs=Songs.query.filter(Songs.album.like(search)).all()
	string=''
	for i in list_songs:
		string+=str(i.sid)+','
	return render_template('songsall.html',var1=list_songs,var2=string)

@app.route('/userAll/<string:searched>',methods=['GET','POST'])
def userAll(searched):
	search=searched
	# print "hello"
	list_usr=User.query.filter(User.uname.like(search)).all()
	return render_template('userAll.html',var1=list_usr)


@app.route('/userProfile/<string:searched>',methods=['GET','POST'])
def userProfile(searched):
	search=searched
	p=str(search).split(">")
	x=p[0].split(" ")
	list_details=User.query.filter_by(uid=x[1]).all()
	user_details=[{'uid':list_details[0].uid,'uname': str(list_details[0].uname).split("'")[0],  'email': str(list_details[0].email).split("'")[0] }]
	list_temp=Follower.query.filter(and_(Follower.uid==list_details[0].uid, Follower.follower_id==session['userid'])).all()

	if(len(list_temp)==0):
		result="true" #this pair is already in the database
	else:
		result="false" #this pair is not in database

	return render_template('profile.html',var1=user_details, status=result)

#added by priya

#added by priya
@app.route('/userProfileById2/<string:searched>',methods=['GET','POST'])
def userProfileById2(searched):
	search=searched
	print search
	list_details=User.query.filter_by(uid=search).all()
	user_details=[{'uid':list_details[0].uid,'uname': str(list_details[0].uname).split("'")[0],  'email': str(list_details[0].email).split("'")[0] }]
	list_temp=Follower.query.filter(and_(Follower.uid==list_details[0].uid, Follower.follower_id==session['userid'])).all()

	if(len(list_temp)==0):
		result="true" #this pair is already in the database
	else:
		result="false" #this pair is not in database

	return render_template('profile2.html',var1=user_details, status=result)

@app.route('/userProfileById/<string:searched>',methods=['GET','POST'])
def userProfileById(searched):
	list_details=User.query.filter_by(uid=searched).all()
	user_details=[{'uid':list_details[0].uid,'uname': str(list_details[0].uname).split("'")[0],  'email': str(list_details[0].email).split("'")[0] }]
	list_temp=Follower.query.filter(and_(Follower.uid==list_details[0].uid, Follower.follower_id==session['userid'])).all()
	
	p=Playlist.query.all()
	
	play_songs=[]
	ps=Playlist_song.query.all()
	
	s=Songs.query.all()

	t=[]
	for i in p:
		
		for j in ps:
			if(i.pid==j.pid):
				
				if(int(i.uid)==list_details[0].uid):
					
					t.append(j)
	for i in t:
		for k in s:
			if ( i.sid == k.sid):
				
				if k not in play_songs:
					play_songs.append(k)
	
	if(len(list_temp)==0):
		result="true" #this pair is already in the database
	else:
		result="false" #this pair is not in database

	return render_template('showFollowerPlaylist.html',var1=user_details, status=result,playlist=play_songs)

@app.route('/follow/<int:uid>',methods=['GET','POST'])
def follow(uid):
	userid=uid
	print userid
	db.engine.execute("insert into follower (uid,follower_id) values("+str(userid)+","+str(session['userid'])+")")
	db.session.commit()
	return str(userid)


@app.route('/unfollow/<int:uid>',methods=['GET','POST'])
def unfollow(uid):
	userid=uid
	print userid
	db.engine.execute("delete from follower where uid="+str(userid)+" and follower_id="+str(session['userid']))
	db.session.commit()
	return str(userid)

@app.route('/songsjson/<string:searched>',methods=['GET','POST'])
def songsjson(searched):
	
	s_array=searched.split(',')
	playlist_songs=[]
	links=[]
	l=[]
	s_array.pop()
	for i in s_array:
		
		q=Songs.query.filter(Songs.sid==int(i)).first()
		playlist_songs.append(str(q.sname))
		playlist_songs.append(str(q.thumbnail))
		playlist_songs.append(str(q.path))
		playlist_songs.append(str(q.duration))
		l.append(playlist_songs)
		playlist_songs=[]
	
	return jsonify(l)