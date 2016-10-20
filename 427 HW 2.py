#!usr/bin/env python

#import sys
import time as t
import math
import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import scipy.integrate as integrate

print "Question 1"
print "The Euler Method:"
#func = function we want to calculate 
#a, b = start, end values"
#ini = given y(0) value"
#n = number of samples"
print

def EulerMethod(func,a,b,n,ini):
    size = (b-a)/float(n)
    time = np.arange(a,b+size,size)
    out = np.zeroes(n+1) #np.zeroes((n+1,len(ini))) for 2D len(ini) -> is for length of the ini 'vector'
    time[0],out[0] = ini
    for i in range(1,n+1):
        out[i] = out[i-1] + size*func(time[i-1],out[i-1])       
    return out
    #return an array, specifically (np.array([x[1],-x[0]]))
    
#fix method for 2D next time for implementation (i.e x and y)
#i.e look at the len(ini) above to change into input into a vector
#specify the parameters; be more clear (i.e numbers or arrays?)
    
    
print "Runge-Kutta Method"
def RungeMethod(func,a,b,n,ini):
    size2 = (b-a)/float(n)
    time2 = np.arange(a,b+size2,size2)
    out2 = np.zeroes(n+1)
    time2[0],out2[0] = ini
    for i in range(1,n+1):
        k1 = size2*func(out2[i-1],time2[i-1])
        k2 = size2*func(out2[i-1]+(k1/2),time2[i-1]+(size2/2))
        k3 = size2*func(out2[i-1]+(k2/2),time2[i-1]+(size2/2))
        k4 = size2*func(out2[i]+k3,t[i]+size2)
        out[i] = out[i-1] + (k1+k2*2+k3*2+k4)/6
    return out

print "Leapfrog Method:"
def LeapMethod(tfinal, h, w0):
#designed specifically for x = cos(t)
#the function that we are integrating specifically for 2
    N = int(tfinal/h)
    h = tfinal/N
    x = np.zeros(N)
    xx = x.copy()
 
    x[0] = math.cos(0)  
    xx[0] = -w0*math.sin(0)
    t = np.arange(N)*h
    for i in range(1,N):
        x[i] = x[i-1] + h * xx[i-1] + h*h/2* (-w0**2)*x[i-1]
        xx[i] = xx[i-1] + h * (-w0**2) * (x[i-1] + x[i])/2
 
    return x,xx,t
    
print "Question 2"
#write the differential equation as a function of x and x'
def question(t,x):
    return(x[1],-x[0])

print "Using all 3 methods in one go"
x0 = np.array([1.,0.]) ## creates an array for the given values in the homework
time = np.array([0.,30.]) ## Creates an array for the time 
steps = np.array([1,.1,.1,.03,.01]) ### Array for iterated values
i=0 
while i < np.count_nonzero(steps): 
    for dt in steps: 
    
        #passing function in EulerMethod
        [X,T] = EulerMethod(question,x0,time,dt,0)
        plt.figure()
        plt.subplot(15,1,i + 1)
        plt.plot(T,X[0,:])
        i+=1
        
        #passing function in Runge-Kutta
        [X,T] = RungeMethod(question,x0,time)
        plt.figure()
        plt.subplot(15,2,i + 1)
        plt.plot(T,X)
        


print "Question 3"
time=np.arange(0,101,1)
stepsizes=np.arange(0.01,1.01,0.01)

phi=-(1.0/sqrt(1+x**2+y**2))

dx2=-x/(1+x**2+y**2)**(3/2)

dy2=-y/(1+x**2+y**2)**(3/2)


    