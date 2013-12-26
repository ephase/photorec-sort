#!/usr/bin/env python
import os
import os.path
import shutil
import sys
import argparse
import re
import processors

parser = argparse.ArgumentParser(description='Sort Photorec results by file type')
parser.add_argument ('--source', help='directory containing photorec recup_xx dirs', default='./', metavar='DIR')
parser.add_argument ('--dest', help='directory where put sorted files', metavar='DIR', required=True)
parser.add_argument ('--move', help='do not copy files, move it', dest='move', action='store_true') 
parser.add_argument ('--filetypes', help='text file containing file type for grouping *NOT IMPLEMENTED*', metavar='FILE')
parser.add_argument ('--verbose', '-v', dest='verbose', action='store_true', help='verbose output')
args = parser.parse_args();

#Future : implement right verification
if not os.path.isdir(args.source):
    print ('source does not exist or not a directory, exiting')
    sys.exit()

if not os.path.exists(args.dest):
    print ('Destination directory does no exist')
    sys.exit()

numbers_of_directory = 0
for directory in os.listdir(args.source):
    numbers_of_files = 0
    is_pr_directory = re.search ('^recup_dir.[0-9]*', directory)
    if is_pr_directory:
        numbers_of_directory+=1
        for root, dirs, files, in os.walk(args.source+'/'+directory):
            for file in files:
                numbers_of_files+=1
                extension = os.path.splitext(file)[1][1:]
                try:
                    path, filename = getattr(processors, 'process_'+extension)(os.path.join(args.source,directory,file))
                except AttributeError:
                    path, filename = processors.process_default(file)
                destination = os.path.join(args.dest,directory,filename)
                if not os.path.exists(destination):
                   os.mkdir(destination)
                if os.path.exists(os.path.join(destination,file)):
                    print ('WARNING: this file was not copied :', os.path.join(args.source, directory ,file))
                else:
                    if args.move:
                        print ('Moving ', file,' from ', os.path.join(args.source, directory) ,' to ', destination)
                        shutil.move(os.path.join(args.source, directory, file), destination)
                    else:
                        if args.verbose : print ('Copying ', file,' from ', os.path.join(args.source, directory ,file), ' to ', destination)
                        shutil.copy2(os.path.join(args.source, directory, file), destination)
        if args.verbose:
            print ('valid directory found : ', directory,' with : ', numbers_of_files)
print ('Directory processed : ',numbers_of_directory)
