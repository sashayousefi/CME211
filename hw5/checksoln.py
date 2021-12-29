import sys
import numpy as np

#checks that the proper number of arguments are given
if len(sys.argv) != 3:
    print('Usage:')
    print('  python checksoln.py <maze file> <solution file>')
    sys.exit(0)
else:
    input_file = sys.argv[1]
    solution_file = sys.argv[2]

#reads the coordinates of the maze and the solution found by the c++ code
maze = np.loadtxt(input_file, dtype = int)
solution = np.loadtxt(solution_file, dtype = int)
dim = maze[0]
maze = maze[1:]

"""
Creates a dictionary of maze walls, which stores the row coordinates as
keys and the column coordinates of values. We can check the existance 
of a wall at a particular coordinate by using this dictionary.
"""
maze_wall_dict = {}
for row in np.arange(dim[0]):
    maze_wall_dict[row] = [i[1] for i in maze if i[0] == row]

for col in np.arange(dim[1]):
    if col not in maze_wall_dict[0]:
        entrance_col = col

def check_solution():
    """
    Checks whether a solution is valid by checking if the solution
    properly entered the maze on the first row, that each position
    change is valid (i.e. we move one position at a time, don't 
    go through a wall, and stay within the bounds of the maze), and
    checks that we exit the maze on the last row
    """
    #check if entrance col is correct and entrance row is 0
    if (solution[0][1] != entrance_col) or (solution[0][0] != 0):
        return "Solution is invalid"
    #check that each position change is valid (+/- 1)
    soln_sum = entrance_col
    for move in solution[1:]: 
        curr_sum = move[0] + move[1]
        if np.abs(curr_sum - soln_sum) != 1:
            return "Solution is invalid"
        soln_sum = curr_sum
        #check that you haven't run into a wall 
        if move[1] in maze_wall_dict[move[0]]:
            return "Solution is invalid"
        #check that the move is within bounds
        if move[0] >= dim[0] or move[1] >= dim[1]:
            return "Solution is invalid"
    #checks that we exit on the last column
    if solution[len(solution)- 1][0] != dim[0] - 1:
        return "Solution is invalid"
    #return valid if all checks pass
    return "Solution is valid!"

validity = check_solution()
print(validity)         
