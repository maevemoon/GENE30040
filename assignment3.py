#!/usr/bin/env python3
# student number

import sys
import math
import mygff as a2
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

# there is a problem with this
# it infinitely asks for an input until you press Exit, in which case the result becomes None
# while messing around with this sometimes it worked fine sometimes it didn't, i ultimately don't know how to fix it
# everything works as it should with a placeholder though
def win_size():
    sg.theme('GreenMono')
    layout = [[sg.VPush()], # centering
              [sg.Push(), sg.Text('Sliding Window for GC Proportion',font=('Franklin Gothic Medium', 12, 'italic', 'bold')), sg.Push()], 
              [sg.Push(), sg.Text('Enter size of sliding window:'), sg.InputText(key='-IN-'), sg.Push()],
              [sg.Push(), sg.Button('CONFIRM',key='-confirm-'), sg.Button('EXIT'), sg.Push()], 
              [sg.VPush()]]
    window = sg.Window('Sliding Window', layout, size=(300,150))
    while True:
        event, values = window.read()
        print(values.get('-IN-'))
        if event == '-confirm-':
            result = values['-IN-']
            if result:
                return result
        elif event in ['Exit', sg.WIN_CLOSED]:
            break
    window.close()

# i was unable to get this to work as one function
# so i did it separately
# firstly, get windows from sequence
def get_windows(seq):
    for i in range(0, len(seq) - win_size() + 1): # ensuring space for last window
        window = seq[i:i + win_size()]
        yield window # returning sequence of windows to be then iterated through to plot

def main():

    gff_file, seq_file = sys.argv[1:]

    with open(seq_file, 'r') as fasta:

        # setting up
        seq = a2.parse_fasta(fasta)
        gff_details = a2.parse_gff(gff_file)
        sequences = a2.extract_orfs(gff_details, seq)

        # secondly, calculate gc proportion per window per gene
        id = 1 # first graph
        for k, v in sequences.items():
            x = range(0,len(v) - win_size() + 1) # nucleotide position
            y = [] # gc proportion
            for window in get_windows(v):
                gc_proportion = (window.count("g") + window.count("c")) / len(window)
                y.append(gc_proportion)
            ax = plt.subplot(math.ceil(len(sequences)/4),4,id) # ensuring there are enough rows
            ax.plot(x,y)

            # formatting
            ax.set_title(k)
            ax.axhline(y=np.nanmean(y),color="red") # gc proportion average line
            ax.set_xlabel("nucleotide position")
            ax.set_ylabel("gc proportion")

            id +=1 # placing plots anticlockwise
    
        plt.tight_layout() 
        plt.show()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.exit("ERROR: Incorrect number of arguments used. Run the script as 'python assignment3.py <.gff file> <.fasta file>")

    main()
