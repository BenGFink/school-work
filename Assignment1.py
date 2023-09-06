#Analysis of how the fibonacci recurance relationship behaves with floating point numbers
#Assignment1.py
#Written sep 2022, Benjamin Fink, bgf6547@nyu.edu


import numpy as np
import matplotlib.pyplot as plt

print()
#fibanacci sequences being studied

def FibForward(f0,f1,M):
    ans = [f0,f1]
    for i in range(0,M):
        ans = [ans[1] , ans[0]+ans[1]] #applying the fibonacci relationship to get the next element
    return ans

def FibBackward(fM,fMp1,M):
    ans = [fM,fMp1]
    for i in range(0, M):
        ans = [ans[1]-ans[0], ans[0]] #applying the fibonacci relationship in reverse to get the previous element
    return ans

def UpDown(f0,f1,M):
    ans = FibForward(f0,f1,M)
    return FibBackward(ans[0],ans[1],M) #use the results of FibForward as the inputs for FibBackward

# Part (a) ------- Sanity check that we defined out functions correctly
# I used the standard inputs andused online sources to verify my porgram was working
print('SANITY CHECKS')
print()
print (str(FibForward(2,7,0)) + ' equals (2,7) as it should ') #checking base case
print (str(FibForward(0,1,10)) + ' equals (55,89) as it should ')
print (str(FibForward(0,1,100)) + ' equals (354224848179261915075, 573147844013817084101) as it should ')
#checking large case
print (str(FibBackward(0,1,0)) + ' equals (0,1) as it should ')#checking base case
print (str(FibBackward(55,89,10)) + ' equals (0,1) as it should ')#checking reverse what i know works
print()


#Part (b) ----- Error found when using integer type inputs
print('Errors when using integers:')
for M in range(0,129,8):
    [f0h, f1h] = UpDown(1,1,M)
    intro = 'absolute error when going up and down {M:3} steps is: '.format(M=M)
    err = '{error}'.format(error=f0h-1) #we computer the error as our output "f0h" minus the correct output of 1
    print(intro + err) #put the parts of the sentnce together
print()
print('These errors should be zero, since int type has infinite presicion')
print()

#Part (c) ----- Error found when using float type inputs
print('Errors when using floats:')
for M in range(0,129,8):
    [f0h, f1h] = UpDown(1.,1.,M)
    intro = 'absolute error when going up and down {M:3} steps is: '.format(M=M)
    err = '{error:e}'.format(error=f0h-1)  #we computer the error as our output "f0h" minus the correct output of 1
    print(intro + err) #put the parts of the sentnce together
print()
print('These errors should be zero and then start to increase in magnitude, since flt type introduces error over time')
print()

#Part (d) ----- Error found when using float type inputs and a small perturbation
print('Errors when using floats with small perturbation:')
for M in range(0,129,8):
    [f0h, f1h] = UpDown(1.,1.003,M)
    intro = 'absolute error when going up and down {M:3} steps is: '.format(M=M)
    err = '{error:e}'.format(error=f0h-1) #we computer the error as our output "f0h" minus the correct output of 1
    print(intro + err) #put the parts of the sentnce together
print()
print('The error in this case should appear almost immediately and then start to increase in magnitude. \n'
      'This happens because the original number themselves cant be described exactly in floating point and are \n'
      'rounded to begin with. Thus the influence and compounding of error starts immediately as opposed to the \n' 
      'case in part (b), where the first time error can exist is when a number has more binary digit than double \n'
      'prescience floating point and must then be rounded.')
print()

#Part (e) ----- plots of parts c and d
FibonacciErrorPlotFile = "FibonacciError.pdf"
length =129 #number of steps i choose to be the maximum after messing around to find a good value
partC = [(UpDown(1.,1.,M)[0]-1) for M in range(length)] #data for error of regualr floating point case
partD = [(UpDown(1.,1.003,M)[0]-1) for M in range(length)] #data for error of perturbed floating point case


fig, ax = plt.subplots() #make plot
ax.plot(np.arange(length), partC, label='floating') #add part c info to plot
ax.plot(np.arange(length), partD, label='perturbed floating') #add part d info to plot
ax.legend()
ax.grid()
ax.set_title(r'Errors found going Up and Down "M" steps in Fibonacci sequnce')
ax.set_xlabel('number "M" of steps')
ax.set_ylabel('symmetrical log scale')
plt.yscale('symlog')
plt.savefig(FibonacciErrorPlotFile)







