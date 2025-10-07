#!/usr/bin/env python3
# FJN, Centre Paul Langevin, Aussois, Savoie, 7.10.2025

"""
    Extracts innermost content from all [[...]] occurrences
    
Syntax:
    
    extract_brackets.py FILE [ANOTHER_FILE] [...]
    
F. Nedelec, 7.10.2025
"""

import sys, os

def process(file):
    """
    Extracts innermost content from all [[...]] occurrences
    """
    all = []
    res = ''
    line = 1
    depth = 0
    with open(file, "r") as f:
        for chunk in iter(lambda: f.read(1024), ''):
            #print(chunk)
            for c in chunk:
                if c == ']':
                    if depth == 2 and res:
                        all.append([res, line])
                        res = ''
                    depth -= 1
                if depth >= 2:
                    res += c
                if c == '[':
                    depth += 1
                if c == '\n':
                    line += 1
                #print(repr(c))
    return all


def main(args):
    files = []
    
    for arg in args:
        if os.path.isfile(arg):
            files.append(arg)
        else:
            sys.stderr.write("  Error: unexpected argument `%s'\n" % arg)
            sys.exit()
    
    if not files:
        sys.stderr.write("  Error: you must specify files\n")
        sys.exit()
    
    for f in files:
        res = process(f)
        if len(files) > 1:
            print(f, ': ')
        for i in res:
            print(f' line {i[1]:4} : {i[0]}')

#------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1].endswith("help"):
        print(__doc__)
    else:
        main(sys.argv[1:])

