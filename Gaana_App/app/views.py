from flask import render_template,jsonify
from sqlalchemy import and_
from flask import url_for, redirect, request, make_response,flash
# Importing Session Object to use Sessions
from flask import session
from app import search
from app import home
from app.models import User, Songs, Category, Subcategory, Favourite, Follower, Cat_subcat, Playlist, Playlist_song, Uploaded_songs
from app import app, db
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from mutagen.mp3 import MP3
import random
import math
import json
import hashlib
from flask import jsonify
from sqlalchemy import *
# from app import catsubcat
# import urllib.request



@app.route('/')
def index():
	global cslist
	with open('catsubcat.json') as data_file:
		data = json.loads(data_file.read())
		print(data['category'][0]['cat_id'])

	for d in data['category']:
			if db.session.query(Category).filter_by(cat_id=d['cat_id']).count() < 1:
				cat1 = Category(cat_id=d['cat_id'], cat_name=d['cat_name'],cat_thumbnail=d['cat_thumbnail'])
				db.session.add(cat1)
				db.session.commit()
	for d in data['Subcategory']:
			if db.session.query(Subcategory).filter_by(scat_id=d['scat_id']).count() < 1:
				cat1 = Subcategory(scat_id=d['scat_id'], scat_name=d['scat_name'])
				db.session.add(cat1)
			if db.session.query(Cat_subcat).filter(and_(Cat_subcat.cat_id==d['cat_id'],Cat_subcat.scat_id==d['scat_id'])).count() < 1:
				cs5 = Cat_subcat(cat_id=d['cat_id'], scat_id=d['scat_id'])
				db.session.add(cs5)
				db.session.commit()

	with open('songs.json') as data_file:
		data = json.loads(data_file.read())
	for d in data:
        	if db.session.query(Songs).filter_by(sid=d['sid']).count() < 1:
        		cat1 = Songs(sid=d['sid'], sname=d['sname'],artist=d['artist'],album=d['album'],category=d['category'],count=d['count'],path=d['path'],genre=d['genre'],year=d['year'])
        		db.session.add(cat1)
        		db.session.commit()
	
	return render_template('base.html')
@app.route('/index')
def index1():
	return render_template('index.html')
@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/registerNext', methods = ['GET','POST'])
def registerNext():
	user = User(uname=request.form["name"], email=request.form["emailid"], phone=request.form["phone"],  password=hashlib.sha224(request.form['loginpassword']).hexdigest())
	db.session.add(user)
	db.session.commit()
	flash('Your account has been created! You are now able to log in', 'success')
	session['userid'] = user.uid
	session['uname'] = user.uname
	# return "success post"
	songList=Songs.query.all()
	genreList=Subcategory.query.all()
	playlist=[]
	return render_template('Dashboard.html',listOfAllSongs=songList, genreList=genreList)



@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/loginNext',methods=['GET','POST'])
def loginNext():
	# To find out the method of request, use 'request.method'
	if 'userid' in session:
		songList=Songs.query.all()
		genreList=Subcategory.query.all()
		playlist=[]
		return render_template('Dashboard.html',listOfAllSongs=songList, genreList=genreList)
	if request.method == "GET":
		print "GET"
		userID = request.args.get("emailid")
		password = request.args.get("loginpassword")
		# Can perform some password validation here
		# return "Login Successful for: %s" % userID
	elif request.method == "POST":
		print "POST"
		userID = request.form['emailid']
		password = request.form['loginpassword']
		# return "success"
		# return render_template('Dashboard.html')

		# Can perform some password validation here!
	user  = User.query.filter(and_(User.email == userID, User.password == hashlib.sha224(password).hexdigest())).first()
	if user:
		flash('Login successful', 'success')
		session['userid'] = user.uid
		session['uname'] = user.uname
		# return "success post"
		songList=Songs.query.all()
		genreList=Subcategory.query.all()
		playlist=[]
		csong=Category.query.all()
		print "QWERTY()",session['userid']

		return render_template('Dashboard.html',listOfAllSongs=songList, genreList=genreList,cresult=csong)
			# return "Login Successful for: %s" % user.uname
	return redirect(url_for('home'))

@app.route('/loginBrowse',methods=['GET','POST'])
def loginBrowse():
	# To find out the method of request, use 'request.method'
	if 'userid' in session:
		songList=Songs.query.all()
		genreList=Subcategory.query.all()
		playlist=[]
		return render_template('Dashboard.html',listOfAllSongs=songList, genreList=genreList)
	if request.method == "GET":
		print(request.args)
		userID = request.args.get("emailid")
		password = request.args.get("loginpassword")
		# Can perform some password validation here
		# return "Login Successful for: %s" % userID
	elif request.method == "POST":
		userID = request.form['emailid']
		password = request.form['loginpassword']
		# return "success"
		# return render_template('Dashboard.html')

		# Can perform some password validation here!
	user  = User.query.filter(and_(User.email == userID, User.password == hashlib.sha224(password).hexdigest())).first()
	if user:
		flash('Login successful', 'success')
		session['userid'] = user.uid
		session['uname'] = user.uname
		# return "success post"
		songList=Songs.query.all()
		genreList=Subcategory.query.all()
		playlist=[]
		csong=Category.query.all()
		print csong
		return redirect(url_for('browse'))
		# return render_template('Dashboard.html',listOfAllSongs=songList, genreList=genreList,cresult=csong)
			# return "Login Successful for: %s" % user.uname
	return redirect(url_for('home'))

@app.route('/loginerror')
def loginerror():
	return render_template('loginerror.html')

@app.route('/addSong')
def addSong():
	return render_template('addSong.html')

@app.route('/downloadSong/<string:sid>')
def downloadSong(sid):
	s_id=int(sid)
	dsong=None
	flag=True
	up_songs=Uploaded_songs.query.all()
	for i in up_songs:
		if i.sid==s_id:
			if i.isPublic==True:
				flag=True
			else:
				flag=False
			break
	if flag==True:
		dsong=Songs.query.filter(Songs.sid==s_id).first()
		# dsong=Songs.query.filter(Songs.query.filter(Songs.sid==s_id)).first()
	# dsong  = Uploaded_songs.query.filter(and_(Uploaded_songs.sid == s_id, Uploaded_songs.isPublic==True)).first()
	if dsong is not None:
		# dpath=os.path.expanduser("~")+"/Downloads/"+dsong.sname
		return jsonify(dsong.path)
		# urllib.request.urlretrieve(dsong.path, dpath)
	return jsonify('None')	
        
	

@app.route('/background_process', methods=['GET','POST'])
def background_process():
	p=request.files['browse']
	p.save(os.path.join('./temp/', p.filename))
	audio=MP3("./temp/"+p.filename)
	length=audio.info.length
	gauth=GoogleAuth()
	gauth.LocalWebserverAuth()
	drive=GoogleDrive(gauth)
	#for uploading
	file1 = drive.CreateFile({'title':request.form["sname"]})
	file1.SetContentFile('./temp/'+p.filename)
	file1.Upload()
	os.remove('./temp/'+p.filename)
	permission = file1.InsertPermission({
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader',
                        'withLink': True})
	#for downloading
	link = file1['alternateLink']
	link=link.split('?')[0]
	link=link.split('/')[-2]
	link='https://docs.google.com/uc?export=download&id='+link
	print "this might cause error ",str(request.form.get('category'))
	print "request.form ", request.args.get('category')
	csong  = Category.query.filter(Category.cat_name==request.form.get('category')).first()
	csubsong  = Subcategory.query.filter(Subcategory.scat_name==request.form.get("genre")).first()
	
	song = Songs(sname=request.form['sname'], album=request.form["album"], artist=request.form["artist"], category=csong.cat_id  , genre=csubsong.scat_id, year=request.form["year"], path=link, duration=length)

	db.session.add(song)
	db.session.flush()
	#db.session.commit()
	db.session.commit()
	if 'userid' in session:
		temp=request.form["isPublic"]
		if temp=="Private":
			x=False
		else:
			x=True
		usong = Uploaded_songs(uid=session['userid'], sname=song.sname, sid=song.sid, path=song.path, isPublic=x)
		db.session.add(usong)
		db.session.commit()
		songList=Songs.query.all()
		genreList=Subcategory.query.all()
		playlist=[]
		csong=Category.query.all()
		print csong
		return render_template('Dashboard.html',listOfAllSongs=songList, genreList=genreList,cresult=csong)


@app.route('/setCookie',methods=['GET','POST'])
def setCookie():
	if request.method == "POST":
		userID = request.form['userid']
		# Create the Response Object
		resp = make_response(render_template('landing.html'))
		# Set the cookie value. Will use this name to refer to the cookies later
		resp.set_cookie('userID',userID)
		return resp

@app.route('/readCookie')
def readCookie():
	# Get all the cookies in request.cookies and then get the cookie named userID
	userID = request.cookies.get('userID')
	return '<h1>Hello '+ userID +' !!</h1>'

@app.route('/home')
def homePage():
	# Check if userID session exists!
	if 'userID' in session:
		return 'Logged in As: ' + session['userID'] + ' <br> Click <a href="/logout">here</a> to logout!'
	return "You are not logged in! <br>Click <a href = '/loginSession'></b>Here</b></a> to Login!"

@app.route('/loginSession',methods=['GET','POST'])
def loginSession():
	if request.method == "POST":
		# Create a session variable
		session['userID'] = request.form['userid']
		return redirect(url_for('homePage'))
	return '''
	<form action = "" method = "post">
      <p><input type = "text" name = "userid" /></p>
      <p><input type = "submit" value = "Login" /></p>
   </form>
	
   '''


@app.errorhandler(404)
def http_404_handler(error):
	return render_template('error404.html')


@app.route('/get_subcat/<cat>')
def get_subcat(cat):
	s = join(Category, Cat_subcat).join(Subcategory).select()
	rs=db.session.execute(s)
	clist={}
	catl=[]
	for row in rs:
		print "row: ",row
		if row[1] in clist:
			if row[6] not in clist.values():
				clist[str(row[1])].append(row[6])

			
		else:
			clist[str(row[1])]=[]
			clist[str(row[1])].append(row[6])
	for k in clist.keys():
		if str(cat) in k:
			catl=clist[k]
	
	return jsonify(catl)

@app.route('/discover')
def discover():
	result =Category.query.all() 
	print(result)
	return render_template('discover.html',result=result)

@app.route('/discoverplay/<int:cat_id>')
def discoverplay(cat_id):
	dsongs =Songs.query.filter(Songs.category==cat_id).all()
	csong=Category.query.filter(Category.cat_id==cat_id).first()
	scmap=Cat_subcat.query.filter(Cat_subcat.cat_id==cat_id).all()

	s = join(Category, Cat_subcat).join(Subcategory).select()
	rs=db.session.execute(s)
	clist={}
	for row in rs:
		print row
		if row[1] in clist:
			if row[6] not in clist.values():
				clist[str(row[1])].append(row[6])
		else:
			clist[str(row[1])]=[]
			clist[str(row[1])].append(row[6])
	w=join(Songs,Subcategory).select()
	rs=db.session.execute(w)
	songpath={}
	songname={}
	songgenre={}
	for row in rs:
		if row.scat_name in clist[csong.cat_name]:
			if row.scat_name not in songpath:
				songpath[str(row.scat_name)]=[]
				songgenre[str(row.scat_name)]=""
				songpath[str(row.scat_name)].append(str(row.path))
				songgenre[str(row.scat_name)]+=(str(row.sid))+","
			else:
				songpath[str(row.scat_name)].append(str(row.path))
				songgenre[str(row.scat_name)]+=(str(row.sid))+","

		if row.path not in songname:
				songname[str(row.path)]=""
				songname[str(row.path)]=(row)
		else:
				songname[str(row.path)]=(row)
	# print "songname",songname
	# print "ji",songpath
	return render_template('discoverbycat.html',result1= clist[csong.cat_name],result2=songname,result3=songpath,result4=songgenre)

@app.route('/discover_genre/<int:g_id>',methods=['GET','POST'])
def discover_genre(g_id):
	list_songs=Songs.query.filter(Songs.genre==g_id).all()
	string=''
	for i in list_songs:
		string+=str(i.sid)+','
	return render_template('songsall.html',var1=list_songs,var2=string)


@app.route('/createPlaylist',methods=['POST'])
def createPlaylist():
	if request.method=="POST":
		if 'userid' in session:
			u_id=session['userid']
			p_name=request.form["pname"]
			pres = Playlist.query.filter(Playlist.uid==u_id,Playlist.pname==p_name)
			if pres.first()!=None:
				return "Playlist already extists"
			play_list=Playlist(pname=str(p_name), uid=str(u_id))
			db.session.add(play_list)
			# db.session.commit()
			pq = Playlist.query.all()[-1]
			pname=pq.pname
			pid=pq.pid

			#fetching selected songs id
			plist = request.form["list"].split(",")
			for songid in plist:
				psong = Playlist_song(pid=str(pid),sid = str(songid) )
				db.session.add(psong)
				db.session.commit()
			return redirect(url_for('browse'))
	return render_template('404page.html')

@app.route('/createPlaylistDashboard',methods=['POST'])
def createPlaylistDashboard():
	if request.method=="POST":
		if 'userid' in session:
			u_id=session['userid']
			p_name=request.form["pname"]
			pres = Playlist.query.filter(Playlist.uid==u_id,Playlist.pname==p_name)
			if pres.first()!=None:
				return "Playlist already extists"
			play_list=Playlist(pname=str(p_name), uid=str(u_id))
			db.session.add(play_list)
			# db.session.commit()
			pq = Playlist.query.all()[-1]
			pname=pq.pname
			pid=pq.pid

			#fetching selected songs id
			plist = request.form["list"].split(",")
			for songid in plist:
				psong = Playlist_song(pid=str(pid),sid = str(songid) )
				db.session.add(psong)
				db.session.commit()
			return redirect(url_for('loginNext'))
	return render_template('404page.html')

@app.route('/logout')
def logout():
	# Remove the session variable if present
	session.pop('userid',None)
	session.pop('uname',None)
	return redirect(url_for('home'))


@app.route('/viewPlaylist')
def viewPlaylist():
	playlist_songs=[]
	links=[]
	l=[]
	result=db.engine.execute("select pid, pname from playlist where uid="+str(session['userid'])+";")
	for i in result:
		print i.pname
		playlist_songs.append([i.pname])
		songs=db.engine.execute("select sid from playlist_song where pid="+str(i.pid))
		for s in songs:
			sname=db.engine.execute("select sname,path,thumbnail,duration from songs where sid="+str(s.sid)).first()
			playlist_songs.append([sname.sname,sname.thumbnail,sname.path,sname.duration,i.pid])
			print sname.sname
		l.append(playlist_songs)
		playlist_songs=[]
	return jsonify(l)

@app.route('/browse')
def browse():
	song_list=[]
	song_list=Songs.query.all()
	return render_template('browse.html',songs=song_list)

@app.route('/addToFav/<int:sid>/<int:uid>',methods=['GET','POST'])
def addToFav(sid,uid):
	fav = Favourite(sid=sid, uid=uid)
	db.session.add(fav)
	db.session.commit()
	print "deleted from fav successfully"
	return "success"

@app.route('/removeFromFav/<int:sid>/<int:uid>',methods=['GET','POST'])
def removeFromFav(sid,uid):
	db.engine.execute("delete from favourite where sid="+str(sid)+" and uid="+str(uid))
	db.session.commit()
	print "deleted from fav successfully"

@app.route('/addToExistingPlaylist/<string:pname>/<string:sid>/<string:uid>', methods=['GET','POST'])
def addToExistingPlaylist(pname, sid, uid):
	fetch_pid =Playlist.query.filter(and_(Playlist.uid == uid, Playlist.pname == pname)).first()
	if fetch_pid!=None:
		print fetch_pid.pid
		psong = Playlist_song(pid=fetch_pid.pid, sid=sid)
		db.session.add(psong)
		db.session.commit()
		print "success"
	else:
		print "Error in adding to playlist"
	return "hey"

@app.route('/viewFavs',methods=['GET','POST'])
def viewFavs():
	if 'userid' in session:
		sid_list = db.engine.execute("select sid from favourite where uid="+str(session['userid']))
		l=[]
		for id in sid_list:
			sinfo = db.engine.execute("select sid,sname, path from songs where sid="+str(id.sid)).first()
			l.append([sinfo.sid,sinfo.sname, sinfo.path])
			print sinfo.sname
		return jsonify(l)
	else:
		return "Please Login"


@app.route('/deletePlaylist/<string:uid>/<string:pname>',methods=['GET','POST'])
def deletePlaylist(uid,pname):
	if 'userid' in session:
		pid = db.engine.execute("select pid from playlist where uid="+uid+" and pname='"+pname+"'").first()
		db.engine.execute("delete from playlist_song where pid="+str(pid.pid))
		db.session.commit()
		status=db.engine.execute("delete from playlist where pid="+str(pid.pid))
		db.session.commit()
		if status is None:
			return "Error"
		else:
			return "success"

@app.route('/radio')
def radio():
	song=Songs.query.all()
	cat=Category.query.all()

	d=[]
	for s in song:
		for c in cat:
			if s.category == c.cat_id:
				if c not in d:
					d.append(c)
				
	for k in d:
		print k
		print "\n"

	return render_template("radio.html", dict=d)

@app.route('/get_song_list/<string:cat_id>')
def get_song_list(cat_id):
	id=int(cat_id)
	song=Songs.query.all()
	cat=Category.query.all()
	l=[]
	s1=""
	for s in song:
		for c in cat:
			if s.category == id:
				if s.sid not in l:
					l.append(s.sid)
					s1+=str(s.sid)+","
				
				
				
	print(s1)
	return jsonify(s1)

@app.route('/cat_fetch')
def cat_fetch():
	list_cat=Category.query.all()
	playlist_songs=[]
	l=[]
	for i in list_cat:
		playlist_songs.append(str(i.cat_id))
		playlist_songs.append(str(i.cat_name))
		l.append(playlist_songs)
		playlist_songs=[]
	print l
	return jsonify(l)

@app.route('/getSids/<string:pid>')
def getSid(pid):
	print "pid is ",pid
	data=db.engine.execute("select sid from playlist_song where pid="+pid)
	id_list=[]
	for items in data:
		data1 = db.engine.execute("select sname,path,thumbnail,duration from songs where sid="+str(items.sid)).first()
		id_list.append([data1.sname,data1.thumbnail,data1.path,data1.duration])
	print id_list
	return jsonify(id_list)

@app.route('/songInfoFromSid/<string:sid>')
def songInfoFromSid(sid):
	l=[]
	data=db.engine.execute("select sname,path,thumbnail,duration from songs where sid="+str(sid)).first()
	l.append(data.sname)
	l.append(data.thumbnail)
	l.append(data.path)
	l.append(data.duration)
	return jsonify(l)

@app.route('/viewFollowing/<string:uid>')
def viewFollowing(uid):
	l=[]
	data=db.engine.execute("select uid from follower where follower_id="+uid)
	for item in data:
		data1 = db.engine.execute("select uid,uname from user where uid="+str(item.uid)).first()
		l.append([data1.uid,data1.uname])
	return jsonify(l)

@app.route('/viewFollowers/<string:uid>')
def viewFollowers(uid):
	l=[]
	data=db.engine.execute("select follower_id from follower where uid="+uid)
	for item in data:
		data1 = db.engine.execute("select uid,uname from user where uid="+str(item.follower_id)).first()
		l.append([data1.uid,data1.uname])
	return jsonify(l)

@app.route('/viewUploadedSong/<string:uid>')
def viewUploadedSong(uid):
	l=[]
	data=db.engine.execute("select * from uploaded_songs where uid="+uid)
	for item in data:
		l.append([item.sid,item.sname,item.path])
	return jsonify(l)