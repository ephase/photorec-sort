#!/usr/bin/env python
import os
# import subprocess
# import shlex
from exifpy import exifread
from datetime import datetime
import logging


def process(file, extension):
    try:
        return extension_to_function[extension](file)
    except KeyError:
        return process_default(file)


def process_default(f):
    return os.path.splitext(f)[1][1:], os.path.splitext(os.path.split(f)[1])[0]


def process_image(f):
    try:
        b = open(f, 'rb')
        p = exifread.process_file(b, stop_tag='EXIF DateTimeOriginal', details=False)
        exiv_date = datetime.strptime(
            p['EXIF DateTimeOriginal'].printable,
            '%Y:%m:%d %H:%M:%S'
        )
        folder = 'photo/' + exiv_date.strftime('%Y')\
            + '/' + exiv_date.strftime('%m')
        name = exiv_date.strftime('%Y') + "-"\
            + exiv_date.strftime('%m') + "-"\
            + exiv_date.strftime('%d') + "_"\
            + exiv_date.strftime('%H') + exiv_date.strftime('%M')\
            + exiv_date.strftime('%S')
        return folder, name
    except:
        b = os.stat(f)
        if b.st_size < 128000:
            logging.info("%s is too small" % (f))
            return False, False
        return process_default(f)


def get_m_tag(f, t):
    try:
        return ''.join(f[t])
    except:
        return ''


def process_music(f):
    import mutagen
    folder = "music/"
    b = os.stat(f)
    try:
        tag = mutagen.File(f, easy=True)
    except:
        logging.error("%s cannot be opened by mutagen", f)
        os.system("pause") 
        return False, False

    artist = get_m_tag(tag, 'artist')
    title = get_m_tag(tag, 'title')
    album = get_m_tag(tag, 'album')
    track = get_m_tag(tag, 'tracknumber')

    if not artist and not title:
        if b.st_size < 256000:
            logging.info("%s is too small", f)
            return False, False
        else:
            return process_default(f)

    if artist:
        folder += artist.replace('/', '.')
    if album:
        folder += '/' + album.replace('/', '.')
    if track:
        name = track.replace('/', '.') + ' - ' + title.replace('/', '.')
    else:
        name = title.replace('/', '.')
    return folder, name


extension_to_function = {
    'jpg': process_image,
    'mp3': process_music,
    'aac': process_music,
    'ogg': process_music,
    'flac': process_music,
    'm4p': process_music
}
