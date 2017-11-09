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

    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        help='verbose output')

    parser.add_argument('-k', '--only-known-filetype',
                        help='Process only known filetype',
                        dest='only_known_fyletype',
                        action='store_true')

    parser.add_argument('-d', '--dry-run',
                        help='',
                        dest='dry_run',
                        action='store_true')

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
    if args.dry_run:
        logging.info("DRY RUN : no change will be made")

    return args


def handle_file(file, directory,  args):
    extension = os.path.splitext(file)[1][1:].lower()

    path, filename = processors.process(os.path.join(directory, file),
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
            logging.info('Dry_run : moving %s to %s', file, destination_file)
            return

        if args.move:
            logging.info('Moving %s to %s', file, destination_file)
            if not args.dry_run:
                shutil.move(os.path.join(directory, file),
                            destination_file)
        else:
            logging.info('Copying %s to %s', file, destination_file)
            if not args.dry_run:
                shutil.copy2(os.path.join(directory, file),
                             destination_file)


def directories():
    for directory in os.listdir(args.source):
        logging.debug("Found a directory : %s", directory)
        yield os.path.join(args.source, directory)


def files():
    for directory in directories():
        for _, _, files, in os.walk(directory):
            for file in files:
                yield directory, file


if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        level=logging.DEBUG
    )
    logging.info("Starting photorec sort")
    args = parse_args()

    for dir, file in files():
        logging.debug("Process file : %s in %s", file, dir)
        handle_file(file, dir, args)

# logging.info('valid directory %s with %s: ' % (directory, numbers_of_files))
# logging.info('Directory processed %s ' % (numbers_of_directory))
