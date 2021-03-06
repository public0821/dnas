#!/usr/bin/python3

import atexit
import os
import sys
import traceback
import logging
import readline
import argparse
import gettext
import time

FILENAME = os.path.basename(os.path.realpath(__file__))
PROGNAME = FILENAME.split('.')[0]
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.extend([CURRENT_DIR])
gettext.install(PROGNAME)


from cli import CommandLine, Command
from cmd.root import RootCommand

def main():
    root = RootCommand(name=PROGNAME.lower())
    cli = CommandLine(root)

    if len(sys.argv) > 1:
        return cli.execute(' '.join(sys.argv[1:]))

    cli.start(sys.argv[1:])

def setup_file_logger(log_file, verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s")

    handlers = []
    #file hanlder
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    handlers.append(file_handler)

    logging.basicConfig(level=log_level, handlers=handlers)

def parse_args():
    parser = argparse.ArgumentParser(description=_('Management tool of {}').format(PROGNAME), add_help=False)
    parser.add_argument('-v', required=False, action='store_true', default=False, help="enable debug messages")
    parser.add_argument('--forever', required=False, action='store_true', default=False, help="do not exit and run forever")
    known_args, unknown_args = parser.parse_known_args()
    # print(known_args, unknown_args, vars(known_args).keys(), sys.argv)
    for arg in ['-v', '--forever']:
        try:
            sys.argv.remove(arg)
        except ValueError:
            pass

    return known_args

if __name__ == '__main__':
    args = parse_args()
    log_file = "{0}/{1}.log".format(CURRENT_DIR, PROGNAME)
    setup_file_logger(log_file, args.v)
    if not main():
        sys.exit(-1)
    if args.forever:
        while  True:
            time.sleep(60)
            # print("I am sleeping ...")
