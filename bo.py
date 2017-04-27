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
from geo.segment import load_segments
from geo.tycat import tycat
from heapq import heappush, heappop
from sortedcontainers import SortedList

def test(filename):
    """
    run bentley ottmann
    """
    events = [] #Tas des événements: (point, type_d_evenement)
    d = {} #Dictionnaire contenant les segments au point (point, type_d_evenement)
    sweep = SortedList() #(Sorted)List des segments en vie

    adjuster, segments = load_segments(filename)
    tycat(segments)

    for segment in segments: #On ajoute les événements adéquats
        a, b = min(segment.endpoints), max(segment.endpoints)
        heappush(events, (a, "in"))
        heappush(events, (b, "out"))
        d[(a, "in")] = segment
        d[(b, "out")] = segment

    while events: #Traitement des événements
        current, status = heappop(events)
        segment = d[(current, status)]
        if status == "in":
            sweep.add(segment)
            i = sweep.index(segment)
            left = i-1
            if left >= 0:
                intrsctn = segment.intersection_with(left)
                if intrsctn:
                    intrsctn
                events.add((intrsctn, "x"))
                d[(intrsctn, "x")] = [left, segment]
        elif status == "out":
            pass
        else:
            pass
        tycat(segments, current) #TODO: liste des segments en vie
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
    for filename in sys.argv[1:]:
        test(filename)

main()
