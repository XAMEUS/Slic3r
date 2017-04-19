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
    sweep = SortedList()
    result = []
    print("Events (init):", events)
    print("\n========\n  LOOP  \n========\n\n   ")
    while True:
        try:
            current, event_type, segment = events.pop(0)

            print("Current:", current, event_type, segment)
            print("Events:", events)
            print("SL:", len(sweep), sweep)

            if event_type == "in":
                xpos, angle = segment.key(current)
                key = (xpos, angle, segment)
                sweep.add(key)
                left = sweep.bisect_left(key) - 1
                if left > -1:
                    _, _, left = sweep[left]
                    intrsctn = segment.intersection_with(left)
                    if intrsctn is not None:
                        events.add((intrsctn, "x", (left, s)))
                right = sweep.bisect_right(key)
                if right < len(sweep):
                    _, _, right = sweep[right]
                    intrsctn = segment.intersection_with(right)
                    if intrsctn is not None:
                        events.add((intrsctn, "x", (s, right)))

            elif event_type == "out":
                xpos, angle = segment.key(current)
                key = (segment.endpoints[0].coordinates[0] if segment.endpoints[0] != current else segment.endpoints[1].coordinates[0], angle, segment)
                sweep.remove(key)
                left = sweep.bisect_left(key)
                right = sweep.bisect_right(key)
                if left > -1 and right < len(sweep):
                    _, _, left = sweep[left]
                    _, _, right = sweep[right]
                    intrsctn = left.intersection_with(right)
                    if intrsctn is not None:
                        events.add((intrsctn, "x", (left, right)))

            else: #event_type == "x"
                result.append(current)
                # TODO swapp

            tycat(segments, result, current)
            input("Press [ENTER] to continue...\n")

        except IndexError:
            break

    print("\n\n=========\n THE END\n=========")
    print("Events:", events)
    print("SL:", sweep)
    print("IL:", result)
    tycat(segments, result)
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
