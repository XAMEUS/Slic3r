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
from geo.tycat import tycat
from sortedcontainers import SortedList
from geo.segment import load_segments, load_segments_stdin

DEBUG = True

def test(filename):
    """
    run bentley ottmann
    """
    events = [] #Tas des événements: (point, type_d_evenement)
    dict_seg = {} #Dictionnaire contenant les segments au point (point, type_d_evenement)
    sweep = SortedList() #(Sorted)List des segments en vie
    results = [] #Les points finaux

    if filename is not None:
        adjuster, SEGMENTS = load_segments(filename)
    else:
        adjuster, SEGMENTS = load_segments_stdin()
    tycat(SEGMENTS)

    for segment in SEGMENTS: #On ajoute les événements adéquats

        a, b = min(segment.endpoints), max(segment.endpoints)
        heappush(events, a)
        heappush(events, b)
        if a in dict_seg:
            dict_seg[a][0].append(segment)
            dict_seg[a][2].append(segment)
        else:
            dict_seg[a] = [[segment], [], []]
        if b in dict_seg:
            dict_seg[b][0].append(segment)
            dict_seg[b][2].append(segment)
        else:
            dict_seg[b] = [[], [], [segment]]

    while events: #Traitement des événements
        current = heappop(events)
        segments = dict_seg[current]
        if DEBUG:
            print("Current:", current, segments)
            print("Events:", events)
            print("SL:", len(sweep), sweep)
            tycat(SEGMENTS, results, current, sweep) #TODO: liste des segments en vie
            print(segments)

        if segments[2]: # out
            for segment in segments[2]:
                i = sweep.index(segment)
                left = i-1
                right = i+1
                if left >= 0 and right < len(sweep):
                    left = sweep[left]
                    right = sweep[right]
                    intrsctn = segment.intersection_with(right)
                    if intrsctn is not None:
                        intrsctn = adjuster.hash_point(intrsctn)
                        if intrsctn.coordinates[1] <= current.coordinates[1]:
                            heappush(events, intrsctn)
                            if intrsctn not in dict_seg:
                                dict_seg[intrsctn] = [[], [left, right], []]
                            else:
                                if left not in segments[1]:
                                    segments[1].append(left)
                                if right not in segments[1]:
                                    segments[1].append(right)
                sweep.remove(segment)

        if segments[1]:
            pass

        if segments[0]: # in
            for segment in segments[0]:
                sweep.add(segment)
                i = sweep.index(segment)
                left = i-1
                if left >= 0:
                    left = sweep[left]
                    intrsctn = segment.intersection_with(left)
                    if intrsctn and intrsctn.coordinates[1] <= current.coordinates[1]:
                        heappush(events, intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [left, current], []]
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
                    if intrsctn:
                        heappush(events, intrsctn)
                        if intrsctn not in dict_seg:
                            dict_seg[intrsctn] = [[], [right, current], []]
                        else:
                            segments = dict_seg[current]
                            if right not in segments[1]:
                                segments[1].append(right)
                            if segment not in segments[1]:
                                segments[1].append(segment)

        input("Press [ENTER] to continue...\n")
    tycat(SEGMENTS, results)
    input("Press [ENTER] to continue...\n")
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
    if(len(sys.argv) == 1):
        test(None)
    for filename in sys.argv[1:]:
        test(filename)

main()
