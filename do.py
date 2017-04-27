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
from heapq import heappush, heappop
from sortedcontainers import SortedList
from geo.tycat import tycat
from geo.segment import load_segments, load_segments_stdin, Segment
from SweepLine import SweepLines

DEBUG = True
ENTER = True

def test(filename):
    """
    run bentley ottmann
    """
    events = [] #Tas des événements: (point, type_d_evenement)
    dict_seg = {} #Dictionnaire contenant les segments au point (point, type_d_evenement)
    sweep = SweepLines() #(Sorted)List des segments en vie
    results = [] #Les points finaux
    nb_coupes = 0 #Si un point d'intersection apparait dans plusieurs segments, il compte plusieurs fois

    if filename is not None:
        adjuster, segments_origin = load_segments(filename)
    else:
        adjuster, segments_origin = load_segments_stdin()
    tycat(segments_origin)

    for segment in segments_origin: #On ajoute les événements adéquats

        pt_min, pt_max = min(segment.endpoints), max(segment.endpoints)
        heappush(events, pt_min)
        heappush(events, pt_max)
        if pt_min in dict_seg:
            dict_seg[pt_min][0].append(segment)
        else:
            dict_seg[pt_min] = [[segment], [], []]
        if pt_max in dict_seg:
            dict_seg[pt_max][2].append(segment)
        else:
            dict_seg[pt_max] = [[], [], [segment]]

    while events: #Traitement des événements
        current = heappop(events)
        segments = dict_seg[current]

        if DEBUG:
            print("Current:", current, segments)
            print("Events:", events)
            print("SL:", len(sweep), sweep)
            tycat(segments_origin, results, current)
            print("in", segments[0])
            print("inter", segments[1])
            print("out", segments[2])

        if segments[2]: # out
            while segments[2]:
                segment = segments[2].pop()
                node = sweep.put(segment)
                left = node.predecessor()
                right = node.successor()
                if left and right:
                    left = left.value
                    right = right.value
                    intrsctn = segment.intersection_with(right)
                    if intrsctn and \
                        intrsctn.coordinates[1] <= current.coordinates[1] and\
                        intrsctn.coordinates[0] != current.coordinates[0]:
                        heappush(events, intrsctn)
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [left, right], []]
                        else:
                            segments = dict_seg[intrsctn]
                            if left not in segments[1]:
                                segments[1].append(left)
                            if right not in segments[1]:
                                segments[1].append(right)
                sweep.delete(segment)

        if segments[1]: # inter
            nb_coupes += 1
            results.append(current)
            for segment in segments[1]:
                sweep.delete(segment)
            Segment.point = current
            for segment in segments[1]:
                sweep.put(segment)
            u = sweep.search(min(segments[1]))
            right = u.successor()
            if right:
                u = u.value
                right = right.value
                intrsctn = u.intersection_with(right)
                if intrsctn is not None:
                    intrsctn = adjuster.hash_point(intrsctn)
                    if intrsctn and \
                        intrsctn.coordinates[1] <= current.coordinates[1] and\
                        intrsctn.coordinates[0] != current.coordinates[0]:
                        heappush(events, intrsctn)
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [u, right], []]
                        else:
                            segments = dict_seg[intrsctn]
                            if u not in segments[1]:
                                segments[1].append(u)
                            if right not in segments[1]:
                                segments[1].append(right)
            v = sweep.search(max(segments[1]))
            left = v.predecessor()
            if left:
                v = v.value
                left = left.value
                intrsctn = v.intersection_with(left)
                if intrsctn is not None:
                    intrsctn = adjuster.hash_point(intrsctn)
                    if intrsctn and \
                        intrsctn.coordinates[1] <= current.coordinates[1] and\
                        intrsctn.coordinates[0] != current.coordinates[0]:
                        heappush(events, intrsctn)
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [left, v], []]
                        else:
                            segments = dict_seg[intrsctn]
                            if v not in segments[1]:
                                segments[1].append(v)
                            if left not in segments[1]:
                                segments[1].append(left)

        if segments[0]: # in
            while segments[0]:
                segment = segments[0].pop()
                node = sweep.put(segment)
                left = node.predecessor()
                if left:
                    left = left.value
                    intrsctn = segment.intersection_with(left)
                    if intrsctn and \
                        intrsctn.coordinates[1] <= current.coordinates[1] and\
                        intrsctn.coordinates[0] != current.coordinates[0]:
                        intrsctn = adjuster.hash_point(intrsctn)
                        heappush(events, intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [left, segment], []]
                        else:
                            segments = dict_seg[intrsctn]
                            if left not in segments[1]:
                                segments[1].append(left)
                            if segment not in segments[1]:
                                segments[1].append(segment)
                right = node.successor()
                if right:
                    right = right.value
                    intrsctn = segment.intersection_with(right)
                    if intrsctn and \
                        intrsctn.coordinates[1] <= current.coordinates[1] and\
                        intrsctn.coordinates[0] != current.coordinates[0]:
                        intrsctn = adjuster.hash_point(intrsctn)
                        heappush(events, intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [right, segment], []]
                        else:
                            segments = dict_seg[intrsctn]
                            if right not in segments[1]:
                                segments[1].append(right)
                            if segment not in segments[1]:
                                segments[1].append(segment)
        if ENTER:
            input("Press [ENTER] to continue...\n")
    tycat(segments_origin, results)
    if ENTER:
        input("Press [ENTER] to continue...\n")
    print("le nombre d'intersections (= le nombre de points differents) est", len(results))
    print("le nombre de coupes dans les segments est", nb_coupes)

def main():
    """
    launch test on each file.
    """
    if len(sys.argv) == 1:
        test(None)
    for filename in sys.argv[1:]:
        test(filename)

main()