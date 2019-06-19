# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 19:27:05 2019

@author: Roy
"""

import FunctionFile as FF
import numpy as np


## %%Write here 'global' parameters needed
#N = 100 #population size
#a = -1 #lower starting bound
#b = 3  #upper starting bound
#gen = 3 #Specify how many generations you want to have
#Exec = 10 #number of executions of the algorithm
#Fraction = 0.5 #Fraction of the parents dies
#NM = 5 #Amount of members that undergo a mutation
#Scaling = 1.25 #Border scaling parameter

def Minimize(tol,limit,N,a,b,Fraction,NM,Scaling):
    gen = 0 #keep track of the number of generations that passed
    members = FF.InitialPopulation(N,a,b)
    frosen = FF.PopEval(members)
    frosenBest = np.amin(frosen)
    while frosenBest > tol and gen < limit:
        PreviousBest = frosenBest
        Parent1,Parent2 = FF.ParentSelection(members,frosen)
        members = FF.ReproductionLife(Parent1,Parent2,Fraction)
        members = FF.MutationBorderScale(members,NM,Scaling)
        frosen = FF.PopEval(members)
        frosenBest = np.amin(frosen)
        Index = np.where(frosen == np.amin(frosen))
        minimum = members[Index[0][0]]
        gen +=1
        print('Generation: %.f, f(x) = %.3f, df(x) = %.3f' % (gen,frosenBest,frosenBest-PreviousBest))
    return minimum