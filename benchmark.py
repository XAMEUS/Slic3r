#!/usr/bin/env python3
"""
A simple benchmark
"""
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import alt
import bruteforce
import bo

def mini_bench(fun, arg_file):
    """
    Run a mini benchmark 10 times, return statistics
    """
    time_bench, ecart, tmp = None, None, [0 for _ in range(10)]
    timer = -time.time()
    for i in range(10):
        fun.test(arg_file, False)
        tmp[i] = time.time()
    time_bench = (timer + tmp[-1]) / 10

    for i in range(9, 0, -1):
        tmp[i] -= tmp[i-1]
    tmp[0] += timer
    ecart = (sum([(i - time_bench)**2 for i in tmp]))**(1/2)
    return time_bench, ecart

def main():
    """
    Run benchmark
    """
    time_alt = []
    time_bruteforce = []
    time_bo = []
    ecart_alt = []
    ecart_bruteforce = []
    ecart_bo = []

    for arg_file in sys.argv[1:]:
        res = mini_bench(alt, arg_file)
        time_alt.append(res[0])
        ecart_alt.append(res[1])

        res = mini_bench(bruteforce, arg_file)
        time_bruteforce.append(res[0])
        ecart_bruteforce.append(res[1])

        res = mini_bench(bo, arg_file)
        time_bo.append(res[0])
        ecart_bo.append(res[1])

    ind = np.arange(len(time_alt))    # the x locations for the groups
    width = 0.2       # the width of the bars: can also be len(x) sequence

    data_1 = plt.bar(ind-width, time_alt, width, color='green', yerr=ecart_alt)
    data_2 = plt.bar(ind, time_bruteforce, width, color='blue', yerr=ecart_bruteforce)
    data_3 = plt.bar(ind+width, time_bo, width, color='red', yerr=ecart_bo)

    plt.ylabel('Temps')
    plt.xticks(ind, [i.split("/")[-1] for i in sys.argv[1:]])
    plt.legend((data_1[0], data_2[0], data_3[0]), ('Alt', 'Bruteforce', 'Bo'))
    plt.show()



if __name__ == '__main__':
    main()
