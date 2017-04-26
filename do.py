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
    sweep = SortedList()
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

            tmp_sweep = SortedList()
            for line in sweep:
                tmp_sweep.add(line)
            sweep = tmp_sweep
            if DEBUG:
                print("SL:", len(sweep), sweep)

            if event_type == "in":
                sweep.add(segment)
                i = sweep.index(segment)
                left = i-1
                if left >= 0:
                    left = sweep[left]
                    intrsctn = segment.intersection_with(left)
                    if intrsctn is not None and intrsctn.coordinates[1] <= current.coordinates[1] \
                                            and intrsctn.coordinates[0] != current.coordinates[0]:
                        events.add((intrsctn, "x", (left, segment)))
                right = i+1
                if right < len(sweep):
                    right = sweep[right]
                    intrsctn = segment.intersection_with(right)
                    if intrsctn is not None and intrsctn.coordinates[1] <= current.coordinates[1] \
                                            and intrsctn.coordinates[0] != current.coordinates[0]:
                        events.add((intrsctn, "x", (segment, right)))

            elif event_type == "out":
                i = sweep.index(segment)
                left = i-1
                right = i+1
                if left >= 0 and right < len(sweep):
                    left = sweep[left]
                    right = sweep[right]
                    intrsctn = left.intersection_with(right)
                    if intrsctn is not None and intrsctn.coordinates[1] <= current.coordinates[1] \
                                            and intrsctn.coordinates[0] != current.coordinates[0]:
                        events.add((intrsctn, "x", (left, right)))
                sweep.remove(segment)

            else: #event_type == "x"
                result.append(current)
                u = sweep.index(segment[0])
                right = u+1
                if right < len(sweep):
                    u = sweep[u]
                    right = sweep[right]
                    intrsctn = u.intersection_with(right)
                    print(current, intrsctn)
                    if intrsctn is not None and intrsctn.coordinates[1] <= current.coordinates[1] \
                                            and intrsctn.coordinates[0] != current.coordinates[0]:
                        events.add((intrsctn, "x", (u, right)))
                v = sweep.index(segment[1])
                left = v-1
                if left >= 0:
                    v = sweep[v]
                    left = sweep[left]
                    intrsctn = v.intersection_with(left)
                    print(current, intrsctn)
                    if intrsctn is not None and intrsctn.coordinates[1] <= current.coordinates[1] \
                                            and intrsctn.coordinates[0] != current.coordinates[0]:
                        events.add((intrsctn, "x", (left, v)))

            if DEBUG:
                print("Events:", events)
            if DEBUG:
                print("SL:", len(sweep), sweep)

            tycat(segments, result, current)
            input("Press [ENTER] to continue...\n")

        except IndexError as e:
            print(e)
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
