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

def load_events(segments_origin, events, dict_seg):
    """
    Load all events
    """
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

def load_file(filename, graph):
    """
    Load file
    """
    if filename is not None:
        adjuster, segments_origin = load_segments(filename)
    else:
        adjuster, segments_origin = load_segments_stdin()
    if graph:
        tycat(segments_origin)
    Segment.adjuster = adjuster
    return adjuster, segments_origin

def test(filename, graph):
    """
    run bentley ottmann
    """
    events = [] #Tas des événements: (point, type_d_evenement)
    dict_seg = {} #Dictionnaire contenant les segments au point (point, type_d_evenement)
    sweep = SortedList() #(Sorted)List des segments en vie
    results = [] #Les points finaux

    _, segments_origin = load_file(filename, graph)
    load_events(segments_origin, events, dict_seg)


    while events: #Traitement des événements
        current = heappop(events)
        segments = dict_seg[current]

        if segments[2]: # out
            while segments[2]:
                segment = segments[2].pop()
                for other in sweep:
                    intrsctn = segment.intersection_with(other)
                    if intrsctn and intrsctn not in results:
                        results.append(intrsctn)
                sweep.remove(segment)

        if segments[0]: # in
            while segments[0]:
                segment = segments[0].pop()
                sweep.add(segment)
                for other in sweep:
                    intrsctn = segment.intersection_with(other)
                    if intrsctn and intrsctn not in results:
                        results.append(intrsctn)
    if graph:
        tycat(segments_origin, results)
    if filename:
        print(filename, ": ", len(results), " intersection(s)")
    else:
        print("stdin: ", len(results), " intersection(s)")

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
