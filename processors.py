#!/usr/bin/env python
import os
#import subprocess
#import shlex
from gi.repository import GExiv2
from mutagenx.easyid3 import EasyID3
from datetime import date, datetime


def process_default(f):
    return os.path.splitext(f)[1][1:],os.path.splitext(os.path.split(f)[1])[0]

def process_jpg(f):
    p = GExiv2.Metadata(f)
    try: 
        exivDate = datetime.strptime(p['Exif.Photo.DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        folder = 'jpg/'+exivDate.strftime('%Y')+'/'+exivDate.strftime('%m')
        name = exivDate.strftime('%Y')+exivDate.strftime('%m')+exivDate.strftime('%d')\
            + "_" + exivDate.strftime('%H') + exivDate.strftime('%M') + exivDate.strftime('%S')
        return folder,name
    except:
        return process_default(f)

def process_mp3(f):
    try:
        tag = EasyID3(f)
    except:
        return 'mp3/','unknow'
    try:
        artist = tag['artist']
    except: 
        artist = 'unknow'
    try:
        title = tag['title'] 
    except:
        title = 'unknow'
    try:
        album = tag['album']
    except:
        album = False
    try:
        track = tag['tracknumber']
    except:
        track =  False

    
    folder = 'mp3/'+''.join(artist)
    if album:
        folder += '/'+''.join(album)
    if track:
        name = ''.join(track) + ' - ' + ''.join(title)
    else:
        name = ''.join(title)
    return folder.replace('/','.'),name.replace('/','.')
