# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:55:22 2019

@author: Roy
"""
import numpy as np
import matplotlib.pyplot as plt
import FunctionFile as FF


# %% This would be quick comparison
def QuickComparison(gen,members,Fraction,NM,Scaling,a,b):
    BestEvalOriginal = np.empty((gen))
    BestEvalNew = np.empty((gen))
    MeanEvalOriginal = np.empty((gen))
    MeanEvalNew = np.empty((gen))
    BestEvalNewComp = np.empty((gen))
    MeanEvalNewComp = np.empty((gen))
    Generations = np.empty((gen))
    for i in range(gen):
        NewMembers,OriginalMembers = FF.BaseEvolution(members,10**i,Fraction,NM,a,b)
        BestEvalOriginal[i] = np.amin(FF.PopEval(OriginalMembers))
        BestEvalNew[i] = np.amin(FF.PopEval(NewMembers))
        MeanEvalOriginal[i] = np.mean(FF.PopEval(OriginalMembers))
        MeanEvalNew[i] = np.mean(FF.PopEval(NewMembers))
        Generations[i] = 10**i
        NewMembersComp,OriginalMembersComp = FF.BaseEvolutionComp(members,10**i,Fraction,NM,a,b)
    #    BestEvalOriginalComp[i] = np.amin(PopEval(OriginalMembersComp))
        BestEvalNewComp[i] = np.amin(FF.PopEval(NewMembersComp))
    #    MeanEvalOriginalComp[i] = np.mean(PopEval(OriginalMembersComp))
        MeanEvalNewComp[i] = np.mean(FF.PopEval(NewMembersComp))
        #GenerationsComp[i] = 10**i
    
    plt.figure(0)
    plt.plot(Generations,BestEvalNew)
    plt.plot(Generations,BestEvalOriginal)
    plt.plot(Generations,BestEvalNewComp)
    plt.title('Best ReproductionLife')
    plt.legend(['Reproduction4','Original','ReproductionLife'])
    plt.figure(1)
    plt.plot(Generations,MeanEvalNew)
    plt.plot(Generations,MeanEvalOriginal)
    plt.plot(Generations,MeanEvalNewComp)
    plt.legend(['Reproduction4','Original','ReproductionLife'])
    plt.title('Mean ReproductionLife')
    
    print('After: %.f generations f(x) = %.2f, compared to the theoretical value 0' % (10**(gen-1), np.amin(FF.PopEval(NewMembers))))
    print('After: %.f generations the mean f(x) = %.2f, compared to the theoretical value 0' % (10**(gen-1), np.mean(FF.PopEval(NewMembers))))

# %% Uncertainty quantification
#Use this code to evaluate the newly written code over multiple executions
#only that way we can be sure that the code is really improving. 
def UQ(Exec,gen,N,a,b,Fraction,NM,Scaling):
    BestMatOriginal = np.empty((Exec,gen))
    BestMatNew = np.empty((Exec,gen))
    MeanMatOriginal = np.empty((Exec,gen))
    MeanMatNew = np.empty((Exec,gen))
    BestMatNewComp = np.empty((Exec,gen))
    MeanMatNewComp = np.empty((Exec,gen))
    AvBestOriginal = np.empty((gen))
    AvBestNew = np.empty((gen))
    AvMeanOriginal = np.empty((gen))
    AvMeanNew = np.empty((gen))
    AvBestNewComp = np.empty((gen))
    AvMeanNewComp = np.empty((gen))
    B  = np.empty((gen))
    W  = np.empty((gen))
    Generations = np.empty((gen))
    for j in range(Exec):
        members = FF.InitialPopulation(N,a,b)
        for i in range(gen):
            NewMembers,OriginalMembers = FF.BaseEvolution(members,10**i,Fraction,NM,a,b)
            BestMatOriginal[j,i] = np.amin(FF.PopEval(OriginalMembers))
            BestMatNew[j,i] = np.amin(FF.PopEval(NewMembers))
            MeanMatOriginal[j,i] = np.mean(FF.PopEval(OriginalMembers))
            MeanMatNew[j,i] = np.mean(FF.PopEval(NewMembers))
            Generations[i] = 10**i
            NewMembersComp,OriginalMembersComp = FF.BaseEvolutionComp(members,10**i,Fraction,NM,a,b)
            BestMatNewComp[j,i] = np.amin(FF.PopEval(NewMembersComp))
            MeanMatNewComp[j,i] = np.mean(FF.PopEval(NewMembersComp))
            AvBestOriginal[i] = np.mean(BestMatOriginal[:,i])
            AvBestNew[i] = np.mean(BestMatNew[:,i])
            AvMeanOriginal[i] = np.mean(MeanMatOriginal[:,i])
            AvMeanNew[i] = np.mean(MeanMatNew[:,i])
            AvBestNewComp[i] = np.mean(BestMatNewComp[:,i])
            AvMeanNewComp[i] = np.mean(MeanMatNewComp[:,i])
            B[i] = np.amin(FF.PopEval(NewMembers))
            W[i] = np.amax(FF.PopEval(NewMembers))
    
    plt.figure(2)
    plt.plot(Generations,AvBestNew)
    #plt.fill_between(Generations,B,W,alpha=0.5)
    plt.plot(Generations,AvBestNewComp)
    plt.title('Average best values over %.f Executions' % Exec)
    plt.legend(['Reproduction4','ReproductionLife'])
    
    plt.figure(3)
    plt.plot(Generations,AvMeanNew)
    plt.plot(Generations,AvMeanNewComp)
    plt.title('Average values over %.f Executions' % Exec)
    plt.legend(['Reproduction4','ReproductionLife'])
    print('The average f(x) = %.3f after %.f Executions and %.f Generations' %(AvMeanNew[-1],Exec,10**(gen-1)))
    print('The minimum f(x) = %.3f after %.f Executions and %.f Generations' %(B[-1],Exec,10**(gen-1)))
    print('The maximum f(x) = %.3f after %.f Executions and %.f Generations' %(W[-1],Exec,10**(gen-1)))
