#!/usr/bin/env python
import os
# import subprocess
# import shlex
from exifpy import exifread
from mutagenx.easyid3 import EasyID3
from datetime import datetime
import logging


extension_to_function = {
    'jpg': process_image,
    'mp3': process_music,
}


def process(file, extension):
    try:
        return extension_to_function[extension](file)
    except IndexError:
        return process_default(file)


def process_default(f):
    return os.path.splitext(f)[1][1:], os.path.splitext(os.path.split(f)[1])[0]


def process_image(f):
    try:
        b = open(f, 'rb')
        p = exifread.process_file(b, stop_tag='EXIF DateTimeOriginal', details=False)
        exivDate = datetime.strptime(p['EXIF DateTimeOriginal'].printable,
                                     '%Y:%m:%d %H:%M:%S')
        folder = 'jpg/'+exivDate.strftime('%Y')+'/'+exivDate.strftime('%m')
        name = exivDate.strftime('%Y')+exivDate.strftime('%m')+exivDate.strftime('%d')\
            + "_" + exivDate.strftime('%H') + exivDate.strftime('%M')\
            + exivDate.strftime('%S')
        return folder, name
    except:
        b = os.stat(f)
        if b.st_size < 256000:
            logging.info("%s is too small" % (f))
            return False, False
        return process_default(f)


def process_music(f):
    try:
        tag = EasyID3(f)
    except:
        return 'mp3/', 'unknow'
    try:
        artist = ''.join(tag['artist'])
    except:
        artist = 'unknow'
    try:
        title = ''.join(tag['title'])
    except:
        title = 'unknow'
    try:
        album = ''.join(tag['album'])
    except:
        album = False
    try:
        track = ''.join(tag['tracknumber'])
    except:
        track = False

    folder = 'mp3/'+artist.replace('/', '.')
    if album:
        folder += '/'+album.replace('/', '.')
    if track:
        name = track.replace('/', '.') + ' - ' + title.replace('/', '.')

    else:
        name = title.replace('/', '.')
    print(folder, name)
    return folder, name
