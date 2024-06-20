import matplotlib
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# define to find eight neighbours given the position and size
# for periodic condition
def neighbours(row,col,lx):
    left_up = ((row-1)%lx,(col-1)%lx)
    up = ((row-1)%lx,col)
    right_up = ((row-1)%lx,(col+1)%lx)
    left = (row,(col-1)%lx)
    right = (row,(col+1)%lx)
    left_down = ((row+1)%lx,(col-1)%lx)
    down = ((row+1)%lx,col)
    right_down = ((row+1)%lx,(col+1)%lx)
    return left_up,up,right_up,left,right,left_down,down,right_down

def update(state,n):
    new_states = np.copy(state)
    for i in range(n):
        for j in range(n):
            living_neighbours = 0
            # counting living neighbours
            for neighbour in neighbours(i, j, n):
                living_neighbours += state[neighbour]
            # man im dead
            if state[i, j] == 1:
                if living_neighbours < 2 or living_neighbours > 3:
                    new_states[i, j] = 0
            # man im alive
            elif state[i,j] == 0:
                if living_neighbours == 3:
                    new_states[i, j] = 1
    return new_states
def update_new(state,l,n,p1,p2):
    new_states = np.copy(state)
    for i in range(l):
        for j in range(l):
            living_neighbours = 0
            # counting on neighbours
            for neighbour in neighbours(i, j, l):
                living_neighbours += state[neighbour]
            # turn on to off
            if state[i, j] == 1:
                if np.random.random() < p1:
                    new_states[i, j] = 0
            # turn off to on
            elif state[i,j] == 0:
                if living_neighbours == n:
                    if np.random.random() < p2:
                        new_states[i, j] = 1
    return new_states
# Calculate the average
def average(state,sweeps, callibration,l,n,p1,p2):
        fraction = []
        for n in range(sweeps):
            state = update_new(state,l,n,p1,p2)
            plt.cla()
            im=plt.imshow(state, animated=True)
            plt.draw()
            plt.pause(0.001)
            if n > callibration:
                inf = np.sum(state) / (l**2)
                if inf == 0:
                    return 0
                fraction.append(inf)
        avg = np.mean(fraction)
        return avg
# Set initial state with 1% on

p1s = np.linspace(0.1, 1, 10)
p2s = np.linspace(0.1, 1, 10)
l = 100
nstep = 200
n = 2
f = open('p1_p2_var.dat', 'w')
for i, p1 in enumerate(p1s):
    for j, p2 in enumerate(p2s):
        iR = []
        iR2 = []
        fraction = []
        state = np.zeros((l,l))
        state += np.random.randint(0,2,size=(l,l))
        fig = plt.figure(figsize=(10,10))
        im=plt.imshow(state, animated=True)
        for a in range(nstep):
            state = update_new(state,l,n,p1,p2)
            if n > 0:
                inf = np.sum(state) / (l**2)
                iR.append(inf)
                iR2.append(inf**2)
                fraction.append(inf)

        meaniR = np.mean(iR)
        meaniR2 = np.mean(iR2)
        var = (meaniR2 - meaniR**2) / (l**2)
        avg = np.mean(fraction)
        print(p1,p2,avg,var)
        print('Done')