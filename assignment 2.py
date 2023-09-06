#Tikhonov regularized linear least squares to find radial basis for noisy function
#Assignment2.py
#Written Oct 2022, Benjamin Fink, bgf6547@nyu.edu

#  make fake data for the radial basis function assignment

import numpy as np
import numpy.linalg as la
from numpy.random import default_rng  # randon number generator
import matplotlib.pyplot as plt


# -------------- function that creates fake data ----------------------

def fake_data(n, sig, L):
    """create a fake dataset of n noisy observations, y_i at points x_i
       y_i = f(x_i) + W_i,
       x_i = i*dx with x_0 = 0 and x_n = 1
       f(x) goes from 0 to 1 in a length L interval near x=.5
               Inputs:
       n  : (pos int) number of data points
       sig: (pos float) the standard deviation of the noise
       L  : (pos flost) the length scale of the transition
              Outputs:
       x,y (tupple)
       x:  (np array of floats) sample points generated
       y:  (np array of floats) observations at thos sample points
    """
    a = 0.  # ends of the x interval where the points go
    b = 1.
    x = np.linspace(a, b, n)  # includes endpoints by default

    y = np.zeros(n)
    rng = default_rng()  # instantiate a bit generator
    for k in range(n):
        xk = x[k]
        if xk < (1. - L) * .5:
            y[k] = 0.
        elif xk > (1. + L) * .5:
            y[k] = 1.
        else:
            y[k] = (xk - .5) / L + .5
        y[k] = y[k] + sig * rng.standard_normal()

    return x, y

#------------------- student part -----------------
def phi(r,S):
    '''
    the radial basis function
    :param r:the radius input of basis function phi
    :param S: the length scale
    :return: the quadratic exponential of r with length scale L
    '''
    return np.exp(-.5*(r/S)**2)

def A(n,m,S): #this is the only function which refrences directly the samples points of the fake data
    '''
    the basis matrix A
        row[i] = all phi basis functions evaluated at sample point x[i]
        column[j] = basis function phi (centered at cj) at all sample points x
    :param n: the numbers of rows of matrix A , i.e. the number of sample points of fake_data
    :param m: the number of columns of matrix A, i.e. the number of basis function going to be used in g(x) to
    approximate fake_data
    :param S: the length scale
    :return: an n by m matrix A where [A]ij is phi of the distance from sample i to center j.
    What this means is that we are forming a collection of phi functions evaluated at all sample points.

    '''
    A = np.zeros((n,m))
    c = np.linspace(0., 1., m) # the m different centers sampled evenly on the range [0,1]
    for i in range(0,n):
        for j in range (0,m):
            r = np.sqrt(abs(x[i]-c[j])) #euclidean distance between sample x_i and center c_j
            A[i][j]=phi(r,S)
    return A

def trlls(n,m,S,lam):
    '''
    preforms Tikhonov regularized linear least squares (trlls) on A to find the best weights w to be used in g(x)
    :param n: number of sample points
    :param m: the number of basis function going to be used in g(x)
    :param S: the length scale
    :param lam: the regularization parameter lambda
    :return: the weigths w found in using trlls on A
    '''
    u, sigma, vt = np.linalg.svd(A(n,m,S)) #svd of A
    rank = sigma.size
    w = np.zeros((m)) #initilaize weights as an array of zeros
    for i in range(0,rank):
        uColumn_i = u[:,i]
        vtRow_i = vt[i,:]
        scalar = sigma[i] * np.dot(uColumn_i,y)/(sigma[i]**2 + lam) # the scalar part of the algorithem from hw 2 part 4
        #hidden in this only time the y values from the data are refrenced
        w = w + scalar * vtRow_i
    return w

def g(n,m,S,lam):
    '''
    evaluates the function g using m basis functions at all n sample points by multiplying the wieght vector
    gotten from trlls by the basis matrix A
    :param n:number of sample points
    :param m: the number of basis function going to be used in g(x)
    :param S: the length scale
    :param lam: the regularization parameter lambda
    :return: an array where the value at index i is the value of our appraximating function 'g' at x[i]

    '''
    weights = trlls(n,m,S,lam)
    basis_samples = A(n,m,S)
    return np.matmul(basis_samples,weights)

def setPlot(r,c,m,S,lam):

    gx = g(n, m, S, lam)  #this lines just runs all the code above to the graph is

    ax[r,c].plot(x, y, ".")
    ax[r,c].plot(x, gx)
    title = "m = {m:d}".format(m=m)
    title = title + ", s = {S:.2f}".format(S=S)
    title = title + ", Lam = {lam:.1f}".format(lam=lam)
    title = title + ", Cond = '{cond:.0f}".format(cond=np.linalg.cond(A(n,m,S)))

    ax[r,c].set_title(title)
    ax[r,c].set_xlabel("x")
    ax[r,c].set_ylabel('g')
    ax[r,c].grid()
# ------------------- main program ------------------

# _____make fake data________
n = 2000
sig = .1
L = .1

x, y = fake_data(n, sig, L)


fig, ax = plt.subplots(2,3)  # Create a figure with 2 by 3 subplots


setPlot(0,0,4,.5,0) #medium S no lambda high condition
setPlot(0,1,6,.1,0) #small S no lambda
setPlot(0,2,6,.1,0) #small S no lambda
setPlot(1,0,6,.5,2) #medium S large lambda

x, y = fake_data(n, sig, .01) # make L smaller for the remaining 2 graohs
setPlot(1,1,6,.5,1)
setPlot(1,2,6,.5,.3)

plt.show()













