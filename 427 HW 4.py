#discussed with professor
import math
import numpy as np
import matplotlib.pyplot as plt

#Definitions
Exp = np.exp
Sqrt = np.sqrt
Log = math.log
phi = (Sqrt(5)-1)/2 #Golden ratio
    
#Given variables  
global v_inff,r_givenObs,v_givenObs 
v_inff = 100.0 #testing
r_givenObs = np.loadtxt('rot.dat',usecols=[0],unpack=True)
v_givenObs = np.loadtxt('rot.dat',usecols=[1],unpack=True)

#defined functions
def v_model(v_inf,r,r0):
    return v_inf*(1-Exp(r/r0))

def rad0(r_obs,v_inf,v_obs): #this is the rearranged function from the given v_model function to solve for r0
#for some reason I kept on getting a math error here, saying that the denominator is close to zero
    return -(r_obs/(Log((1-(v_obs/v_inf)),2.718)))
    
def error(v_obs,v_model):
    return (v_obs - v_model)**2
    
#didn't have to invert the function whatsoever! we just needed to minimize the error function!!
    
print "Question 1 - Construction of the Golden Search Method."
print
#func = function
#a,b = endpoints of interval [a,b]
#tol = tolerance value
    
def GoldMethod(func,a,b,tol,v_inf=1.0,v_obs=0):
#(General) Golden Search method that is adapted to include values for our functions
#Side note: This method is similar to the bisection method
    result = 0
    x1 = (phi-1)*a+ + (2-phi)*b #x-value of the left end of beginning interval
    x2 = (2-phi)*a + (phi-1)*b #x-value of the right end of interval
    
    #slightly different from expected range -> written in comments
    
    while np.abs(b - a) > tol:

        #by doing this it allows the function to take in extra values
        #if the parameters v_inf and v_obs are changed the func(x1) and func(x2) will be passed according to
        #the rad0 function
        if(v_obs!=0):
            funky1 = func(x1,v_inf,v_obs)
            funky2 = func(x2,v_inf,v_obs)
        else:
            funky1 = func(x1,10.0,1.0) #arbitrary values
            funky2 = func(x2,10.0,1.0)
        if funky1 < funky2:
            result = x1
            b = x2
            x2 = x1
            x1 = (phi-1)*a + (2-phi)*b
        elif funky1 > funky2:
            result = x2
            a = x1
            x1 = x2
            x2 = (phi-1)*a + (2-phi)*b
        elif funky1 == funky2:
            result = x1
        else:
            break
    return result

print
print "Question 2 - Confirmation of Golden Method."
print

def real_r0(v_inf): #this attempts to find the r0 of the given data
#by feeding the values of the data through a for loop
    all_r0 = np.zeros(len(r_givenObs))
    ii = 0
    for ii in range(len(r_givenObs)):
        v_given = v_givenObs[ii]
        guess = GoldMethod(rad0,ii,ii+1,1e-4,v_inf=v_inff,v_obs=v_given)
        all_r0[ii] = guess
    return all_r0

def gold_vmodel(v_inf,r,r0): #this attempts to find the v_model of the data with the r0 found above
#by feeding the r0 of each point into a for loop
    gold_model = np.zeros(len(r_givenObs))
    j = 0
    for j in range(len(r_givenObs)):
        gold_model[j] = -v_model(v_inf,r[j],r0[j]) #negative here because velocity is positive
    return gold_model

def error_graph(r0,v_inf): #attempts to find the error of the values through putting in values
#from the error function and the values of v_model and v_obs
    errs = np.zeros(len(r_givenObs))
    k = 0
    for k in range(len(r_givenObs)):
        errs[k] = (v_givenObs[k] - v_model(v_inf,r_givenObs[k],r0[k]))**2
    return errs

oh_yea = real_r0(v_inff) #attempts to find the r0 of the data
oh_model = gold_vmodel(v_inff,r_givenObs,oh_yea) #attempts to find the v_model using r0 from oh_yea
oh_bad = error_graph(oh_yea,v_inff) #attempts to find the error from the error function
xSpace = np.linspace(0,10,10,endpoint=True)

print "Arrays"
print oh_yea
print oh_model
print oh_bad

#Plotting/Printing
plt.plot(r_givenObs,oh_model,'b*') #plots the r_obs vs v_model
plt.plot(r_givenObs,v_givenObs,'g*-') #plots r_obs vs v_obs
plt.plot(xSpace,oh_bad,'r*-') #plots the error in respect to a normal linear space