"""
A simple benchmark
"""
import sys
import time
import matplotlib.pyplot as plt
import alt
import bruteforce
import algo


def main():
    """
    Run benchmark
    """
    time_alt = []
    time_bruteforce = []
    time_algo = []
    for arg_file in sys.argv[1:]:
        timer_alt = -time.time()
        for _ in range(10):
            alt.test(arg_file)
        time_alt.append(timer_alt + time.time())
        timer_bruteforce = -time.time()
        for _ in range(10):
            bruteforce.test(arg_file)
        time_bruteforce.append(timer_bruteforce + time.time())
        timer_algo = -time.time()
        for _ in range(10):
            algo.test(arg_file)
        time_algo.append(timer_algo + time.time())

    alt_plt = plt.scatter(range(len(time_alt)), time_alt, s=100, color="red")
    brut_plt = plt.scatter(range(len(time_bruteforce)), time_bruteforce, s=100, color="blue")
    algo_plt = plt.scatter(range(len(time_algo)), time_algo, s=100, color="green")

    plt.legend([alt_plt, brut_plt, algo_plt], ['Alt', 'Bruteforce', 'Algo'])
    plt.ylabel('Temps (*10 s)')
    plt.xlabel('Numéro Fichier')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
