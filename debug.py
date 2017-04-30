"""
DEBUG MODULE
"""

from geo.segment import key

def debug_print(data, debug=True, pause=False):
    """
    PRINT
    """
    if debug:
        print(*data)
    if pause:
        input("[PAUSE] : debug_print - Press [ENTER] to continue\n")

def debug_sweep(sweep, current, debug=True, pause=False):
    """
    DEBUG SWEEP
    """
    if debug:
        print("{")
        index = 0
        for tmp in sweep:
            print("\t.", index, " - ", key(tmp, current), tmp)
            index += 1
        print("}")
    if pause:
        input("[PAUSE] : debug_sweep - Press [ENTER] to continue\n")

def debug_pause(msg="", pause=True):
    """
    PAUSE
    """
    if pause:
        if msg:
            print(msg)
        input("[PAUSE] : Press [ENTER] to continue\n")
