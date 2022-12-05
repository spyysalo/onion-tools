#!/usr/bin/env python3

# Convert Onion vert format into simple JSONL document format.

import sys
import re
import json
import xml.etree.ElementTree as ET
import logging

from ast import literal_eval
from argparse import ArgumentParser


DOC_TAG = 'doc'
PARA_TAG = 'p'


def argparser():
    ap = ArgumentParser()
    ap.add_argument('vert', nargs='+')
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
        if l.startswith(f'<{DOC_TAG}>') or l.startswith(f'<{DOC_TAG} '):
            assert current_doc is None
            current_doc = {}
            try:
                elem = parse_start_tag(l)
            except Exception as e:
                logging.error(f'failed to parse {f.name} line {ln}: {e}: {l}')
                raise
            current_doc['text'] = []
            for a, v in elem.attrib.items():
                current_doc[a] = v
        elif l.startswith(f'</{DOC_TAG}>'):
            assert current_doc is not None
            current_doc['text'] = '\n'.join(current_doc['text'])
            yield current_doc
            current_doc = None
        elif l.startswith(f'<{PARA_TAG}>') or l.startswith(f'<{PARA_TAG} '):
            assert current_para is None
            current_para = []
        elif l.startswith(f'</{PARA_TAG}>'):
            assert current_para is not None
            para_text = ' '.join(current_para)
            current_doc['text'].append(para_text)
            current_para = None
        else:
            current_para.append(unescape_token(l))
    assert current_doc is None


def renormalize_space(text):
    paragraphs = [p for p in re.split(r'\n\n+', text) if p and not p.isspace()]
    return '\n\n'.join(p.strip() for p in paragraphs)


def main(argv):
    args = argparser().parse_args(argv[1:])

    for fn in args.vert:
        with open(fn) as f:
            for doc in read_documents(f):
                doc['text'] = renormalize_space(doc['text'])
                print(json.dumps(doc, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
