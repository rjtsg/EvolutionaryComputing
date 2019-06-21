# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:40:59 2019

@author: Roy
"""
# %% Import stuff
import FunctionFile as FF
import EvaluationFile as EF
import SearchFile as SF

# %%Write here 'global' parameters needed
N = 100 #population size
a = -1 #lower starting bound
b = 3  #upper starting bound
gen = 4 #Specify how many generations you want to have
Exec = 100 #number of executions of the algorithm
Fraction = 0.5 #Fraction of the parents dies
NM = 5 #Amount of members that undergo a mutation
Scaling = 1.25 #Border scaling parameter #see below this might be wrong now...
#for both it should be addaptable if -number use 1.25 if + use 0.75
Scale = 0.25 #Scale for Mutation2 up side (1+scale) low side (1-scale)
tol = 0.1  #the tolerance limit
limit = 10000 #the upper limit of generations
stop = 1000000 #after how many same numbers it should stop make large if you do not want this
# %% Call here the functions
members = FF.InitialPopulation(N,a,b)
frosen = FF.PopEval(members)
Parent1,Parent2 = FF.ParentSelection(members,frosen)
NewMembers = FF.ReproductionLife(Parent1,Parent2,Fraction)
MutatedMembers = FF.MutationXX(NewMembers,NM,a,b)
members1,OriginalMembers = FF.RunEvolution(N,a,b,gen,Fraction)
members2,OriginalMembers2 = FF.BaseEvolution(members,gen,Fraction,NM,a,b,Scale)

# %% Call here evaluation files
output1 = EF.QuickComparison(gen,members,Fraction,NM,Scaling,a,b,Scale)
output2 = EF.UQ(Exec,gen,N,a,b,Fraction,NM,Scaling,Scale)

# %% Call here the optimization function
#Minimum = SF.Minimize(tol,limit,stop,N,a,b,Fraction,NM,Scaling)
#print(Minimum)