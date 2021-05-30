from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import urllib
# import wget

def getLink(path):
    gauth=GoogleAuth()
    gauth.LocalWebserverAuth()
    drive=GoogleDrive(gauth)
#for uploading
    file1 = drive.CreateFile({'title':'test_song'})
    file.SetContentFile(path)
    # file1.SetContentFile('/home/priya/Sem1/Scripting and Environments/Project/ColdplayParadise.mp3')
    file1.Upload()
    permission = file1.InsertPermission({
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader'
                        'withLink': True})
# url=file1['alternateLink']

#for downloading
    url = file1['alternateLink']
# link='https://drive.google.com/file/d/10rfBh2XQaiTBKwjM_84xMLQaBkY99o8v/view?usp=sharing'
    link=link.split('?')[0]
    link=link.split('/')[-2]
    link='https://docs.google.com/uc?export=download&id='+link

# urllib.urlretrieve(link,'mp13.mp3')



