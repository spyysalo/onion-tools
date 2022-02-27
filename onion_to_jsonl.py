#!/usr/bin/env python3

# Convert Onion output format with "id" and "meta" document attributes
# into simple JSON with "text", "id", and "meta" keys.

import sys
import json
import xml.etree.ElementTree as ET
import logging

from ast import literal_eval
from argparse import ArgumentParser


DOC_TAG = 'doc'
PARA_TAG = 'p'


def argparser():
    ap = ArgumentParser()
    ap.add_argument('onion', nargs='+')
    return ap


def unescape_token(text):
    if text.startswith('&lt;'):
        return '<' + text[4:]
    elif text.startswith('&amp;'):
        return '&' + text[5:]
    else:
        return text


def parse_start_tag(string):
    assert string.endswith('>')
    string = string[:-1] + ' />'
    return ET.fromstring(string)


def read_documents(f):
    current_doc, current_para = None, None
    for ln, l in enumerate(f, start=1):
        l = l.rstrip('\n')
        try:
            mark, l = l.split('\t')
            mark = int(mark)
        except Exception as e:
            logging.error(f'failed to parse {fn} line {ln}: {e}: {l}')
            continue
        if l.startswith(f'<{DOC_TAG}>') or l.startswith(f'<{DOC_TAG} '):
            assert current_doc is None
            current_doc = {}
            elem = parse_start_tag(l)
            current_doc['id'] = elem.attrib['id']
            if 'meta' in elem.attrib:
                current_doc['meta'] = literal_eval(elem.attrib['meta'])
            current_doc['text'] = []
        elif l.startswith(f'</{DOC_TAG}>'):
            assert current_doc is not None
            current_doc['text'] = '\n'.join(current_doc['text'])
            yield current_doc
            current_doc = None
        elif l.startswith(f'<{PARA_TAG}>') or l.startswith(f'<{PARA_TAG} '):
            assert current_para is None
            current_para = []
            elem = parse_start_tag(l)
        elif l.startswith(f'</{PARA_TAG}>'):
            assert current_para is not None
            para_text = ' '.join(current_para)
            current_doc['text'].append(para_text)
            current_para = None
        else:
            current_para.append(unescape_token(l))
    assert current_doc is None


def main(argv):
    args = argparser().parse_args(argv[1:])

    for fn in args.onion:
        with open(fn) as f:
            for doc in read_documents(f):
                print(json.dumps(doc, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
