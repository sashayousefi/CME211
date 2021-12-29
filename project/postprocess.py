import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os 
import sys 
"""
Program for plotting the psuedocolor plot of the temperature distribution
within the pipe wall. Our plot also overlays the mean temperature isoline. 
In this program, we attain matrix attributes (such as temperatures of the
isothermal boundaries and matrix size) by reading in the input file. 
We also attain the temperature at each point in the grid by reading 
in the matrix values from the solution files. From there, we use 
the pcolormesh function from matplotlib to plot our heat map. Additionally,
we overlay the plot with the mean temperature isoline. We compute the
coordinates of the isoline by using a 1D linear interpolation along
the width of the domain. Finally, we save the figures and print 
the corresponding mean. 
"""
#usage error for insufficient conditions
if len(sys.argv) != 3: 
    print("Usage:\n $ python3 postprocess.py <inputfile>" \
        " <solutionfile>")
    sys.exit(1)

input_file = sys.argv[1]
solution_file = sys.argv[2]

#reading in temperature values in the pipe wall from the solution file
try:
    isoline_df = np.genfromtxt(solution_file, delimiter = " ", dtype = np.float64)
    isoline_df = np.flipud(isoline_df)
except IOError:
    raise RuntimeError("Invalid solution file")

#reading in matrix attributes from the input file
try:
    inputdf1 = np.genfromtxt(input_file, max_rows = 1, delimiter = " ", 
        dtype = np.float64)
    inputdf2 = np.genfromtxt(input_file, skip_header = 1, delimiter = " ", 
        dtype = np.float64)
except IOError:
    raise RuntimeError("Invalid input file")

length, width, h = inputdf1
Tc, Th = inputdf2
nx = int(length/h) + 1
ny = int(width/h) + 1

#getting the mean temperature for the isoline
mean = isoline_df.mean() 

#getting the axes for the plot 
x = np.linspace(0, length, nx)
y = np.linspace(0, width, ny)
X, Y = np.meshgrid(x, y)

#computing the coordinates of the isoline
interp_vals = np.array([])
for i in np.arange(nx):
    col_vals = isoline_df[:, i]
    interp_vals = np.append(interp_vals, np.interp(mean, col_vals, y)) 
    
#function to plot/format the isoline and psuedocolor plots
def plot_fig(solution_file):        
    plt.figure()
    plt.pcolormesh(x, y, isoline_df, cmap = 'jet') 
    plt.colorbar()
    plt.xlim(0, length);
    plt.ylim(min(y) - 0.2, max(y) + 0.2)
    plt.plot(x,interp_vals, color = 'black')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(os.path.splitext(solution_file)[0] + "plot.png")

plot_fig(solution_file)
print("Input file processed: {}".format(input_file))
print("Mean Temperature: {:.5f}".format(mean))


