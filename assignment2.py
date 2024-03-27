#!/usr/bin/env python3
# student number

import sys

gff = sys.argv[1]
fasta = sys.argv[2]
codons = sys.argv[3]
outfile = sys.argv[4]

# assuming codon table file will always be the same
codon_table = {}
with open(codons, 'r') as f:
    codon_header = f.readline().strip().split("\t")
    for line in f:
        columns = line.strip().split("\t")
        key = columns[0]
        value = columns[3]       
        codon_table[key] = value

def GffParser(file):
    global header # need for other gff functions 

    data = []
    with open(file) as f:
        # parsing the header & columns
        header = f.readline().strip().split("\t")
        for line in f:
            columns = line.strip().split("\t")
            data.append(columns)
    return data

def GffNoteFinder(file, term):
    locations = [] # list of locations where term is mentioned
    for i, row in enumerate(GffParser(file)):
        note = row[header.index("notes")] 
        if term in note:
            locations.append((i))
    # if no instances are found:
    if not locations:
        return "None"
    # otherwise find corresponding gene name(s) for every instance !
    for instance in locations:
        return GffParser(file)[instance][header.index("gene_name")] # at (row number, corresponding "gene_name" entry)

# assuming an "annotated gene" is one that has something other than "none" entered in the corresponding "notes" column
def GffAnnotatedCount(file):
    count = 0
    for i, row in enumerate(GffParser(file)):
        note = row[header.index("notes")]
        if not "none" in note:
            count +=1
    return str(count)

# this only parses one fasta entry which is what I initially thought was in the question
# def FastaParser(file):
#     with open(file) as f:
#         sequence = ""
#         for line in f:
#             if not line.startswith('>'):
#                 sequence += line.rstrip()
#     return sequence

# functions wouldn't work if i made headers, seqs global values, not sure why. so i have to call them spearately every time
def FastaParser(file):
    headers = []
    seqs = []
    with open(file) as f:
        sequence = ""
        header = None
        for line in f:
            # parsing header
            if line.startswith('>'):
                headers.append(line[1:-1])
                if header:
                    seqs.append(sequence)
                sequence = ""
                header = line[1:]
            # otherwise must be a sequence
            else:
                sequence += line.rstrip()
        seqs.append(sequence) # adding individual sequence to the list of all sequences
    return headers, seqs

def FastaTranslator(file):
    headers, seqs = FastaParser(file)
    translated_seqs = []
    for i in seqs:
        codons = (i[n:n+3] for n in range(0,len(i),3)) # defining a codon; 3 nucleotide reading frame
        protein_sequence = ""
        for codon in codons: 
            # if codon (uppercase to match dictionary) is a key in the codon table dictionary, add corresponding 1 letter code to protein sequence
            if codon.upper() in list(codon_table): 
                protein_sequence += codon_table.get(codon.upper())
        translated_seqs.append(protein_sequence)
    return translated_seqs

def CodonUsage(file):
    headers, seqs = FastaParser(file)
    codon_count = {}
    for i in seqs:
        codons = (i[n:n+3] for n in range(0,len(i),3)) # defining again; couldn't make it work using codons as a global variable
        for codon in codons:
            # if the codon is in the dictionary already, add to count. otherwise add it and count once
            if codon.upper() in list(codon_count):
                codon_count[codon.upper()] += 1
            else:
                codon_count[codon.upper()] = 1
    codon_usage = ""
    total = sum(codon_count.values())
    # for every entry in the codon count dictionary, add the codon, count, and proportion to the codon usage table
    for key, value in codon_count.items():
        codon_usage += (key + "\t" + str(value) + "\t" + str(round((value/total),2)) + "\n") # codon / count / proportion, tab-separated
    return codon_usage

def main():

    with open(outfile, 'w') as fout:
        fout.write("student number")

        # Q1.
        fout.write("\n\n##Q1\nName of the gene(s) found in the input .gff file encoding a hemagglutinin:\n")
        fout.write(GffNoteFinder(gff, "hemagglutination"))

        # Q2. 
        fout.write("\n\n##Q2\nNumber of annotated genes found in the input .gff file:\n")
        fout.write(GffAnnotatedCount(gff))

        # Q3. 
        fout.write("\n\n##Q3\nLength of and translation of sequences found in the input .fasta file:\n")

        headers, seqs = FastaParser(fasta)
        translated_seqs = FastaTranslator(fasta)

        # small issue here: if {translated_seqs[i]} is called here, it posts all translated sequences but only the first header + corresponding length.
        # however, if posted separately with a new for loop, then {translated_seqs[i]} joins every sequence together into one? not sure how to fix
        # i think the issue is with location of " protein_sequence = "" " in FastaTranslator but unsure
        for i in range(len(translated_seqs)):
            fout.write(f"{headers[i]}: length {str(len(seqs[i]))} nt\n{translated_seqs[i]}")

        # Q4. i wanted to use codon table dictionary but i couldn't figure out how to connect .fasta to it, so it's its own function
        fout.write("\n\n##Q4\nCodon Usage Table\n\n")
        fout.write(CodonUsage(fasta))

if __name__ == "__main__":

    if len(sys.argv) != 5:
        sys.exit("ERROR: Incorrect number of arguments used. Run the script as 'python assignment2.py <gff file> <fasta file> <codon table> <output file>")

    main()
