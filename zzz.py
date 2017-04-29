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

DEBUG = False
ENTER = False
MORE = False
STOP = []

def load_events(segments_origin, events, dict_seg):
    """
    Load all events
    """
    for segment in segments_origin: #On ajoute les événements adéquats
        pt_min, pt_max = min(segment.endpoints), max(segment.endpoints)
        if pt_min not in dict_seg:
            heappush(events, pt_min)
            dict_seg[pt_min] = [set(), set()]
        dict_seg[pt_min][0].add(segment)
        if pt_max not in dict_seg:
            heappush(events, pt_max)
            dict_seg[pt_max] = [set(), set()]
        dict_seg[pt_max][1].add(segment)

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
    load_events(segments_origin, events, dict_seg)

    count = 0

    while events: #Traitement des événements
        count += 1
        print(count)
        current = heappop(events) #On récupère le point à traiter
        segments = dict_seg[current] #On récupèrer ses segments associés (in, out)
        if DEBUG or count in STOP:
            print("Current:", current, segments)
            print("Events:", events)
            print("SL:", len(sweep), sweep)
            tycat(segments_origin, results, current, sweep, segments[0], segments[1])
            print("###############")

        if segments[1]: #On traite les out
            while segments[1]:
                segment = segments[1].pop()
                # DEBUG
                if MORE or count in STOP:
                    print("{")
                    for s in sweep: # AFFICHE LES COUPLES (KEY, SEGMENT)
                        print("\t-", key(s, current), s)
                    print("}")
                # END DEBUG
                i = sweep.index(segment)
                left, right = i - 1, i + 1
                if left >= 0 and right < len(sweep):
                    left, right = sweep[left], sweep[right]
                    intrsctn = left.intersection_with(right)
                    if intrsctn:
                        intrsctn = adjuster.hash_point(intrsctn)
                    if intrsctn and intrsctn not in results: # Intersection non-nulle et nouvelle
                        results.append(intrsctn)
                        if intrsctn not in dict_seg:
                            heappush(events, intrsctn)
                            dict_seg[intrsctn] = [set(), set()]
                        tmp = dict_seg[intrsctn]
                        tmp[0].add(left)
                        tmp[1].add(left)
                        tmp[0].add(right)
                        tmp[1].add(right)
                sweep.remove(segment)
                if MORE or count in STOP:
                    tycat(segments_origin, results, current, sweep, segment)

        if MORE or count in STOP:
            print("###### IN", current)
        Segment.point = current #On actualise le point: pt de référence

        if segments[0]: #On traite les in
            while segments[0]:
                segment = segments[0].pop()
                sweep.add(segment)
                # DEBUG
                if MORE or count in STOP:
                    print("{")
                    for s in sweep:
                        print("\t-", key(s, current), s)
                    print("}")
                i = sweep.index(segment)
                # END DEBUG

                #On traite à gauche
                left = i - 1
                if left >= 0:
                    left = sweep[left]
                    intrsctn = segment.intersection_with(left)
                    if intrsctn:
                        intrsctn = adjuster.hash_point(intrsctn)
                    if intrsctn and intrsctn not in results: # Intersection non-nulle et nouvelle
                        results.append(intrsctn)
                        if intrsctn not in dict_seg:
                            heappush(events, intrsctn)
                            dict_seg[intrsctn] = [set(), set()]
                        tmp = dict_seg[intrsctn]
                        tmp[0].add(segment)
                        tmp[1].add(segment)
                        tmp[0].add(left)
                        tmp[1].add(left)

                #Idem à droite
                right = i + 1
                if right < len(sweep):
                    right = sweep[right]
                    intrsctn = segment.intersection_with(right)
                    if intrsctn:
                        intrsctn = adjuster.hash_point(intrsctn)
                    if intrsctn and intrsctn not in results:
                        results.append(intrsctn)
                        if intrsctn not in dict_seg:
                            heappush(events, intrsctn)
                            dict_seg[intrsctn] = [set(), set()]
                        tmp = dict_seg[intrsctn]
                        tmp[0].add(segment)
                        tmp[1].add(segment)
                        tmp[0].add(right)
                        tmp[1].add(right)
                if MORE or count in STOP:
                    tycat(segments_origin, results, current, sweep, segment)

        if DEBUG or count in STOP:
            print("Current:", current, segments)
            print("Events:", events)
            print("SL:", len(sweep), sweep)
            print(results)
            tycat(segments_origin, results, current, sweep)
        if ENTER:
            input("Press [ENTER] to continue...\n")
    tycat(segments_origin, results)
    if ENTER:
        input("Press [ENTER] to continue...\n")
    # print("le nombre d'intersections (= le nombre de points differents) est", len(results))
    # print("le nombre de coupes dans les segments est", nb_coupes)

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
