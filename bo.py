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
from geo.segment import load_segments, load_segments_stdin, Segment, key, compute_x

def load_events(segments_origin, events, dict_seg, results):
    """
    Load all events
    """
    for segment in segments_origin: #On ajoute les événements adéquats
        pt_min, pt_max = min(segment.endpoints), max(segment.endpoints)
        if pt_min not in dict_seg:
            heappush(events, pt_min)
            dict_seg[pt_min] = [set(), set()]
        dict_seg[pt_min][0].add(segment)
        if dict_seg[pt_min][0] and dict_seg[pt_min][1]:
            results.add(pt_min)
        if pt_max not in dict_seg:
            heappush(events, pt_max)
            dict_seg[pt_max] = [set(), set()]
        dict_seg[pt_max][1].add(segment)
        if (dict_seg[pt_max][0] and dict_seg[pt_max][1]) or \
           len(dict_seg[pt_max][0]) > 1 or \
           len(dict_seg[pt_max][1]) > 1:
            results.add(pt_max)
        if len(dict_seg[pt_min][0]) > 1 or len(dict_seg[pt_min][1]) > 1:
            results.add(pt_min)

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
    return adjuster, segments_origin

#pylint: disable-msg=too-many-arguments
def test_intersect(results, dict_seg, events, adjuster, current, order):
    """
    Have we a intersection ? If yes, we do the necessary
    """
    intrsctn = order[0].intersection_with(order[1])
    if intrsctn and intrsctn != current:
        intrsctn = adjuster.hash_point(intrsctn)
        if intrsctn not in results: # Intersection non-nulle et nouvelle
            results.add(intrsctn)
            if intrsctn not in dict_seg:
                heappush(events, intrsctn)
                dict_seg[intrsctn] = [set(), set()]
            tmp = dict_seg[intrsctn]
            for elem in order:
                if elem not in tmp[1]:
                    tmp[0].add(elem)
                tmp[1].add(elem)

def take_neighbors(sweep, segment, current):
    """
    Takes the index of the segment and its neighbors which not having the same key
    """
    try:
        i = sweep.bisect_left(segment)
        if sweep[i] != segment and i < len(sweep)-1:
            for i, tmp in enumerate(sweep):
                if tmp == segment:
                    break
        left = i-1-(i > 1 and key(sweep[i-1], current) == key(segment, current))
        right = i+1+(i < len(sweep)-1 and key(sweep[i+1], current) == key(segment, current))
        return i, left, right
    except IndexError:
        sweep = SortedList(list(sweep), load=10)
        return take_neighbors(sweep, segment, current)



def test(filename, graph):
    """
    run bentley ottmann
    """
    events = [] #Tas des événements: (point)
    dict_seg = {} #Dictionnaire contenant les segments (in, out) au point en arg
    sweep = SortedList(load=10) #(Sorted)List des segments en vie
    results = set() #Les points finaux

    adjuster, segments_origin = load_file(filename, graph)
    Segment.adjuster = adjuster
    load_events(segments_origin, events, dict_seg, results)

    while events: #Traitement des événements
        current = heappop(events) #On récupère le point à traiter
        segments = dict_seg[current] #On récupère ses segments associés (in, out)

        while segments[1]: #On traite les out
            segment = segments[1].pop()
            i, left, right = take_neighbors(sweep, segment, current)

            if left >= 0 and right < len(sweep):
                test_intersect(results, dict_seg, events, adjuster, current,
                               [sweep[left], sweep[right]])

            del sweep[i]

        Segment.point = current #On actualise le point: pt de référence

        while segments[0]: #On traite les in
            segment = segments[0].pop()
            sweep.add(segment)
            _, left, right = take_neighbors(sweep, segment, current)

            #On traite à gauche
            if left >= 0:
                test_intersect(results, dict_seg, events, adjuster, current,
                               [segment, sweep[left]])
            #Idem à droite
            if right < len(sweep):
                test_intersect(results, dict_seg, events, adjuster, current,
                               [segment, sweep[right]])

    return (segments_origin, results)

def main():
    """
    launch test on each file.
    """
    if len(sys.argv) == 1:
        segments_origin, results = test(None, True)
        tycat(segments_origin, results)
        print("le nombre d'intersections (= le nombre de points differents) est", len(set(results)))
        print("le nombre de coupes dans les segments est", len(results))

    for filename in sys.argv[1:]:
        segments_origin, results = test(filename, True)
        compute_x.cache_clear()
        tycat(segments_origin, results)
        print("le nombre d'intersections (= le nombre de points differents) est", len(set(results)))
        print("le nombre de coupes dans les segments est", len(results))

if __name__ == '__main__':
    main()
