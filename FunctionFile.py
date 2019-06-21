# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:40:13 2019

@author: Roy
"""

# %% Load packages
import numpy as np
from scipy.optimize import rosen




# %% Write functions
def InitialPopulation(N,a,b):
    members = np.empty((N,4))
    for i in range(N):
        members[i] = np.random.uniform(a,b,4)
    return members

def PopEval(members):
    frosen = np.empty((len(members)))
    for i in range(len(members)):
        frosen[i] = rosen(members[i])
    return frosen

def ParentSelection(members,frosen):
    Parent1 = np.empty((int(len(members)/2),4))
    Parent2 = np.empty((int(len(members)/2),4))
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
    Kid1 = np.empty((int(len(Parent1)),4))
    Kid2 = np.empty((int(len(Parent2)),4)) 
    for i in range(len(Parent1)):
        Kid1[i] = np.append(Parent1[i][0:2],Parent2[i][2:4])
        Kid2[i] = np.append(Parent1[i][2:4],Parent2[i][0:2])
    NewMembers = np.append(Kid1,Kid2,0)
    return NewMembers

def ReproductionLife(Parent1,Parent2,Fraction):
    #The fraction of parents that stays alive
    Parent1survive = Parent1[0:int(len(Parent1)*Fraction)]
    Parent2survive = Parent2[0:int(len(Parent2)*Fraction)]
    Kid1 = np.empty((int(len(Parent1)*Fraction),4))
    Kid2 = np.empty((int(len(Parent2)*Fraction),4)) 
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
        gene = np.random.randint(0,len(Members[0]),1)
        Mutation = np.random.uniform(a,b,1)
        MutatedMembers[i,gene] = Mutation
    return MutatedMembers

def MutationBorderScale(Members,NM,Scaling):
    GenesForMutation = np.random.randint(0,len(Members),NM)
    MutatedMembers = np.copy(Members)
    for i in GenesForMutation:
        gene = np.random.randint(0,len(Members[0]),1)
        Mutation = np.random.uniform(np.amin(Members)*Scaling,np.amax(Members)*Scaling,1)
        MutatedMembers[i,gene] = Mutation
    return MutatedMembers

def RunEvolution(N,a,b,gen,Fraction):
    members1 = InitialPopulation(N,a,b)
    OriginalMembers = members1
    for i in range(gen):
        frosen = PopEval(members1)
        Parent1,Parent2 = ParentSelection(members1,frosen)
        members1 = ReproductionLife(Parent1,Parent2,Fraction)
    return members1,OriginalMembers

def BaseEvolution(base,gen,Fraction,NM,a,b):
    OriginalMembers = base
    for i in range(gen):
        frosen = PopEval(base)
        Parent1,Parent2 = ParentSelection(base,frosen)
        base = Reproduction4(Parent1,Parent2)
        base = MutationXX(base,NM,a,b)
    return base,OriginalMembers #note that here base is the new population...

def BaseEvolutionComp(base,gen,Fraction,NM,a,b):
    OriginalMembers = base
    for i in range(gen):
        frosen = PopEval(base)
        Parent1,Parent2 = ParentSelection(base,frosen)
        base = ReproductionLife(Parent1,Parent2,Fraction)
        base = MutationXX(base,NM,a,b)
    return base,OriginalMembers #note that here base is the new population...

def Reproduction4(Parent1,Parent2):
    Kid1 = np.empty((int(len(Parent1)),4))
    Kid2 = np.empty((int(len(Parent2)),4))
    Kid3 = np.empty((int(len(Parent1)),4))
    Kid4 = np.empty((int(len(Parent2)),4))
    BestNewMembers = np.empty((int(len(Parent1)+len(Parent2)),4))
    b100 = 0
    for i in range(len(Parent1)):
        Kid1[i] = np.append(Parent1[i][0:2],Parent2[i][2:4])
        Kid2[i] = np.append(Parent1[i][2:4],Parent2[i][0:2])
        Kid3[i] = np.append(Parent2[i][0:2],Parent1[i][2:4])
        Kid4[i] = np.append(Parent2[i][2:4],Parent1[i][0:2])
    NewMembers = np.append(Kid1,Kid2,0)
    NewMembers = np.append(NewMembers,Kid3,0)
    NewMembers = np.append(NewMembers,Kid4,0)
    NewMembers = np.append(NewMembers,Parent1,0)
    NewMembers = np.append(NewMembers,Parent2,0)
    frosen = PopEval(NewMembers)
    for i in range(len(NewMembers)):
        Index1 = np.where(frosen == np.amin(frosen))
        BestNewMembers[i] = NewMembers[Index1[0][0]]
        frosen = np.delete(frosen,Index1[0][0])
        NewMembers = np.delete(NewMembers,Index1[0][0],0)
        b100 +=1
        if b100 == 100:
            break
    return BestNewMembers
