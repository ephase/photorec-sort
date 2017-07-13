#!/usr/bin/env python
import os
import os.path
import shutil
import sys
import argparse
import re
import logging
import processors


def setup_cli():
    parser = argparse.ArgumentParser(description='Sort Photorec results by file type')
    parser.add_argument('--source',
                        help='directory containing photorec recup_xx dirs',
                        default='./',
                        metavar='DIR')

    parser.add_argument('--dest',
                        help='directory where put sorted files',
                        metavar='DIR',
                        required=True)

    parser.add_argument('--move',
                        help='do not copy files, move it',
                        dest='move', action='store_true')

    parser.add_argument('--filetypes',
                        help='text file containing file type for grouping *NOT IMPLEMENTED*',
                        metavar='FILE')

    parser.add_argument('--verbose',
                        '-v',
                        dest='verbose',
                        action='store_true',
                        help='verbose output')

    return parser


def parse_args():
    parser = setup_cli()

    # Future : implement right verification
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        logging.error('source does not exist or not a directory, exiting')
        sys.exit()

    if not os.path.exists(args.dest):
        logging.error('Destination directory does no exist')
        sys.exit()

    return args


def handle_file(file, args):
    extension = os.path.splitext(file)[1][1:].lower()

    path, filename = processors.proces(os.path.join(args.source, directory, file),
                                       extension)

    if filename:
        destination_dir = os.path.join(args.dest, path)
        os.makedirs(destination_dir, exist_ok=True)

        destination_file = os.path.join(destination_dir,
                                        filename + '.' + extension)

        increment = 0
        while os.path.exists(destination_file):
            increment += 1
            destination_file = os.path.join(destination_dir,
                                            filename +
                                            '_' + str(increment) +
                                            '.' + extension)
        if args.move:
            logging.info('Moving %s to %s' % (file, destination_file))
            shutil.move(os.path.join(args.source, directory, file),
                        destination_file)
        else:
            logging.info('Moving %s to %s' % (file, destination_file))
            shutil.copy2(os.path.join(args.source, directory, file),
                         destination_file)


def directories():
    for directory in os.listdir(args.source):
        is_pr_directory = re.search('^recup_dir.[0-9]*', directory)
        if is_pr_directory:
            yield os.path.join(args.source, directory)


def files():
    for directory in directories():
        for _, _, files, in os.walk(directory):
            for file in files:
                yield file


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    args = parse_args()

    for file in files():
        handle_file(file, args)

# logging.info('valid directory %s with %s: ' % (directory, numbers_of_files))
# logging.info('Directory processed %s ' % (numbers_of_directory))
