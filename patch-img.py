#!/usr/bin/python

import mmap, argparse

parser = argparse.ArgumentParser(description='Inplace find/replace a file. Replaces the first occurrence only.')

parser.add_argument('find', type=str)
parser.add_argument('replace', type=str)
parser.add_argument('file', type=argparse.FileType('r+b'))

args = parser.parse_args()

if len(args.find) != len(args.replace):
    raise Exception("'find' and 'replace' must be the same length")

try:
    s = mmap.mmap(args.file.fileno(), 0)

    offset = s.find(args.find)

    if offset == -1:
        raise Exception("'find' not found in file.")

    s[offset:offset+len(args.replace)] = args.replace
finally:
    s.close()
    args.file.close()
