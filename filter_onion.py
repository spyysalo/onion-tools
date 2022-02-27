#!/usr/bin/env python3

import sys

from collections import Counter
from argparse import ArgumentParser


DESCRIPTION = 'Filter onion output'

DOC_TAG = 'doc'
PARA_TAG = 'p'


def argparser():
    ap = ArgumentParser(description=DESCRIPTION)
    ap.add_argument(
        '--max-doc-duprate',
        type=float,
        default=0.5,
        help='maximum ratio of duplicate to total document lines'
    )
    ap.add_argument(
        '--no-trim',
        default=False,
        action='store_true',
        help='do not remove duplicate paragraphs at document start and end'
    )
    ap.add_argument(
        '--remove-all-dups',
        default=False,
        action='store_true',
        help='remove all duplicate paragraphs'
    )
    ap.add_argument('file', nargs='+')
    return ap


def split_into_paragraphs(lines):
    paragraphs, current_lines = [], []
    for line in lines:
        current_lines.append(line)
        mark, rest = line.split('\t')
        if rest.startswith(f'</{PARA_TAG}>'):
            paragraphs.append(current_lines)
            current_lines = []
    return paragraphs


def is_duplicate_paragraph(lines):
    return lines[0].startswith('1')


def trim_paragraphs(paragraphs):
    for start in range(len(paragraphs)):
        if not is_duplicate_paragraph(paragraphs[start]):
            break
    for end in reversed(range(start, len(paragraphs))):
        if not is_duplicate_paragraph(paragraphs[end]):
            break
    return paragraphs[start:end+1]


def process_document(lines, stats, args):
    stats['total_docs'] += 1
    stats['total_lines'] += len(lines)

    start_line, lines, end_line = lines[0], lines[1:-1], lines[-1]
    paragraphs = split_into_paragraphs(lines)

    if args.remove_all_dups:
        paragraphs = [p for p in paragraphs if not is_duplicate_paragraph(p)]
    elif not args.no_trim:
        paragraphs = trim_paragraphs(paragraphs)

    if not paragraphs:
        return    # all removed

    lines = [start_line] + [l for p in paragraphs for l in p] + [end_line]
    marks = [int(l.split('\t')[0]) for l in lines]
    rate = sum(marks)/len(marks)

    if rate > args.max_doc_duprate:
        return    # too much duplication remaining

    stats['output_docs'] += 1
    for l in lines:
        stats['output_lines'] += 1
        print(l)


def filter_onion(fn, stats, args):
    current_lines = []
    with open(fn) as f:
        for ln, line in enumerate(f, start=1):
            line = line.rstrip('\n')
            try:
                mark, rest = line.split('\t')
                mark = int(mark)
            except Exception as e:
                logging.error(f'failed to parse {fn} line {ln}: {e}: {l}')
                raise
            current_lines.append(line)
            if rest.startswith(f'</{DOC_TAG}>'):
                process_document(current_lines, stats, args)
                current_lines = []


def main(argv):
    args = argparser().parse_args(argv[1:])

    stats = Counter()
    for fn in args.file:
        filter_onion(fn, stats, args)

    for item in ('lines', 'docs'):
        o, t = stats[f'output_{item}'], stats[f'total_{item}']
        print(f'output {o}/{t} ({o/t:.1%}) {item}', file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
