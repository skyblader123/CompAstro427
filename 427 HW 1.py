#!/usr/bin/env python

import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from sympy import limit, Symbol, cos

print "Question 1:"
print "1A:"
epsilon = 1
while (1 + 0.5**epsilon) != 1: 
    epsilonMax = 0.5**epsilon
    epsilon += 1
print "System's epsilon value: ", sys.float_info.epsilon #system's epsilon
print "Obtained maximum epsilon: ", epsilonMax
print

print "1B:"
while (1 - 0.5**epsilon) != 1:
    epsilonMin = 0.5**epsilon
    epsilon += 1  
print "Obtained minimum epsilon: ", epsilonMin
print

print "1C:"
start = 1
while (np.float32(1.99*2**start) < sys.float_info.max):
    maxValue = np.float32(1.99*2**start) #empirically largest value
    start += 1
    
print "Maximum value that can be obtained with single-precision: ", maxValue
print "System's representable maximum: ", sys.float_info.max
print

print "1D:"
while (np.float32(2**(-1*start)) > sys.float_info.min):
    minValue = np.float32(2**(-start)) #empirically smallest value
    start += 1
    
print "Minimum value that can be obtained with single-precision: ", minValue   
print "System's representable minimum: ", sys.float_info.min 
print

#sys.float_info.max and min are in np.float64
#can add extra bit to the last number in 1A, i.e. if the second last input only has
#like 6 decimal digits, so the system can still print out something much closer to the
#greatest/lowest value

question1 = '''
Using the float data type, the main reason for obtaining such significantly small numbers compared to the actual system max/min is because the lack in precision in determining the precision after the decimal point accumulates over large amounts of multiplication upto the point of the system max/min (which may be at least hundreds of multiplication). This is especially important for the values here, which are single-precision because the mantissa is only up to 7. Compared to double-precision in np.float64, it would have missed twice the amount of precision each time since the mantissa in np.float64 is 14. Futhermore, the number decreases in value because in the IEEE 754 standards, the base of the number becomes 10 rather than the computer's base of 2.
'''

#slight issue in description (i.e. it's not really an infinity problem but rather an accuracy issue)
print question1

print "Question 2:"
def function(x):
    product = (1-math.cos(x))/(x**2) #given function in question
    return product
    
print function(9e-7)," ",function(1e-7)," ", function(0.1e-7)

y = Symbol("x")
print limit((1-cos(y))/y**2,y,0)

XX = np.linspace(-0.1,5.,200,endpoint=True) #original function from -0.1 to 5
yay = (1-np.cos(XX))/(XX**2)
plt.plot(XX,yay,"ro")
plt.show()

XX2 = np.linspace(0,np.float(1e-7),200,endpoint=True) #function from 0 to 1e-7
yay2 = (1-np.cos(XX2))/(XX2**2)
plt.plot(XX2,yay2,"bo")
plt.show()

question2 = '''
The main difference between the numerical results computed above and the limit is that the limit is the expected value that will occur as the "'x'" value approaches, but not necessarily be at, zero. This is especially important for functions (i.e functions that cannot exist at certain values) that approach positive/negative infinity as these values of "'x'" do not exist at these values. However, the numerical values computed above is directly the result of the function when that certain value of x is inputted into the function, and is the direct result of the "'x'" for this f(x).
'''
print "The first graph with red spots is graph from -0.1 to 5 for comparison."
print
print "The second graph is from 0 to 0.0000001."
print question2

print "Question 3:"
hwfile = 'hw1.dat'
print "3A, Reading the",hwfile,"currently..."
print
def readFunction(f): 
#"reading function" that reads off the columns of the given file; omits first line
    a,b = np.loadtxt(f,usecols=[0,1],unpack=True) 
    return(a,b)
a,b = readFunction(hwfile)
print a
print b
print

print "3B:"
value = 4.75
interVal = np.interp(value,a,b)
print "Interpolated value at x = ",value,"is ",interVal
print

print "3C:"
def NevAlgorithm(a, b, points, value): #Neville's Algorithm
#points = number of points in data
#value = what we want interpolated
    p = [[0]*(points+1) for i in range (points+1)]
    for i in range(1,points+1): #better if I go from (0 to points)
    #could have written some from of a copy command like np.copy(b)
        p[i] = b[i] #setting up the array to print out values 
    for j in range(1,points):
        for i in range(1,points+1-j): #repeats for nth orders of polynomials determined by "points"
            p[i] = ((value-a[j+i])*p[i] + (a[i]-value)*p[i+1])/(a[i]-a[j+i])
    nevValue = p[1]
    return(nevValue)
    
nev = NevAlgorithm(a,b,4,4.75)
print nev
print

print "3D:"
def originalFunc(x):
    func = 100/(x**2)
    return func
print "Actual value at x=",value,"is equal to",originalFunc(value)
question3 = '''There is a much larger error margin for computing Neville's Algorithm 
because since the Algorithm is computed over the interpolation of the preceding points
that come before it (which also have its own error margins), the erros of these 
interpolations build up over several calculations, compared to the actual function and
the interpolated value within the given values (of our desired value).
'''
print question3

