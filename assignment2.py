#!/usr/bin/env python3
# student number

import sys

gff = sys.argv[1]
fasta = sys.argv[2]
codons = sys.argv[3]
outfile = sys.argv[4]

def main():

    with open(outfile, 'w') as fout:

        # Q1
        gff_data = []

        with open(gff,'r') as fin:

            fout.write("22206666")
            fout.write("\n\n##Q1\nName of the gene(s) found in the input .gff file encoding a hemagglutinin:\n")

            # parsing the header & columns
            header = fin.readline().strip().split("\t")
            for line in fin:
                columns = line.strip().split("\t")
                gff_data.append(columns)
        
            # finding "hemagglutination" in the "notes" column of the parsed file
            hg_loc = [] # list of locations where "hemaglutination" is mentioned
            for i, row in enumerate(gff_data):
                note = row[header.index("notes")] 
                if "hemagglutination" in note:
                    hg_loc.append((i))
                # Q2 code should be here for efficiency however to keep my assignment easy to track i've instead written it below

            # if no instances are found:
            if not hg_loc:
                fout.write("None")
            # otherwise find corresponding gene name(s) for every instance !
            for instance in hg_loc:
                fout.write(gff_data[instance][header.index("gene_name")]) # at (row number, corresponding "gene_name" entry)

        # Q2. assuming an "annotated gene" is one that has something other than "none" entered in the corresponding "notes" column
            count = 0
            for i, row in enumerate(gff_data):
                note = row[header.index("notes")]
                if not "none" in note:
                    count +=1
            
            fout.write("\n\n##Q2\n{}".format(count))

        # MAKE ALL OF THESE FUNCTIONS ! if you can

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit("ERROR: Incorrect number of arguments used. Run the script as 'python assignment2.py <gff file> <fasta file> <codon table> <output file>")

    main()
