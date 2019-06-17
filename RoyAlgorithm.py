# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:04:50 2019

@author: Roy
"""
# %% Load in packages
import numpy as np
from scipy.optimize import minimize, rosen
import matplotlib.pyplot as plt

# %% Check if things work out
X0 = np.random.uniform(-1,1,4)
sol = rosen(X0)
res = minimize(rosen,X0, method='Nelder-Mead',tol=1e-6)
Xopt = np.array([1,1,1,1])
solopt = rosen(Xopt)

# %%Write here 'global' parameters needed
N = 100 #population size
a = -1 #lower starting bound
b = 3  #upper starting bound
gen = 4 #Specify how many generations you want to have
Exec = 10000 #number of executions of the algorithm
Fraction = 0.5 #Fraction of the parents dies
NM = 5 #Amount of members that undergo a mutation
Scaling = 1.25 #scaling factor for mutation boundary
# %% Write here the needed storage modules
members = np.empty((N,4))
frosen = np.empty((N))
Parent1 = np.empty((int(N/2),4))
Parent2 = np.empty((int(N/2),4))
Kid1 = np.empty((int(N/2*Fraction),4))
Kid2 = np.empty((int(N/2*Fraction),4))
BestEvalOriginal = np.empty((gen))
BestEvalNew = np.empty((gen))
MeanEvalOriginal = np.empty((gen))
MeanEvalNew = np.empty((gen))
#BestEvalOriginalComp = np.empty((gen))
BestEvalNewComp = np.empty((gen))
#MeanEvalOriginalComp = np.empty((gen))
MeanEvalNewComp = np.empty((gen))
Executions = np.empty((Exec))
Generations = np.empty((gen))

# %% Here the functions are made starts
def InitialPopulation(N,a,b):
    for i in range(N):
        members[i] = np.random.uniform(a,b,4)
    return members

def PopEval(members):
    for i in range(len(members)):
        frosen[i] = rosen(members[i])
    return frosen

def ParentSelection(members,frosen):
    for i in range(int(len(members)/2)):
        Index1 = np.where(frosen == np.amin(frosen)) #determine position
        Parent1[i] = members[Index1[0][0]]
        frosen = np.delete(frosen,Index1[0][0])
        members = np.delete(members,Index1[0][0],0)
        Index2 = np.where(frosen == np.amin(frosen))
        Parent2[i] = members[Index2[0][0]]
        frosen = np.delete(frosen,Index2[0][0])
        members = np.delete(members,Index2[0][0],0)
    return Parent1,Parent2

def Reproduction(Parent1,Parent2):
    for i in range(len(Parent1)):
        Kid1[i] = np.append(Parent1[i][0:2],Parent2[i][2:4])
        Kid2[i] = np.append(Parent1[i][2:4],Parent2[i][0:2])
    NewMembers = np.append(Kid1,Kid2,0)
    return NewMembers

def ReproductionLife(Parent1,Parent2,Fraction):
    #The fraction of parents that stays alive
    Parent1survive = Parent1[0:int(len(Parent1)*Fraction)]
    Parent2survive = Parent2[0:int(len(Parent2)*Fraction)]
    for i in range(int(len(Parent1)*Fraction)):
        Kid1[i] = np.append(Parent1survive[i][0:2],Parent2survive[i][2:4])
        Kid2[i] = np.append(Parent1survive[i][2:4],Parent2survive[i][0:2])
    NewMembers1 = np.append(Parent1survive,Parent2survive,0)
    NewMembers2 = np.append(NewMembers1,Kid1,0)
    NewMembers = np.append(NewMembers2,Kid2,0)
    return NewMembers

def MutationXX(Members,NM,a,b):
    GenesForMutation = np.random.randint(0,len(Members),NM)
    MutatedMembers = np.copy(Members)
    for i in GenesForMutation:
        gene = np.random.randint(0,len(Members[GenesForMutation])-1,1)
        Mutation = np.random.uniform(a,b,1)
        MutatedMembers[i,gene] = Mutation
    return MutatedMembers

def MutationBorderScale(Members,NM,Scaling):
    GenesForMutation = np.random.randint(0,len(Members),NM)
    MutatedMembers = np.copy(Members)
    for i in GenesForMutation:
        gene = np.random.randint(0,len(Members[GenesForMutation])-1,1)
        Mutation = np.random.uniform(np.amin(Members)*Scaling,np.amax(Members)*Scaling,1)
        MutatedMembers[i,gene] = Mutation
    return MutatedMembers

def RunEvolution(N,a,b,gen):
    members1 = InitialPopulation(N,a,b)
    OriginalMembers = members1
    for i in range(gen):
        frosen = PopEval(members1)
        Parent1,Parent2 = ParentSelection(members1,frosen)
        members1 = ReproductionLife(Parent1,Parent2,Fraction)
    return members1,OriginalMembers

def BaseEvolution(base,gen):
    OriginalMembers = base
    for i in range(gen):
        frosen = PopEval(base)
        Parent1,Parent2 = ParentSelection(base,frosen)
        base = ReproductionLife(Parent1,Parent2,Fraction)
        base = MutationBorderScale(base,NM,Scaling)
    return base,OriginalMembers #note that here base is the new population...

def BaseEvolutionComp(base,gen):
    OriginalMembers = base
    for i in range(gen):
        frosen = PopEval(base)
        Parent1,Parent2 = ParentSelection(base,frosen)
        base = ReproductionLife(Parent1,Parent2,Fraction)
        base = MutationXX(base,NM,a,b)
    return base,OriginalMembers #note that here base is the new population...

# %% Call here the functions
members = InitialPopulation(N,a,b)
frosen = PopEval(members)
Parent1,Parent2 = ParentSelection(members,frosen)
NewMembers = ReproductionLife(Parent1,Parent2,Fraction)
MutatedMembers = MutationXX(NewMembers,NM,a,b)
members1,OriginalMembers = RunEvolution(N,a,b,gen)
members2,OriginalMembers2 = BaseEvolution(members,gen)    
# %%The for loop that runs for several generations

#members = InitialPopulation(N,a,b)
#print('lowest value for rosenbrock before evolution: ',np.amin(PopEval(members)))
#for i in range(gen):
#    frosen = PopEval(members)
#    Parent1,Parent2 = ParentSelection(members,frosen)
#    members = Reproduction(Parent1,Parent2)
#
#print('lowest value for rosenbrock after evolution: ', np.amin(PopEval(members)))

# %%Write a loop that uses RunEvolution to visualise what happens over a amount
# of executions

#for i in range(Exec):
#    NewMembers,OriginalMembers = RunEvolution(N,a,b,gen)
#    BestEvalOriginal[i] = np.amin(PopEval(OriginalMembers))
#    BestEvalNew[i] = np.amin(PopEval(NewMembers))
#    MeanEvalOriginal[i] = np.mean(PopEval(OriginalMembers))
#    MeanEvalNew[i] = np.mean(PopEval(NewMembers))
#    Executions[i] = i 
#
#plt.figure(0)
#plt.plot(Executions,BestEvalOriginal)
#plt.plot(Executions,BestEvalNew)
#plt.legend(['Original','New'])
#plt.figure(1)
#plt.plot(Executions,MeanEvalOriginal)
#plt.plot(Executions,MeanEvalNew)
#plt.legend(['Original','New'])
#plt.figure(2)
#plt.plot(Executions,BestEvalOriginal-BestEvalNew)
#plt.figure(3)
#plt.plot(Executions,MeanEvalOriginal-MeanEvalNew)

# %% Look what the influence is of a amount of generations 

for i in range(gen):
    NewMembers,OriginalMembers = BaseEvolution(members,10**i)
    BestEvalOriginal[i] = np.amin(PopEval(OriginalMembers))
    BestEvalNew[i] = np.amin(PopEval(NewMembers))
    MeanEvalOriginal[i] = np.mean(PopEval(OriginalMembers))
    MeanEvalNew[i] = np.mean(PopEval(NewMembers))
    Generations[i] = 10**i
    NewMembersComp,OriginalMembersComp = BaseEvolutionComp(members,10**i)
#    BestEvalOriginalComp[i] = np.amin(PopEval(OriginalMembersComp))
    BestEvalNewComp[i] = np.amin(PopEval(NewMembersComp))
#    MeanEvalOriginalComp[i] = np.mean(PopEval(OriginalMembersComp))
    MeanEvalNewComp[i] = np.mean(PopEval(NewMembersComp))
    #GenerationsComp[i] = 10**i

plt.figure(0)
plt.plot(Generations,BestEvalNew)
plt.plot(Generations,BestEvalOriginal)
plt.plot(Generations,BestEvalNewComp)
plt.title('Best ReproductionLife')
plt.legend(['MutationBorderScaling','Original','MutationXX'])
plt.figure(1)
plt.plot(Generations,MeanEvalNew)
plt.plot(Generations,MeanEvalOriginal)
plt.plot(Generations,MeanEvalNewComp)
plt.legend(['MutationBorderScaling','Original','MutationXX'])
plt.title('Mean ReproductionLife')

print('After: %.f generations f(x) = %.2f, compared to the theoretical value 0' % (10**(gen-1), np.amin(PopEval(NewMembers))))
print('After: %.f generations the mean f(x) = %.2f, compared to the theoretical value 0' % (10**(gen-1), np.mean(PopEval(NewMembers))))