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
from sortedcontainers import SortedList
from geo.segment import load_segments, Segment
from geo.tycat import tycat
from SweepLine import SweepLines

DEBUG = False

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
    sweep = SweepLines()
    result = []
    print("Events (init):", events)
    print("\n========\n  LOOP  \n========\n\n   ")
    while True:
        try:
            current, event_type, segment = events.pop(0)

            Segment.point = current

            if DEBUG:
                print("Current:", current, event_type, segment)
            if DEBUG:
                print("Events:", events)
            if DEBUG:
                print("SL:", len(sweep), sweep)

            tmp_sweep = SweepLines()
            for node in sweep:
                tmp_sweep.put(node.value)
            sweep = tmp_sweep
            if DEBUG:
                print("SL:", len(sweep), sweep)

            if event_type == "in":
                node = sweep.put(segment)
                left = node.predecessor()
                if left:
                    left = left.value
                    intrsctn = segment.intersection_with(left)
                    if intrsctn is not None:
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn.coordinates[1] <= current.coordinates[1] and intrsctn.coordinates[0] != current.coordinates[0]:
                            events.add((intrsctn, "x", (left, segment)))
                right = node.successor()
                if right:
                    right = right.value
                    intrsctn = segment.intersection_with(right)
                    if intrsctn is not None:
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn.coordinates[1] <= current.coordinates[1] and intrsctn.coordinates[0] != current.coordinates[0]:
                            events.add((intrsctn, "x", (segment, right)))

            elif event_type == "out":
                node = sweep.search(segment)
                left = node.predecessor()
                right = node.successor()
                if left and right:
                    left = left.value
                    right = right.value
                    intrsctn = left.intersection_with(right)
                    if intrsctn is not None:
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn.coordinates[1] <= current.coordinates[1] and intrsctn.coordinates[0] != current.coordinates[0]:
                            events.add((intrsctn, "x", (left, right)))
                sweep.delete(segment)

            else: #event_type == "x"
                result.append(current)
                u = sweep.search(segment[0])
                right = u.successor()
                if right:
                    intrsctn = u.value.intersection_with(right.value)
                    if intrsctn is not None:
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn.coordinates[1] <= current.coordinates[1] and intrsctn.coordinates[0] != current.coordinates[0]:
                            events.add((intrsctn, "x", (u.value, right.value)))
                v = sweep.search(segment[1])
                left = v.predecessor()
                if left:
                    intrsctn = v.value.intersection_with(left.value)
                    if intrsctn is not None:
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn.coordinates[1] <= current.coordinates[1] and intrsctn.coordinates[0] != current.coordinates[0]:
                            events.add((intrsctn, "x", (left.value, v.value)))

            if DEBUG:
                print("Events:", events)
            if DEBUG:
                print("SL:", len(sweep), sweep)

            #tycat(segments, result, current)
            #input("Press [ENTER] to continue...\n")

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
