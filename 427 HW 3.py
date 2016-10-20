#!usr/bin/env python
### ADD WORKING CODE HERE ###
#discussed with prof

import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

#Definitions/Given values:
Sin = np.sin
Cos = np.cos
Pi = np.pi

def func(x): #given function
    return x**2 - 2.0
    
def kepler(M,E,e): #Kepler's 2nd Law
    #global M,e -> can set M and e outside of function
    return M-E-e*Sin(E)

def deriFunc(x): #derivative of given function
    return 2*x
    
def deriKepler(E,e): #derivative of the 2nd Law EQ in respect to E
    return -1-e*Cos(E)   

print "Question 1:"
print
# "func" = function ; "it" = iterations

def bisectMethod(func,ini,end,it,e=1.0,M=1.0): #bisectMethod for given function
#should have clarified what "e" and "M" are in the parameters
    aArray = np.zeros(it) #empty array for "a"
    bArray = np.zeros(it) #empty array for "b"
    iters = np.zeros(it) #empty array for plotting each iteration (to graph)
    a = ini
    b = end
    c = (ini + end)/2
    i = 0
    #this if-condition passes the correct function into the while-loop
    #by looking to see if the e,M values are modified
    if (e !=1.0 and M !=1.0):
    #THIS SHOULD be inside the while loop! Need to be evaluated during the loop and not outside
    #like this (and inside the while loop, but before the if):
        funky = func(M,c,e)
        #funkyb = func(M,b,e)
        #funkya = func(M,a,e)
    else:
        funky = func(c)
        
    while i < it:
        if funky < 0.0: #case 1: create a bracket closer to "a", left end of interval
            a = c 
            c = (a + b)/2 #same operations
            aArray[i] = a #store value for a
            iters[i] = i #stores current iteration number
            i += 1 #increment
        elif funky > 0.0: #case 2: create a bracket closer to "b", right end of interval
            b = c
            c = (a + b)/2
            bArray[i] = b
            iters[i] = i
        else:
            break #go out of loop and find error value
    return aArray, bArray,iters

def newtonMethod(func,deri,ini,tol,e=1.0, M=1.0): #newtonMethod for given function
    #lists are used instead because we don't know how long the method will iterate
    #tol = allowance of how much the result can be deviated from actual function
    iters = []
    result = []
    nextStart = ini + 2 #the constant is an arbitrary number to start the loop
    i = 0
    if M != 1.0:
        while np.abs(ini - nextStart) > tol:
            e1 = float(e) #e1,M1 in float to make sure that the denominator will be non-zero
            M1 = float(e)
            ini = nextStart
            nextStart = ini - (func(M1,ini,e1))/(deri(ini,e1))
            result.append(nextStart)
            iters.append(i)
            i += 1
    else:
        while np.abs(ini - nextStart) > tol:
            ini = nextStart
            nextStart = ini - (func(ini))/(deri(ini))
            result.append(nextStart)
            iters.append(i)
            i += 1

    return result,iters
    
#packaged methods to check accuracy
def bisectMethodCheck(func,ini,fin,it):
#ini,fin = start, end values of given interval
    return optimize.bisect(func,ini,fin,maxiter=it) 
     
def newtonMethodCheck(func,ini,deri,it):
    return optimize.newton(func,ini,fprime=deri,maxiter=it)   
   
#values
funcRoot = math.sqrt(2) #real root for first function
xPlotCheck = np.linspace(-2,3,50,endpoint=True) #linear space from x = -2 to x = 2

#iterSpace = np.linspace(0,50,50,endpoint = True) -> do this if you have time
#toler = 0.5 #tolerance for NewtonMethod

bisecAFunc, bisecBFunc, bisecIterFunc = bisectMethod(func,-1.0,1.5,30)
newtonResultFunc, newtonItersFunc = newtonMethod(func,deriFunc,1.5,0.001)

#trying for e = 0.9, M = 1.5
bisecAKepler, bisecBKepler, bisecIterKepler = bisectMethod(kepler,0,2*Pi,20,e=0.9,M=1.5)
newtonResultKep, newtonItersKep = newtonMethod(kepler,deriKepler,0,0.01,e=0.9,M=1.5)
#trying for e = 0.5, M = 1.5
bisecAKepler2, bisecBKepler2, bisecIterKepler2 = bisectMethod(kepler,0,2*Pi,20,e=0.5,M=1.5)
newtonResultKep2, newtonItersKep2 = newtonMethod(kepler,deriKepler,0,0.01,e=0.5,M=1.5)

bisectFuncCheck = bisectMethodCheck(func,-1.0,1.5,42) #f(-1),f(2) = negative, positive value of range
newtonFuncCheck = newtonMethodCheck(func,funcRoot,deriFunc,42)

leftHandValue = '''Array of roots for using left hand value of interval for Bisection Method'''
rightHandValue = '''Array of roots using right hand value of interval for Bisection Method'''
newtValue = '''Array of roots using Newton-Raphson Method'''

print "For the first function:"
print leftHandValue, bisecAFunc #A values for bisectMethod for function
print
print rightHandValue, bisecBFunc #B values for bisectMethod."
print
print newtValue, newtonResultFunc #newton results for function
print
print "For the Kepler's Law, e = 0.9:"
print leftHandValue,bisecAKepler
print
print rightHandValue,bisecBKepler
print
print newtValue, newtonResultKep
print
print "For the Kepler's Law, e = 0.5:"
print leftHandValue,bisecAKepler2
print
print rightHandValue,bisecBKepler2
print
print newtValue, newtonResultKep2
print
print "Checking values:"
print "Root obtained from packaged Bisection method:", bisectFuncCheck #actual root obtained from bisection method
print "Root obtained from packaged Newton Method: ", newtonFuncCheck #actual root obtained from newton method
print 

plt.title("Bisection Method for first Function")
plt.plot(bisecIterFunc,bisecAFunc,"r-") #bisecAFunc plot
plt.plot(bisecIterFunc,bisecBFunc,"b-") #bisecBFunc plot
print "If either the red or blue lines don't show, it is possibly due to the guess."
print "Depending on where the guess is made, the bisection method could either lean closer to the left or right."
print "Hence one array will not be accounted at all and it will display all zeros."
plt.show()
plt.title("Newton-Raphson Method for first Function")
plt.plot(newtonItersFunc,newtonResultFunc,"g--")
plt.show()
plt.title("Bisection Method for Kepler, e = 0.9")
plt.plot(bisecIterKepler,bisecAKepler,"ro")
plt.plot(bisecIterKepler,bisecAKepler,"bo")
plt.show()
plt.title("Newton Method for Kepler, e = 0.9")
plt.plot(newtonItersKep,newtonResultKep,"go")
plt.show()
plt.title("Bisection Method for Kepler, e = 0.5")
plt.plot(bisecIterKepler2,bisecAKepler2,"r*")
plt.plot(bisecIterKepler2,bisecAKepler2,"b*")
plt.show()
plt.title("Newton Method for Kepler, e = 0.5")
plt.plot(newtonItersKep2,newtonResultKep2,"g*")

plt.plot(bisectFuncCheck,"r*") # bisectFuncCheck
plt.show()
plt.plot(newtonFuncCheck,"ro") # newtonFuncCheck
plt.plot(xPlotCheck,func(xPlotCheck[:]),"b-") #original function

plt.show() #shows everything else

print "Question 2:"
E = np.linspace(0.,2.*Pi,20,endpoint=True) # setting values of E
M = np.linspace(0,2*Pi,20,endpoint=True) #setting values of M
sinValues = kepler(E,0.9,M)
cosValues = deriKepler(E,0.9)
plt.title('Sin(E) vs. Cos(E) with e=0.9')
plt.xlim(-2,2)
plt.ylim(-2*Pi,2*Pi)
plt.plot(sinValues,cosValues,'o--')
plt.show()

#trying another value of e, i.e e = 0.7 to see difference
sinValues = kepler(E,0.7,M)
cosValues = deriKepler(E,0.7)
plt.title('Sin(E) vs. Cos(E) with e=0.7')
plt.xlim(-2,2)
plt.ylim(-2,0)
plt.plot(sinValues,cosValues,'o--')

response = '''
From experimenting with the two methods, which were the bisection method and Newton-Raphson
method, it is clearly observed that the Newton method displayed a higher degree of efficiency
as it achieved the roots faster by producing the roots with less iterations. However, even
despite the Newton's pronounced efficiency, it requires that the derivative of the function to be
computed first. If the derivative is wrong then the whole approximation can be very inaccurate. 
Having that said, the bisection method is more predictable because its iteration counts can be accounted
for during its computation, though it will take more iterations to get to the same results.'''

print response
