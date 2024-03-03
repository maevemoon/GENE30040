#!/usr/bin/env python3
# student number

import sys
import math

# run the program as "python assignment1.py input.txt output_assignment1.txt"
infile = sys.argv[1]
outfile = sys.argv[2]

# functions for all problems
# INI2  
def hypotenuse(a,b):
    return math.sqrt(a**2 + b**2)

# INI3
def sliced_string(s,a,b,c,d):
    return s[a:b+1] + " " + s[c:d+1]

# INI4
def odd_sum(a,b):
    return sum([i for i in range(a,b) if i % 2 != 0])

# INI6
def word_count(s):
    counts = dict()
    # this problem doesn't work in this assignment because the input file is split into individual words, but it does work on any sentence input
    words = s.split()
    for i in words:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    return counts

# RNA
def transcribe(s): 
    # DNA -> RNA means thymine becomes uracil
    return s.replace("T", "U")

# DNA
def nucleotide_count(s):
    return "{} {} {} {}".format(s.count("A"), s.count("C"), s.count("G"), s.count("T"))

# driver code / main module
def main():
    with open(infile,'r') as fin, open(outfile,'w') as fout:
        # splitting data from input.txt
        # data.append(line.strip(),split("\t")) is a better option for splitting the data up, however i could not figure out how to locate specific inputs with it 
        data = fin.read().split()

        # locating inputs (unfortunately was unable to make this work for every instance of a specific problem's input, so it only works on the first)
        ini2_loc = data.index("##INI2")
        ini3_loc = data.index("##INI3")
        ini4_loc = data.index("##INI4") # this function will not work as intended - unfortunately was unable to join the split words into a sentence in between two sets of inputs in order to be split again
        ini6_loc = data.index("##INI6")
        rna_loc = data.index("##RNA")
        dna_loc = data.index("##DNA")

        # writing outputs to output_assignment1.txt
        # the input is the index of the problem + terms needed after it, translated into an integer if necessary for the function in question
        print("##INI2\n{}".format(hypotenuse(int(data[ini2_loc+1]),int(data[ini2_loc+2]))), file=fout)
        print("##INI3\n{}".format(sliced_string(data[ini3_loc+1],int(data[ini3_loc+2]),int(data[ini3_loc+3]),int(data[ini3_loc+4]),int(data[ini3_loc+5]))), file=fout)
        print("##INI4\n{}".format(odd_sum(int(data[ini4_loc+1]),int(data[ini4_loc+2]))), file=fout)
        print("##INI6\n{}".format(word_count(data[ini6_loc+1])), file=fout)
        print("##RNA\n{}".format(transcribe(data[rna_loc+1])), file=fout)
        print("##DNA\n{}".format(nucleotide_count(data[dna_loc+1])), file=fout)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
