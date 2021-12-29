import random
import sys

try:
    #initializing variables from the command line
    ref_len = int(sys.argv[1])
    num_reads = int(sys.argv[2])
    read_len = int(sys.argv[3])
    ref_file = sys.argv[4]
    read_file = sys.argv[5]
except IndexError:
    #printing usage error and exit if incorrect input numbers
    print("Usage:\n $ python3 generatedata.py <ref_length>" \
         " <nreads> <read_len> <ref_file> <reads_file>")
    sys.exit(1)

with open(ref_file, 'w') as ref_file:
    #creating the reference genome
    rand_len = round(.75*ref_len)
    ref = ""
    #randomly generating the first 75% of the ref genome
    for i in range(rand_len):
        base = random.randint(0,3)
        #assigning randomly generated integers from 0-3 to their
        #respective base
        if base == 0:
            base = "A"
        elif base == 1:
            base = "T"
        elif base == 2:
            base = "G"
        else:
            base = "C"
        ref += base
    #copying the latter 25% of the ref genome to complete the ref
    #this allows for double alignment for a number of reads
    copy_25 = ref[int(.5*ref_len): int(.75*ref_len)]
    ref += copy_25
    ref_file.write(ref)
ref_file.close()
ref_genome = ref

with open(read_file, 'w') as g:
    #initializing counts for the number of alignments per read
    iterator = 0
    align_0 = 0
    align_1 = 0
    align_2 = 0
    #generating random reads by randomly choosing an value from 0 to 1
    #assigning that value to an interval, and randomly picking a starting
    #point from within the assigned interval
    while iterator < num_reads:
        interval = random.random()
        #if clause determines which interval we choose our starting
        #value from
        if interval >= 0.15 and interval < 0.9:
            #generating read with one alignment in this interval.
            #string generated from the first randomly generated
            #50% of the reference. This ensures only one match.
            starting_val = random.randint(0,ref_len * 0.5)
            read = ref_genome[starting_val : starting_val + read_len]
            align_1 += 1
            g.write(read + '\n')
        elif interval >=0.9 and interval < 1:
            #generating read with two alignments in this interval.
            #string generated from the last copied 75% of the ref.
            #this ensures two matches since the 50-75% and 75-100%
            #intervals are identical.
            starting_val = random.randint(ref_len * 0.75,\
                ref_len - read_len)
            read = ref_genome[starting_val : starting_val + read_len]
            align_2 += 1
            g.write(read + '\n')
        else:
            #no alignments in this interval. reads are randomly generated
            #and checked against the ref to ensure no matches.
            while True:
                null_read = ''
                for i in range(read_len):
                     base = random.randint(0,3)
                     if base == 0:
                          base = "A"
                     elif base == 1:
                          base = "T"
                     elif base == 2:
                          base = "G"
                     else:
                          base = "C"
                     null_read += base
                if ref_genome.find(null_read) == -1:
                    break;
            align_0 += 1
            g.write(null_read + '\n')
        iterator += 1
g.close()

#printing relevant vaues and proportions
print("reference length: {}".format(ref_len))
print("number reads: {}".format(num_reads))
print("read length: {}".format(read_len))
for num, align in enumerate([align_0/num_reads,\
     align_1/num_reads, align_2/num_reads]):
    print("aligns {}: {}".format(num,align))
