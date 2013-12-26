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
    if p:
        exivDate = datetime.strptime(p['Exif.Photo.DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        folder = 'jpg/'+exivDate.strftime('%Y')+'/'+exivDate.strftime('%m')
        name = exivDate.strftime('%Y')+exivDate.strftime('%m')+exivDate.strftime('%d')\
            + "_" + exivDate.strftime('%H') + exivDate.strftime('%M') + exivDate.strftime('%S')
        return folder,name
    else:
        return process_default(f)

def process_mp3(f):
    tag = EasyID3(f)
    artist = tag['artist'] if tag['artist'] != '' else 'unknow'
    title = tag['title'] if tag['title'] else 'unknow'
    album = tag['album']
    track = tag['tracknumber']
    
    folder = 'mp3/'+''.join(artist)
    if album:
        folder += '/'+''.join(album)
    if track:
        name = ''.join(track) + ' - '
    name += ''.join(title)
    return folder,name
