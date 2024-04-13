#!/usr/bin/env python3
# student number

import sys
import math
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
        id = 1 # placing the plots anticlockwise on the subplot grid
        for k, v in sequences.items():
            x = range(0,len(v) - win_size() + 1)
            y = []
            for window in get_windows(v):
                gc_proportion = (window.count("g") + window.count("c")) / len(window)
                y.append(gc_proportion) # y-axis point to plot on graph
            ax = plt.subplot(math.ceil(len(sequences)/4),4,id) # ensuring there are enough rows for the plot
            ax.plot(x,y)
            # decoration, formatting
            ax.set_title(k)
            ax.axhline(y=np.nanmean(y),color="red") # adding horizontal average line
            ax.set_xlabel("nucleotide position")
            ax.set_ylabel("gc proportion")
            id +=1
    
        plt.tight_layout() # so titles etc don't overlap
        plt.show()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.exit("ERROR: Incorrect number of arguments used. Run the script as 'python assignment3.py <.gff file> <.fasta file>")

    main()
