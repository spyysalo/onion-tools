#!/usr/bin/python3

import sys
import json
import logging

from argparse import ArgumentParser


DESCRIPTION = 'Convert TSV with ID and text fields to vertical file'


# Escapes for XML attributes
XML_ATTR_ESCAPES = [
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('"', '&quot;'),
    # ("'", '&apos;'),   # assume " quotes, so not needed
]


def argparser():
    ap = ArgumentParser(description=DESCRIPTION)
    ap.add_argument('file', nargs='+')
    return ap


def xml_attr_escape(string):
    # Escape string for use as XML attribute
    for char, escape in XML_ATTR_ESCAPES:
        string = string.replace(char, escape)
    return string


def tsv_to_vert(fn, options):
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            try:
                id_, text = l.split('\t')
                text = json.loads(text)    # assume JSON escaping
            except Exception as e:
                logging.error(f'failed to parse {fn} line {ln}: {e}: {l}')
                continue
            print(f'<doc id="{xml_attr_escape(id_)}">')
            for para in text.split('\n'):
                print(f'<p>')
                for token in para.split():
                    print(token)
                print(f'</p>')
            print(f'</doc>')


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        tsv_to_vert(fn, args)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
