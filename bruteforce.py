#!/usr/bin/env python3
"""
this tests bentley ottmann on given .bo files.
for each file:
    - we display segments
    - run bentley ottmann
    - display results
    - print some statistics
"""
import sys
from itertools import combinations
from geo.tycat import tycat
from geo.segment import load_segments, load_segments_stdin

def test(filename, graph):
    """
    Launch bruteforce test on filename or stdin
    """
    if filename is not None:
        _, segments_origin = load_segments(filename)
    else:
        _, segments_origin = load_segments_stdin()
    if graph:
        tycat(segments_origin)
    results = []
    for sega, segb in combinations(segments_origin, 2):
        candidate = sega.intersection_with(segb)
        if candidate is not None:
            results.append(candidate)
    if graph:
        tycat(segments_origin, results)


def main():
    """
    launch test on each file.
    """
    if len(sys.argv) == 1:
        test(None, True)
    for filename in sys.argv[1:]:
        test(filename, True)

if __name__ == '__main__':
    main()
