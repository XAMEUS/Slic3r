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

DEBUG = False
ENTER = False

def test(filename):
    """
    run bentley ottmann
    """
    events = [] #Tas des événements: (point, type_d_evenement)
    dict_seg = {} #Dictionnaire contenant les segments au point (point, type_d_evenement)
    sweep = SortedList() #(Sorted)List des segments en vie
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
            tycat(segments_origin, results, current, sweep)
            print("in", segments[0])
            print("inter", segments[1])
            print("out", segments[2])

        if segments[2]: # out
            while segments[2]:
                segment = segments[2].pop()
                i = sweep.index(segment)
                left = i-1
                right = i+1
                if left >= 0 and right < len(sweep):
                    left = sweep[left]
                    right = sweep[right]
                    intrsctn = segment.intersection_with(right)
                    if intrsctn and \
                        intrsctn.coordinates[1] <= current.coordinates[1] and\
                        intrsctn.coordinates[0] != current.coordinates[0]:
                        heappush(events, intrsctn)
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [left, right], []]
                        else:
                            if left not in segments[1]:
                                segments[1].append(left)
                            if right not in segments[1]:
                                segments[1].append(right)
                sweep.remove(segment)

        if segments[1]: # inter
            nb_coupes += 1
            results.append(current)
            for segment in segments[1]:
                sweep.remove(segment)
            for segment in segments[1]:
                sweep.add(segment)
            u = sweep.index(max(segments[1]))
            right = u+1
            if right < len(sweep):
                u = sweep[u]
                right = sweep[right]
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
                            if u not in segments[1]:
                                segments[1].append(u)
                            if right not in segments[1]:
                                segments[1].append(right)
            v = sweep.index(min(segments[1]))
            left = v-1
            if left >= 0:
                v = sweep[v]
                left = sweep[left]
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
                            if v not in segments[1]:
                                segments[1].append(v)
                            if left not in segments[1]:
                                segments[1].append(left)

        if segments[0]: # in
            while segments[0]:
                segment = segments[0].pop()
                sweep.add(segment)
                i = sweep.index(segment)
                left = i-1
                if left >= 0:
                    left = sweep[left]
                    intrsctn = segment.intersection_with(left)
                    if intrsctn and \
                        intrsctn.coordinates[1] <= current.coordinates[1] and\
                        intrsctn.coordinates[0] != current.coordinates[0]:
                        intrsctn = adjuster.hash_point(intrsctn)
                        heappush(events, intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [left, segment], []]
                        else:
                            segments = dict_seg[current]
                            if left not in segments[1]:
                                segments[1].append(left)
                            if segment not in segments[1]:
                                segments[1].append(segment)
                right = i+1
                if right < len(sweep):
                    right = sweep[right]
                    intrsctn = segment.intersection_with(right)
                    if intrsctn and \
                        intrsctn.coordinates[1] <= current.coordinates[1] and\
                        intrsctn.coordinates[0] != current.coordinates[0]:
                        intrsctn = adjuster.hash_point(intrsctn)
                        heappush(events, intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [right, segment], []]
                        else:
                            segments = dict_seg[current]
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
