import matplotlib
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pds

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

def update(state,l,n):
    new_states = np.copy(state)
    for i in range(l):
        for j in range(l):
            living_neighbours = 0
            # counting on neighbours
            for neighbour in neighbours(i, j, l):
                living_neighbours += state[neighbour]
            # turn on to off
            if state[i, j] == 1:
                new_states[i, j] = 0
            # turn off to on
            elif state[i,j] == 0:
                if living_neighbours == n:
                    new_states[i, j] = 1
    return new_states

# The new update law with probability
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
            if n > callibration:
                inf = np.sum(state) / (l**2)
                if inf == 0:
                    return 0
                fraction.append(inf)
        avg = np.mean(fraction)
        return avg

# Calculate the variance
def variance(state,sweeps, callibration,l,n,p1,p2):
    iR = []
    iR2 = []
    fraction = []
    # Variance and average calculation for given probabilities after sweeps
    for n in range(sweeps):
        state = update_new(state,l,n,p1,p2)
        if n > callibration:
            inf = np.sum(state) / (l**2)
            iR.append(inf)
            iR2.append(inf**2)
            fraction.append(inf)
    meaniR = np.mean(iR)
    meaniR2 = np.mean(iR2)
    var = (meaniR2 - meaniR**2) / (l**2)
    avg = np.mean(fraction)
    return (avg, var)
    
# Size of the system
# l = 100
# Update rule parameter
#n = 2
l = int(sys.argv[1])
n = float(sys.argv[2])

nstep = 1000
# This controls which part of the code to use
question = 'a'
# choose mode
if question == 'a':
    nlist = []
    tlist = np.arange(0,nstep,1)
    # Set initial state with 1% on
    state = np.zeros((l,l))
    for i in range(l):
        for j in range(l):
            if np.random.random()<0.01:
                state[i][j] = 1 
    # Visulise  
    fig = plt.figure(figsize=(10,10))
    im=plt.imshow(state, animated=True)
    for a in range(nstep):
        state = update(state,l,n)
        number = np.sum(state)
        nlist.append(number)
        plt.cla()
        im=plt.imshow(state, animated=True)
        plt.draw()
        plt.pause(0.001)
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.plot(tlist, nlist)
    ax.set_title('Number of total on states over time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of on states')
    plt.savefig('On_state_over_time')
    plt.show()
    plt.close()
if question == 'c':
    # Initial condition
    state = np.zeros((l,l))
    for i in range(l):
        if i > (l/2)-10 and i < (l/2)+10 :
            for j in range(l):
                if j > (l/2)-10 and j < (l/2)+10 :
                    state[i][j]=1
    fig = plt.figure(figsize=(10,10))
    im=plt.imshow(state, animated=True)
    for a in range(nstep):
        print(a)
        state = update(state,l,n)
        plt.cla()
        im=plt.imshow(state, animated=True)
        plt.draw()
        plt.pause(0.001)
if question == 'e':
    # Random initial state
    state = np.zeros((l,l))
    state += np.random.randint(0,2,size=(l,l))
    # Set up p1s and p2s
    p1s = np.linspace(0.1, 1, 10)
    p2s = np.linspace(0.1, 1, 10)
    f = open('p1_p2_var.dat', 'w')
    # Iterate among the p1s and p2s
    for i, p1 in enumerate(p1s):
        for j, p2 in enumerate(p2s):
            iR = []
            iR2 = []
            fraction = []
            state = np.zeros((l,l))
            state += np.random.randint(0,2,size=(l,l))
            for a in range(300):
                state = update_new(state,l,n,p1,p2)
                if n > 0:
                    inf = np.sum(state) / (l**2)
                    iR.append(inf)
                    iR2.append(inf**2)
                    fraction.append(inf)
            # Calculate the variance and average
            meaniR = np.mean(iR)
            meaniR2 = np.mean(iR2)
            var = (meaniR2 - meaniR**2)
            avg = np.mean(fraction)
            f.write(f'{p1} {p2} {avg} {var}\n')
    f.close()
if question == 'f':
    f = 'p1_p2_var.dat'
    with open(f, "r") as txt_file:
        input_data = [line.split() for line in txt_file]
    p1s = np.linspace(0.1, 1, 10)
    p2s = np.linspace(0.1, 1, 10)
    max_p2 = []
    avg = []
    var = []
    for i in range(len(input_data)):
        var.append(float(input_data[i][3]))
    plot_var = np.transpose(np.array(var).reshape((10, 10)))
    # Find the value of p2 for each p1 where the variance is the highest
    for j in range(len(plot_var)):
        max_p2_index = np.argmax((plot_var[j]))
        max_p2.append((max_p2_index+1)*0.1)
    # Try to fit a line based on the p1 and p2 values
    x,y = np.polyfit(p1s,max_p2,1)
    print(x,y)