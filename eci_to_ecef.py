# eci_to_ecef.py
#
# Usage:python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km
#  Converts coordinate transform from eci to ecef using JD conversion 

# Parameters:
# Y = year
# Mo = month
# D = day
# h = hour
# m = month
# s = second
# eci_x_km = eci x coord in km 
# eci_y_km = eci y coord in km
# eci_z_km = eci z coord in km

# Output:
#  Prints the position vector now in ECEF coord sys.
#
# 
# Written by Jack Rathert
# Other contributors: None

# Test Case Input: python3 eci_to_ecef.py 2054 4 29 11 29 3.3 5870.038832 3389.068500 3838.027968

# import Python modules
import sys 
from math import trunc, cos, sin, fmod, pi

class numpy_lite: # By the end of the semester I shall have finished development of numpy lite, every script will be 10,000 lines, and I shall be vindicated
    def matrix_mult(self,matrix1, matrix2):
        rowsA = len(matrix1)
        colsA = len(matrix1[0])
        rowsB = len(matrix2)
        colsB = len(matrix2[0])
        if colsA != rowsB:
            return "Cannot Multiply!"
        else:
            result = [[0 for row in range(colsB)] for col in range(rowsA)]
            for i in range(rowsA):
                for j in range(colsB):
                    for k in range(colsA):
                        result[i][j] += matrix1[i][k] * matrix2[k][j]
            return result
    def matrix_add(list1,list2):
        return [x+y for x,y in zip(list1, list2)]
    def matrix_sub(list1,list2):
       return [x-y for x,y in zip(list1,list2)]
    
## Should have let me use numpy man
npl = numpy_lite()

# constants 
omega = 7.292115e-5 # rad/s

# helper functions


# Convert Standard date to Julian Date
def date_to_JD(Y: int,Mo: int,D: int,h: int,m:int,s: float):

  JD = D - 32075 \
  +  int( 1461 * ( Y + 4800 +  int((Mo-14)/12) ) /4) \
  + int( 367 * ( Mo - 2 - (int((Mo-14)/12) *12 )) / 12) \
  - int( 3 * int(( Y + 4900 + int((Mo-14)/12)) /100 ) /4 )

  JDmidnight = (JD) - 0.5
  Dfrac = (s + 60*(m + 60*h))/86400
  JDfrac = JDmidnight + Dfrac

  return JDfrac

# Convert Julian Date to GMST in radians
def JD_to_GMSTang(JDfrac):
  TUT1 = (JDfrac-2451545.0)/36525

  theta_gmst_sec = 67310.54841 + (876600*60*60 + 8640184.812866)*TUT1 \
    + 0.093104*TUT1**2 \
    - 6.2e-6 * TUT1**3 # ouput in seconds?
  
  theta_rad = fmod(theta_gmst_sec%86400 * omega + 2*pi, 2*pi)
  return theta_rad

# Perform rotations on eci_vec
def Rz_Theta(theta, eci_vec):
  Rz = [ [ cos(-theta), -sin(-theta),0 ], [sin(-theta), cos(-theta), 0 ], [0,0,1] ]
  ans = npl.matrix_mult(Rz,eci_vec)
  return ans
    
# Main Function to Call
def eci_to_ecef(Y,Mo,D,h,m,s,x,y,z):
  eci_vec = [[x],[y],[z]]
  JDfrac = date_to_JD(Y,Mo,D,h,m,s)
  Theta_rad = JD_to_GMSTang(JDfrac)
  ecef_vec = Rz_Theta(Theta_rad, eci_vec)
  print(ecef_vec[0][0])
  print(ecef_vec[1][0])
  print(ecef_vec[2][0])

  return

# initialize script arguments
Y = int(0)
Mo = int(0)
D = int(0)
h = int(0)
m = int(0)
s = float('nan')
eci_x_km = float('nan')
eci_y_km = float('nan')
eci_z_km = float('nan')

# parse script arguments
if len(sys.argv)==10:
  Y = int(sys.argv[1])
  Mo = int(sys.argv[2])
  D = int(sys.argv[3])
  h = int(sys.argv[4])
  m = int(sys.argv[5])
  s = float(sys.argv[6])
  eci_x_km = float(sys.argv[7])
  eci_y_km = float(sys.argv[8])
  eci_z_km = float(sys.argv[9])
else:
  print(\
   'Usage: '\
   'python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'\
  )
  exit()

# write script below this line
eci_to_ecef(Y,Mo,D,h,m,s,eci_x_km,eci_y_km,eci_z_km)