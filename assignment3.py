#!/usr/bin/env python3
# student number

import sys
import textwrap
from mygff import *
import matplotlib.pyplot as plt
import numpy as np

# placeholder
def win_size():
    return 50

# i was unable to get this to work as one function
# so i did it separately
# firstly, get windows from sequence
def get_windows(seq):
    for i in range(0, len(seq) - win_size() + 1): # ensuring space for last window
        window = seq[i:i + win_size()]
        yield window # returning sequence of windows to be then iterated through

def main():

    gff_file, seq_file = sys.argv[1:]

    with open(seq_file, 'r') as fasta:

        seq = parse_fasta(fasta)
        gff_details = parse_gff(gff_file)
        sequences = extract_orfs(gff_details, seq)

        # secondly, calculate gc proportion per window per gene
        for k, v in sequences.items():
            x = [] # im going crazy! i don't know how to define the nucleotide position.
            y = []
            for window in get_windows(v):
                gc_proportion = (window.count("g") + window.count("c")) / len(window)
                y.append(gc_proportion) # y-axis point to plot on graph
            plt.figure()
            plt.plot(x,y)
            plt.title(k)
            plt.xlabel("nucleotide position")
            plt.ylabel("gc proportion")
            plt.show()

if __name__ == "__main__":

    # if len(sys.argv) != 3:
    #     sys.exit("ERROR: Incorrect number of arguments used. Run the script as 'python assignment3.py <.gff file> <.fasta file>")

    main()
