import time
import sys
import random

try:
    #initialize variables from the command line
    ref_file = sys.argv[1]
    read_file = sys.argv[2]
    align_file = sys.argv[3]
except IndexError:
    #printing usage error and exit if incorrect input numbers
    print("Usage:\n $ python3 generatedata.py <ref_file>" \
         " <reads_file> <align_file>")
    sys.exit(1)

num_reads = 0
align_0 = 0
align_1 = 0
align_2 = 0

with open(align_file, 'w') as f:
    with open(ref_file, 'r') as ref:
        #reading the reference genome
        ref_str = ref.readline().strip()
        with open(read_file, 'r') as reads:
            time1 = time.time()
            while True:
                #reading the individual reads line by line. Checking if
                #if the read aligns to 1, 2, or no regions of the ref
                #genome.
                seq = reads.readline().strip()
                if not seq:
                    #break once it encounters an empty line
                    break;
                num_reads += 1
                #finding the 1st or 2nd matches (if they exist)
                first_match = ref_str.find(seq)
                second_match = ref_str.find(seq, \
                    first_match+1, len(ref_str))
                if first_match == -1:
                   #writing string with no matches to alignment file
                   to_write = "{} {}".format(seq, first_match)
                   align_0 += 1
                elif second_match == -1:
                   #writing string with one match to alignment file
                   to_write = "{} {}".format(seq, first_match)
                   align_1 += 1
                else:
                   #writing string with two matches to alignment file
                   to_write = "{} {} {}".format(seq, first_match,\
                        second_match)
                   align_2 += 1
                f.write(to_write + '\n')
            time2 = time.time()
            reads.close()
        ref.close()
f.close()

#printing relevant variables and ratios 
print("reference length: {}".format(len(ref_str)))
print("number reads: {}".format(num_reads))
for num, align in enumerate([align_0/num_reads, \
    align_1/num_reads, align_2/num_reads]):
    print("aligns {}: {}".format(num,align))
print("elapsed time: {}".format(time2 - time1))

