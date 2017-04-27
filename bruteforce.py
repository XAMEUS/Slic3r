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
from geo.segment import load_segments, load_segments_stdin, Segment, key

def test(filename):
    _, segments_origin = load_segments(filename)
    results = []
    for sega, segb in combinations(segments_origin, 2):
        candidate = sega.intersection_with(segb)
        if candidate is not None:
            results.append(candidate)
    tycat(segments_origin, results)


def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

main()
