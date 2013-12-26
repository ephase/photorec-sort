#!/usr/bin/env python
import os
#import subprocess
#import shlex
from gi.repository import GExiv2
from mutagenx.easyid3 import EasyID3
from datetime import date, datetime


def process_default(f):
    #print ('processing default file')
    return os.path.splitext(f)[1][1:],f

def process_jpg(f):
    p = GExiv2.Metadata(f)
    exivDate = datetime.strptime(p['Exif.Photo.DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
    folder = exivDate.strftime('%Y')+'/'+exivDate.strftime('%m')
    name = exivDate.strftime('%Y')+exivDate.strftime('%m')+exivDate.strftime('%d')\
        + "_" + exivDate.strftime('%H') + exivDate.strftime('%M') + exivDate.strftime('%S')
    print (folder.lstrip(),name.lstrip())
    return folder,name

def process_mp3(f):
    tag = EasyID3(f)
    artist = tag['artist'] if tag['artist'] != '' else 'unknow'
    title = tag['title'] if tag['title'] else 'unknow'
    album = tag['album']
    track = tag['tracknumber']
    
    folder = ''.join(artist)
    if album:
        folder += '/'+''.join(album)
    if track:
        name = ''.join(track) + ' - '
    name += ''.join(title)
    print (name)
    return folder,name
