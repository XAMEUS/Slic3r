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
from geo.segment import load_segments, load_segments_stdin, Segment, key
from debug import debug_sweep, debug_print, debug_pause

DEBUG = False
PAUSE = False
MORE = False
STOP = []

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
            results.append(pt_min)
        if pt_max not in dict_seg:
            heappush(events, pt_max)
            dict_seg[pt_max] = [set(), set()]
        dict_seg[pt_max][1].add(segment)
        if (dict_seg[pt_max][0] and dict_seg[pt_max][1]) or \
           len(dict_seg[pt_max][0]) > 1 or \
           len(dict_seg[pt_max][1]) > 1:
            results.append(pt_max)
        if len(dict_seg[pt_min][0]) > 1 or len(dict_seg[pt_min][1]) > 1:
            results.append(pt_min)

def load_file(filename):
    """
    Load file
    """
    if filename is not None:
        adjuster, segments_origin = load_segments(filename)
    else:
        adjuster, segments_origin = load_segments_stdin()
    tycat(segments_origin)
    return adjuster, segments_origin

def test_intersect(results, dict_seg, events, adjuster, current, order):
    """
    Have we a intersection ? If yes, we do the necessary
    """
    intrsctn = order[0].intersection_with(order[1])
    if intrsctn and intrsctn != current:
        intrsctn = adjuster.hash_point(intrsctn)
        if intrsctn not in results: # Intersection non-nulle et nouvelle
            results.append(intrsctn)
            if intrsctn not in dict_seg:
                heappush(events, intrsctn)
                dict_seg[intrsctn] = [set(), set()]
            tmp = dict_seg[intrsctn]
            for elem in order:
                if elem not in tmp[1]:
                    tmp[0].add(elem)
                tmp[1].add(elem)

def test(filename):
    """
    run bentley ottmann
    """
    events = [] #Tas des événements: (point)
    dict_seg = {} #Dictionnaire contenant les segments (in, out) au point en arg
    sweep = SortedList() #(Sorted)List des segments en vie
    results = [] #Les points finaux

    adjuster, segments_origin = load_file(filename)
    Segment.adjuster = adjuster
    load_events(segments_origin, events, dict_seg, results)

    count = 0

    while events: #Traitement des événements
        count += 1
        # debug_print(("ITER:", count))
        current = heappop(events) #On récupère le point à traiter
        segments = dict_seg[current] #On récupèrer ses segments associés (in, out)
        if DEBUG or count in STOP:
            # print("Events:", events)
            # print("SL:", len(sweep), sweep)
            tycat(segments_origin, results, current, sweep, segments[0], segments[1])
            print("###############")
            print("Current:", current, segments)
            print("###############")

        if segments[1]: #On traite les out
            while segments[1]:
                segment = segments[1].pop()


                if MORE or count in STOP:
                    tycat(segments_origin, results, current, sweep, segment)
                debug_print(("DO : OUT", segment), DEBUG)
                i = sweep.bisect_left(segment)

                # DEBUG
                debug_print(("on cherche", key(segment, current), segment), DEBUG)
                debug_print(("default i =", i), DEBUG)
                debug_sweep(sweep, current, DEBUG, PAUSE)
                # END DEBUG

                if sweep[i] != segment and i < len(sweep)-1:
                    for i, tmp in enumerate(sweep):
                        if tmp == segment:
                            debug_print(("real i =", i), DEBUG)
                            debug_pause(pause=PAUSE)
                            break
                left = i-1-(i > 1 and key(sweep[i-1], current) == key(segment, current))
                right = i+1+(i < len(sweep)-1 and key(sweep[i+1], current) == key(segment, current))

                debug_print(("default i =", i), DEBUG)
                if left >= 0 and right < len(sweep):
                    test_intersect(results, dict_seg, events, adjuster, current,
                                   [sweep[left], sweep[right]])

                # DEBUG
                debug_print(("del i =", i), DEBUG)
                debug_sweep(sweep, current, DEBUG, PAUSE)
                # END DEBUG
                del sweep[i]
                # DEBUG
                debug_sweep(sweep, current, DEBUG, PAUSE)
                # END DEBUG

        if MORE or count in STOP:
            print("###### IN", current)
        Segment.point = current #On actualise le point: pt de référence

        if segments[0]: #On traite les in
            while segments[0]:
                #print(segments[0])
                segment = segments[0].pop()
                #print(segments[0])
                if MORE or count in STOP:
                    tycat(segments_origin, results, current, sweep, segment)
                debug_print(("DO : IN", segment), DEBUG)
                sweep.add(segment)
                debug_sweep(sweep, current, DEBUG, PAUSE)
                debug_print(("add", segment), DEBUG)
                i = sweep.bisect_left(segment)
                # DEBUG
                debug_print(("on cherche", key(segment, current), segment), DEBUG)
                debug_print(("default i =", i), DEBUG)
                debug_sweep(sweep, current, DEBUG, PAUSE)
                # END DEBUG


                if sweep[i] != segment and i < len(sweep)-1:
                    for i, tmp in enumerate(sweep):
                        if tmp == segment:
                            debug_print(("real i =", i), DEBUG)
                            debug_pause(pause=PAUSE)
                            break
                left = i-1-(i > 1 and key(sweep[i-1], current) == key(segment, current))
                right = i+1+(i < len(sweep)-1 and key(sweep[i+1], current) == key(segment, current))

                debug_print(("left:", left, ", right:", right), DEBUG)
                #On traite à gauche
                if left >= 0:
                    test_intersect(results, dict_seg, events, adjuster, current,
                                   [segment, sweep[left]])

                #Idem à droite
                if right < len(sweep):
                    test_intersect(results, dict_seg, events, adjuster, current,
                                   [segment, sweep[right]])
                #print(segments[0])

        if DEBUG or count in STOP:
            # print("Events:", events)
            # print("SL:", len(sweep), sweep)
            print("############### END WHILE")
            print("Current:", current, segments)
            tycat(segments_origin, results, current, sweep)
        if PAUSE:
            input("Press [ENTER] to continue...\n")
    tycat(segments_origin, results)
    if PAUSE:
        input("Press [ENTER] to continue...\n")
    print("le nombre d'intersections (= le nombre de points differents) est", len(set(results)))
    print("le nombre de coupes dans les segments est", len(results))

def main():
    """
    launch test on each file.
    """
    if len(sys.argv) == 1:
        test(None)
    for filename in sys.argv[1:]:
        test(filename)

if __name__ == '__main__':
    main()
