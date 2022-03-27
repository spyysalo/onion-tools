#!/usr/bin/env python3

import sys
import json

from argparse import ArgumentParser
from difflib import unified_diff


def argparser():
    ap = ArgumentParser()
    ap.add_argument('original')
    ap.add_argument('filtered')
    return ap


def skip_until(orig, filt_item):
    for orig_line in orig:
        orig_item = json.loads(orig_line)
        if filt_item is not None and orig_item['id'] == filt_item['id']:
            return orig_item
        else:
            print(f'Only in {orig.name}: {orig_item["id"]}')
            for line in orig_item['text'].splitlines():
                print('<', line)
            print('-'*78)
    return None


def split_text_for_diff(text):
    # assure terminal newline for diff
    text = text.rstrip('\n') + '\n'
    return text.splitlines(keepends=True)


def process(orig, filt, args):
    for filt_line in filt:
        filt_item = json.loads(filt_line)
        orig_item = skip_until(orig, filt_item)
        if orig_item is None:
            break
        orig_text = split_text_for_diff(orig_item['text'])
        filt_text = split_text_for_diff(filt_item['text'])
        if orig_text == filt_text:
            continue
        print(f'diff {orig_item["id"]}')
        for line in unified_diff(orig_text, filt_text):
            if line.startswith('---') or line.startswith('+++'):
                pass
            elif line.startswith('-'):
                print('<', line[1:].rstrip('\n'))
            elif line.startswith('+'):
                print('>', line[1:].rstrip('\n'))
            elif line.startswith('@@'):
                print(line.rstrip('\n'))
        print('-'*78)
    skip_until(orig, None)


def main(argv):
    args = argparser().parse_args(argv[1:])
    with open(args.original) as orig:
        with open(args.filtered) as filt:
            process(orig, filt, args)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
