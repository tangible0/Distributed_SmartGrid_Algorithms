# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 19:38:16 2018

@author: Andrew
"""

import numpy as np
import matplotlib.pyplot as plt
import copy
class GNode():

    def __init__(_self,a,b,ulim,llim,pos):
        _self.a = a
        _self.b = b
        _self.ulim = ulim
        _self.llim = llim
        _self.umax = (_self.ulim - _self.a)/_self.b
        _self.umin = (_self.llim - _self.a)/_self.b
        _self.p = 0
        _self.lamda = (_self.umax + _self.umin)/2
        _self.x = (_self.llim + _self.ulim)/2
        _self.pos = pos

    def u(_self, x): #lamda at a given load
        u = (x - _self.a)/_self.b
        u = np.clip(u,_self.umin,_self.umax)
        return(u)

    def solvex(_self,lamda):
        if lamda < _self.umin:
            return(_self.llim)
        if lamda >= _self.umax:
            return(_self.ulim)
        else:
            return(_self.a + lamda*_self.b)

    def cost(_self,x):
        cost = ((x - _self.a)**2)/(2*_self.b)
        return(cost)

class SNode():

    def __init__(_self,p,pos):
        _self.p = p
        _self.lamda = 0
        _self.x = 0
        _self.pos = pos

    def solvex(_self, lamda):
        return(0)

def consensus(array, W, maxitt = 10000, eps = .0000001):
    new = copy.copy(array)
    hist = [array[:]]
    itt = 0
    while itt < maxitt:
        old = hist[-1]
        for i in np.arange(0,len(array)):
            new[i] = np.dot(W[i,:],copy.copy(old))
        itt += 1
        if np.all(np.abs(new - old) < eps):
            return([new,hist])
        hist.append(copy.copy(new))
    return([new,hist])

def maxconsensus(array,A):
    diameter = len(array)
    array = copy.copy(array)
    for i in np.arange(0,diameter):
        array[i] = np.max(A[i,:]*array)
    print(array)
    return(array[0])

def minconsensus(array,A):
    diameter = len(array)
    array = copy.copy(array)
    for i in np.arange(0,diameter):
        array[i] = np.min(A[i,:]*array)
    print(array)
    return(array[0])

def alpha(t,num = .5, power = .85):
    return(num/(t**power))

def beta(t,num = .2, power = .001):
    return(num/(t**power))

def lEqual(nodes, eps = .00001):
    flag = True
    for i in np.arange(0,len(nodes)-1):
        for j in np.arange(i+1,len(nodes)):
            if abs(nodes[i].lamda - nodes[j].lamda) > eps:
                flag = False
                return(flag)
    return(flag)

def run(anum,apow,bnum,bpow):
    itt = 1
    maxitt = 200000
    eps = .00013
    lhist = []
    xhist = []
    x = [node.x for node in generators]
    costhist = []
    while (abs(np.sum(x) - np.sum(p)) > eps and itt < maxitt) or itt == 1:
        betat = beta(itt,bnum,bpow)
        alphat = alpha(itt,anum,apow)
        betat = 1/180000
        alphat = 1/100000
        lams = [node.lamda for node in generators]
        cost = 0
        for node in generators:
            li = copy.copy(node.lamda)
            locallams = RQ[node.pos,:]*lams
            ldiffs = betat*np.sum([li - lj for lj in locallams])
            xdiffs = alphat*(node.x -  node.p)
            node.lamda = li - ldiffs - xdiffs
            node.x = node.solvex(node.lamda)
            cost += node.cost(node.x)
        itt += 1
        x = [node.x for node in generators]
        lams = [node.lamda for node in generators]
        xhist.append(x)
        lhist.append(lams)
        costhist.append(cost)
    lavg = np.mean(lams)
    xtot = np.sum(x)
    return((itt,x,lams,xhist,[np.sum(n) for n in xhist],costhist))

p = np.array([0,0,0,.5,1.4,1.1,.9,.2])
p_tot = np.sum(p)
Q = np.array([1/3,1/5,0,1/4,0,0,0,0,1/3,1/5,1/5,0,0,1/5,0,1/3,0,1/5,1/5,0,0,1/5,1/3,1/3,1/3,0,0,1/4,1/4,1/5,0,0,0,0,0,1/4,1/4,1/5,1/3,0,0,1/5,1/5,1/4,1/4,1/5,0,0,0,0,1/5,0,1/4,0,1/3,0,0,1/5,1/5,0,0,0,0,1/3])
Q = Q.reshape((8,8))
AQ = Q > 0
R = np.array([1/2,1/3,0,1/2,1/3,1/2,0,1/3,1/2]).reshape((3,3))
RQ = R > 0

n1 = GNode(-1,3,2.1,0,0)
n2 = GNode(-1,2,1.0,0,1)
n3 = GNode(-1,2,5.0,0,2)
n4 = SNode(1,3)
n5 = SNode(1.4,4)
n6 = SNode(1.1,5)
n7 = SNode(.9,6)
n8 = SNode(.2,7)
nodes = [n1,n2,n3,n4,n5,n6,n7,n8]
generators = [n3,n2,n1]
lbounds = np.array([node.llim for node in generators])
ubounds = np.array([node.ulim for node in generators])
numnodes = len(nodes)
numgens = len(generators)
eps = .0001
diameter = 2

[p,phist] = consensus(p,Q)

sold = np.zeros((8,))
for i in np.arange(0,numgens):
    sold[i] = p[i]
snew = sold
[snew,hist] = consensus(snew,Q)

ynew = p*p/snew
[y,yhist] = consensus(ynew[0:3],R)

for i in np.arange(0,numgens):
    generators[i].p = y[i]

(itt,x,lams,xhist,xdiffs,costhist) = run(.2,.01,.2,.00001)
plt.plot(xhist)
