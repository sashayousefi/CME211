import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.linalg
from scipy.sparse import csr_matrix
from scipy.sparse import linalg
import warnings

"""
Truss Class: a collection of different methods calculating the forces 
acting on a truss, which is defined as a rigid figure made up of beams that are
joined by frictionless pins. In this class, we know the orientation of the 
beams and the external forces acting on the beams. We then calculate the 
compression force for each beam as well as the reaction force on the 
beams due to the fixed supports using a system of linear equations. 

This project would be of interest to someone studying truss geometry
and forces acting on beams in these figures. 
"""
class Truss:
    def __init__(self, joints, beams, output_file = None):
        """
        Initializes all variables needed in the program. 
        This __init__ method takes in a joints file, beams file,
        and optional output file which saves the image of the truss.
        It stores each file, the beams dictionary (which matches 
        beam number to the joint indicies for the beam), a joints
        dictionary (which stores attributes like xy coordinates 
        and whether forces/fixed supports act on the joints),and a
        bx_coeffs and by_coeffs list, which stores the coefficients
        for the x and y components of the beams for the linear system.
        It also stores the resulting force vector from solving the system.
        Lastly, the init_method calls the run_function() function, 
        which runs the desires functions.
        """
        self.joints_file = os.path.join(os.getcwd(), joints)
        self.beams_file = os.path.join(os.getcwd(), beams)
        self.output_file = output_file
        self.beams_dict = {}
        self.joints_dict = {}
        self.count_fixed_support = 0
        self.bx_coeffs, self.by_coeffs, self.forces = [], [], []
        self.run_functions()

    def get_data(self):
        """
        This method reads our beams and joints file for the particular
        truss. It utilizes the beams and joints file initialized in the 
        init method, and parses the files to get data for each beam 
        and joint. The method adds the joint indicies as vals to beam key
        in the beams dictionary. Additionally, the method adds x,y coords, 
        external forces, and the existence of a fixed support as values 
        to the joint number key in the joints dictionary.
        """
        beams = np.loadtxt(self.beams_file, skiprows = 1, dtype = int)
        for beam in beams:
            self.beams_dict[beam[0]] = (beam[1], beam[2])
        joints = np.loadtxt(self.joints_file, skiprows = 1)
        for joint in joints:
            self.joints_dict[joint[0]] = (joint[1], joint[2], joint[3], \
                joint[4], joint[5])
            if joint[5] == 1:
                self.count_fixed_support += 1

    def get_beam_values(self):
        """
        This method calculates the coefficients for the components of force
        for each beam in the linear system. Appends x coefficients for each
        beam to the bx_coeffs list and y coefficients for each beam
        to the by_coeffs list. 
        """
        for beam, beam_val in self.beams_dict.items():
            Ja, Jb = beam_val
            Jax, Jay = self.joints_dict[Ja][0:2]
            Jbx, Jby = self.joints_dict[Jb][0:2]
            self.bx_coeffs.append((Jax - Jbx)/np.sqrt((Jax - Jbx)**2 \
                + (Jay - Jby)**2))
            self.by_coeffs.append((Jay - Jby)/np.sqrt((Jax - Jbx)**2 \
                + (Jay - Jby)**2))

    def create_matrix(self):
        """
        This method creates the sparse CSR data matrix with contains 
        data for our system of linear equations. As the method iterates
        through the joints, it attains the beam coefficient for that 
        particular component of the joint and stores it as a value 
        with row and column indiciess in the sparse matrix. Additionally, 
        the method adds a 1 for each x and y components for a fixed 
        point joint to adequately define the linear system. While iterating
        through pivots, I also create a cooresponding force vector,
        which stores the external forces. Now, I can solve the 
        system of linear equations since I have a system of 
        the form Ax = b, with A the sparse matrix and b the 
        force vector. Following the matrix and force vector
        creation, I apply the sparse linear package solver
        in scipy to solve the system of linear equations. I catch 
        errors if the system of linear equations is under/over determined
        or if the matrix is singular.    
        """
        force_vector = np.array([])
        joint_num = 1
        r_force_index = len(self.beams_dict)
        data, row, col = [], [], []
        while joint_num <= len(self.joints_dict):
            for beam, beam_val in self.beams_dict.items():
                if joint_num == beam_val[0]:
                    row.extend([2*joint_num-2, 2*joint_num-1])
                    col.extend([beam - 1, beam - 1])
                    data.extend([self.bx_coeffs[beam - 1],\
                        self.by_coeffs[beam - 1]])
                elif joint_num == beam_val[1]:
                    row.extend([2*joint_num - 2, 2*joint_num - 1])
                    col.extend([beam - 1, beam - 1])
                    data.extend([-self.bx_coeffs[beam - 1],\
                        -self.by_coeffs[beam - 1]])

            if self.joints_dict[joint_num][4] == 1:
                col.extend([r_force_index, r_force_index + 1])
                row.extend([2*joint_num-2, 2*joint_num -1])
                data.extend([1, 1])
                r_force_index += 2

            force_vector = np.append(force_vector, [-1*self.joints_dict\
                [joint_num][2], -1*self.joints_dict[joint_num][3]])
            joint_num += 1

        data_matrix = csr_matrix((data, (row, col)))
        shape = np.shape(data_matrix.toarray())
        if shape[0] != shape[1]:
            str_1="Truss geometry not suitable for static equilbrium analysis"
            raise RuntimeError(str_1)
        force_vector = np.array(force_vector)
        warnings.filterwarnings('error', category=scipy.sparse.linalg.dsolve.\
            linsolve.MatrixRankWarning)       
        try:   
            self.forces = scipy.sparse.linalg.spsolve(data_matrix, force_vector)
        except:
            str_2 = "Cannot solve the linear system, unstable truss?"
            raise RuntimeError(str_2) from None


    def PlotGeometry(self, saved_image):
        """
        Plots the geometry for the truss. Only invoked if the user provides 
        an output file for the image. The input is the filename for the 
        saved image. The method then uses the matplotlib module to plot 
        the geometry of the plot based on the orientation for the joints 
        for each beam. The image is then stored and saved in the output
        file.
        """
        for beam in self.beams_dict.values():
            joint_a_idx = beam[0]
            joint_b_idx =  beam[1]
            joint_a_x = self.joints_dict[joint_a_idx][0]
            joint_a_y = self.joints_dict[joint_a_idx][1]
            joint_b_x = self.joints_dict[joint_b_idx][0]
            joint_b_y = self.joints_dict[joint_b_idx][1] 
            plt.plot([joint_a_x, joint_b_x], [joint_a_y, joint_b_y], 'b')
        (bottom, top) = plt.ylim()
        plt.ylim(bottom-0.6, top+0.6)
        plt.savefig(saved_image)

    def __repr__(self):
        """
        Method that returns the string to be printed as invoked by 
        main.py. Properly formats the beam number and force values.
        The output we expect is im a tabular format.
        """
        main_str = ''
        main_str += ' Beam       Force\n'
        main_str += '-----------------\n'
        for beam in self.beams_dict.keys():
            main_str+=('{:5d}      {: 5.3f}\n')\
                .format(beam,self.forces[beam - 1])
        return main_str

    def run_functions(self):
        """
        Method invoked by the init method. Runs necessary functions to 
        obtain beam forces and plot truss geometry (if applicable). 
        The plot_geometry function is only run if the user provides 
        an output file for the image.
        """
        self.get_data()
        self.get_beam_values()
        self.create_matrix()
        if self.output_file:
            self.PlotGeometry(self.output_file)

