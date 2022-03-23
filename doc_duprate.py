#!/usr/bin/python3

import sys
import logging
import xml.etree.ElementTree as ET

from argparse import ArgumentParser


DESCRIPTION = 'Get document duplication rate from onion output'

DOC_TAG = 'doc'
PARA_TAG = 'p'


def argparser():
    ap = ArgumentParser(description=DESCRIPTION)
    ap.add_argument('file', nargs='+')
    return ap


def get_id(docstart):
    element = ET.fromstring(f'{docstart}</doc>')
    return element.attrib['id']


def get_duprate(fn, options):
    current_id = None
    current_marks = []
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            try:
                mark, token = l.split('\t')
                mark = int(mark)
            except Exception as e:
                logging.error(f'failed to parse {fn} line {ln}: {e}: {l}')
                continue
            if token.startswith(f'<{DOC_TAG}'):
                current_marks = []
                try:
                    current_id = get_id(token)
                except Exception as e:
                    logging.error(f'failed to parse {fn} line {ln}: {e}: {l}')
                    current_id = None
                    continue
            if current_id is not None:
                current_marks.append(mark)
            if token.startswith(f'</{DOC_TAG}>'):
                rate = sum(current_marks)/len(current_marks)
                print(f'{rate}\t{current_id}')
                current_id = None
                current_marks = []


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        get_duprate(fn, args)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
