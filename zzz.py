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

def intersect_process(intrsctn, results, dict_seg, events, to_add):
    """
    When we have a intersection
    """
    if intrsctn not in results: # Intersection non-nulle et nouvelle
        results.append(intrsctn)
        n_inter = intrsctn.copy()
        n_inter.coordinates[0] = float("inf")
        print(n_inter, intrsctn)
        if n_inter not in dict_seg:
            heappush(events, n_inter)
            dict_seg[n_inter] = [set(), set()]
        tmp = dict_seg[n_inter]
        for elem in to_add:
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
                    for tmp in sweep: # AFFICHE LES COUPLES (KEY, SEGMENT)
                        print("\t-", key(tmp, current), tmp)
                    print("}")
                # END DEBUG
                i = sweep.index(segment)
                left, right = i - 1, i + 1
                if left >= 0 and right < len(sweep):
                    left, right = sweep[left], sweep[right]
                    intrsctn = left.intersection_with(right)
                    if intrsctn:
                        intrsctn = adjuster.hash_point(intrsctn)
                        intersect_process(intrsctn, results, dict_seg, events, [left, right])
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
                    for tmp in sweep:
                        print("\t-", key(tmp, current), tmp)
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
                        intersect_process(intrsctn, results, dict_seg, events, [segment, left])

                #Idem à droite
                right = i + 1
                if right < len(sweep):
                    right = sweep[right]
                    intrsctn = segment.intersection_with(right)
                    if intrsctn:
                        intrsctn = adjuster.hash_point(intrsctn)
                        intersect_process(intrsctn, results, dict_seg, events, [segment, right])
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
