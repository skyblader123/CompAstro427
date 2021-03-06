### CODE TO HAND IN ###

import time
import numpy as np
import numpy.random as rd #numpy packaged random number generator
import matplotlib.pyplot as plt
#CUDA packages
import pycuda.tools
import pycuda.autoinit
import pycuda.gpuarray as gpuarray
import pycuda.curandom
import pycuda.cumath

#Definitions
Pi = np.pi
Sum = np.sum

print ("Question 1 - Using Monte-Carlo for computing Pi.")
print
print ("This is the value of Pi for comparison: ", Pi)

#calculates Pi within a circle of radius 1; repeats for n iterations if radius is not 1 during computation 
 
def randPi(n):
#n -> iterations to do; determines the array size returned
    countsCircle = 0.
    #represents the dots drawn in the circle within a domain of a (1x1 box)
    iterations = [] 
    #list for displaying number of iterations
    calculatedPi = [] 
    #list for inputting calculated Pi value
    errors = [] 
    #error value list for values computed in error function
    for i in range(0,n):
        i += 1
        radLength = np.sqrt(np.power(rd.rand(),2) + np.power(rd.rand(),2)) 
        #calculates radius of a random point
        if radLength <= 1.: 
            countsCircle += 1.
            iterations.append(i)   
            calculatedPi.append(4.*countsCircle/i)
            errors.append(np.sqrt(Sum(np.power(Pi - np.float64(calculatedPi[:]),2)/i)))
    return calculatedPi,iterations, errors

startTimeCPU = time.time()
calculatedPi1,iterations1, errors1= randPi(100)
endTimeCPU = time.time()

"Log-Log plot of number of iterations vs. error at each iteration; log is utilized to reduce scale."
plt.plot(iterations1,errors1,'bo')
plt.xscale('log')
plt.yscale('log')

print ("Time it took for CPU computation:")
print (endTimeCPU - startTimeCPU)

print ("This is the array of calculated Pi values:")
print (calculatedPi1)

print ("This is the array of calculated error:")
print (errors1)

print ("Question 2 - Using GPU to compute Pi.")
print
print ("This part of the code utilizes Python 3.5")

N = 100 #-> number of iterations we want to have
gpuRandom = pycuda.curandom.XORWOWRandomNumberGenerator(seed_getter=None) #provides a list of pseudo-random numbers

#the following are arrays of random values; "gen_uniform" creates objects of GPUArray of random numbers
x1 = gpuRandom.gen_uniform(N,dtype=np.float32,stream=None)
x2 = gpuRandom.gen_uniform(N,dtype=np.float32,stream=None)
testRadLength = pycuda.cumath.floor((x1**(2)).__add__(x2**(2)))
pi = 4*((N-gpuarray.sum(testRadLength))/N) #obtained by summing the gpuRadLength array

print ("Another Pi value calculated outside loop for comparison")
print (pi) #a separate Pi value calculated outside for loop for comparison

def gpuRandPi(N):
    calculatedPi2 = []
    errorswithGPUPi = []
    for j in range(N):
        xx1 = gpuRandom.gen_uniform(N,dtype=np.float32,stream=None)
        xx2 = gpuRandom.gen_uniform(N,dtype=np.float32,stream=None)
        testRadLength = pycuda.cumath.floor((xx1**(2)).__add__(xx2**(2)))
        pi2 = 4*((N-gpuarray.sum(testRadLength))/N)
        calculatedPi2.append(pi2)
        #print (pi2) #printing out all calculated Pi values as the loop goes; printing out an array of arrays could be tedious
        j += 1
        error = pycuda.cumath.sqrt((Sum((Pi - gpuarray.sum(pi2))**2)/j))
        errorswithGPUPi.append(error) 
        #array of all differences of all Pi and calculated Pi values; was not used
    return calculatedPi2,errorswithGPUPi
    
startTimeGPU = time.time()
calPi2, errorsPi2 = gpuRandPi(N)
endTimeGPU = time.time()
print (calPi2)
print ("Time for GPU Computation:")
print (endTimeGPU - startTimeGPU)