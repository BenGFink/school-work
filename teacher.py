#  Demonstration code for Scientific Computing class,
#  http://www.math.nyu.edu/faculty/goodman/teaching/SciComp2022/
#  BinomialCoefficients.py
#  Demonstrate practices and standards for computing exercises

#  Written September 2022, Jonathan Goodman, goodman@cims.nyu.edu

#  Compute binomial coefficients and make plots related to them

import numpy             as np
import matplotlib.pyplot as plt

#--------------- A function that evaluates binomail coefficients -----

def bc(n):
   """Return an array of binomail coefficients: n choose k for k = 0, ...,n
      input:  n (type = int)
      return: one index numpy array in double precision floating point
      of length n+1 with the coefficnents
   """

   bin = np.zeros(n+1)     #  Allocate a numpy one index array.  These
                           #  are float64 (double precision) by default
   nck = 1.                #  nck is for "n choose k", starting with k=0
                           #  Note: it's 1., not 1 to be floating point.

   bin[0] = nck

   for k in range(1,(n+1)):    # the integers 1,2,..,n
       nck    = nck*(n-k+1)/k  # n choose k is (n choose k-1)*(n-k+1)/k
       bin[k] = nck
   return bin

#--------- Main program, some experiments with binomial coefficients

#--------- Print the largest binomial coefficient and the error in n choose n

nVals = [5, 40, 80, 300, 1000, 2000]  # Compute (n/k) (binomial coef) for these n
print("Experiment computing binomial coefficients in floating point")

for n in nVals:
    b = bc(n)           # b becomes an array of n+1 binomial coeefficients
    max = np.amax(b)    # np.amax returns the largest value in the array
    err = b[n] - 1.     # is zero when arithmetic is exact

    out1 = "n is {n:4d}".format( n = n)                  # formatted numbers
    out2 = ", max is {max:10.3e}".format( max = max)     # commas in output
    out3 = ", error is {err:13.4e}".format( err = err)

    print( out1 + out2 + out3)    #  The numbers line up in the output

#--------- Plot the normalized coefficients, linear scale

LinearScalePlotFile = "LinearScaleBinomialCoefficients.pdf"
fig, ax = plt.subplots()     # Create a figure containing a single axes.

nVals = [30, 120, 1000]
for n in nVals:
    b = bc(n)
    m = np.amax(b)
    bn = b/m
    x = np.linspace( 0., 1., (n+1))          # n+1 uniformly spaced points
    LabelString = "n = {n:4d}".format(n=n)   # labels are for the legend
    ax.plot( x, bn, "o", ms = 2., label = LabelString)

ax.legend()
ax.grid()                                    # makes the plot readable
ax.set_title(r'Normalized binomial coefficients $\binom{n}{k}/\binom{n}{n/2}$')
ax.set_xlabel(r'$x_k = \frac{k}{n}$')
ax.set_ylabel('linear scale')
plt.savefig(LinearScalePlotFile)

#--------- Plot the normalized coefficients, log scale

LogScalePlotFile = "LogScaleBinomialCoefficients.pdf"
fig, ax = plt.subplots()     # Create a new figure.

for n in nVals:
    b = bc(n)
    m = np.amax(b)
    bn = b/m
    x = np.linspace( 0., 1., (n+1))
    LabelString = "n = {n:4d}".format(n=n)
    ax.semilogy( x, bn, "o", ms = 2., label = LabelString)
ax.legend()
ax.grid()
ax.set_title(r'Normalized binomial coefficients $\binom{n}{k}/\binom{n}{n/2}$')
ax.set_xlabel(r'$x_k = \frac{k}{n}$')
ax.set_ylabel('log scale')
plt.savefig(LogScalePlotFile)

plt.plot((3,5,7),(10,2,1))