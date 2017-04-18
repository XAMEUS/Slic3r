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
from geo.segment import load_segments
from geo.tycat import tycat
from sortedcontainers import SortedList

def test(filename):
    """
    run bentley ottmann
    """
    adjuster, segments = load_segments(filename)
    #segments = sorted(segments, key=lambda x: min(x.endpoints[0].coordinates[1],
    #                                              x.endpoints[0].coordinates[1]))
    events = SortedList()
    for s in segments:
        events.add((min(s.endpoints), "in", s))
        events.add((max(s.endpoints), "out", s))
    SL = SortedList()
    IL = []
    print("Events (init):", events)
    print("\n========\n  LOOP  \n========\n\n   ")
    while True:
        try:
            p, t, s = events.pop(0)

            print("Current:", p, t, s)
            print("Events:", events)
            print("SL:", len(SL), SL)

            tycat(segments, IL, p)
            input("Press [ENTER] to continue...\n")

        except IndexError:
            break

    print("\n\n=========\n THE END\n=========")
    print("Events:", events)
    print("SL:", SL)
    print("IL:", IL)
    tycat(segments, IL)
    #TODO: merci de completer et de decommenter les lignes suivantes
    #results = lancer bentley ottmann sur les segments et l'ajusteur
    #...
    #tycat(segments, intersections)
    #print("le nombre d'intersections (= le nombre de points differents) est", ...)
    #print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
    # plusieurs segments, il compte plusieurs fois) est", ...)

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        test(filename)

main()
