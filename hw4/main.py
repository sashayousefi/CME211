import sys
import truss 
"""
main class which instantiates our truss object
and runs the necessary functions to find compression
forces
"""

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print('Usage:')
    print('  python3 main.py [joints file] [beams file]'+ \
    ' [optional plot output file]')
    sys.exit(0)

joints_file = sys.argv[1]
beams_file = sys.argv[2]

if len(sys.argv) == 4:
    output_file = sys.argv[3]

if len(sys.argv) == 3:
    t = truss.Truss(joints_file, beams_file)
elif len(sys.argv) == 4:
     t = truss.Truss(joints_file, beams_file, output_file)

print(t)
