#!/usr/bin/env python3

header = r"""
"""

footer = r"""
"""

import sys
import re

def main():
    symtab = {}
    for line in sys.stdin:
        line = line.rstrip()
        part = line.split("\t", 2)
        if 2 != len(part):
            continue
        part = part[1].split()
        if 3 != len(part) or "GLIBC_PRIVATE" in part[1] or part[2].startswith("GLIBC_"):
            continue
        sym = part[2]
        ver = part[1]
        symtab.setdefault(sym, []).append(ver)

    print(header)
    for sym in sorted(symtab.keys()):
        ver = symtab[sym]
        ver = sorted(ver, key = lambda v: [int(p) if p.isdigit() else p.lower() for p in re.split(r'(\d+)', v)])
        ver = ver[-1].lstrip("(").rstrip(")")
        print(f'__asm__(".symver {sym} {sym}@{ver}")')
    print(footer)

if __name__ == "__main__":
    main()
