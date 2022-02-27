#!/usr/bin/env python3

# Convert simple JSONL document format with keys "text", "id", and
# "meta" into Onion vert format.

import sys
import json
import xml.etree.ElementTree as ET
import logging

from argparse import ArgumentParser


DOC_TAG = 'doc'
PARA_TAG = 'p'


def argparser():
    ap = ArgumentParser()
    ap.add_argument('jsonl', nargs='+')
    return ap


def escape_token(text):
    # Escape in case "<doc" or "<p" appear in source
    if text.startswith('<'):
        return '&lt;' + text[1:]
    elif text.startswith('&'):
        return '&amp;' + text[1:]
    else:
        return text


def output_document(data, out=sys.stdout):
    paragraphs = data['text'].split('\n')

    attrib = {}
    for key in ('id', 'meta'):
        if key in data:
            attrib[key] = data.pop(key)
    extra = { key for key in data if key != 'text' }
    if extra:
        logging.warning(f'extra attributes: {extra}')

    elem = ET.Element(DOC_TAG, attrib)
    elem_string = ET.tostring(elem, encoding='unicode')
    assert elem_string.endswith(' />')
    doc_start_tag = elem_string[:-3] + '>'
    doc_end_tag = f'</{DOC_TAG}>'

    print(doc_start_tag, file=out)
    for paragraph in paragraphs:
        print(f'<{PARA_TAG}>', file=out)
        for token in paragraph.split():
            print(escape_token(token), file=out)
        print(f'</{PARA_TAG}>', file=out)
    print(doc_end_tag, file=out)


def main(argv):
    args = argparser().parse_args(argv[1:])

    for fn in args.jsonl:
        with open(fn) as f:
            for ln, l in enumerate(f, start=1):
                data = json.loads(l)
                output_document(data)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
