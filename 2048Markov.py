import random
import numpy as np
import pygame
import glob
import os
import sys
import time
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from game2048 import gameManager, tile


pygame.init()
game = gameManager()
game.restart()
game.updateGrid()

n_actions = 4
gamma = 0.9

  
def getState():
    state = game.gridValues()[0]
    state = np.ravel(state)
    def scale(X, x_min, x_max):
        nom = (X-X.min(axis=0))*(x_max-x_min)
        denom = X.max(axis=0) - X.min(axis=0)
        #denom[denom==0] = 1
        return x_min + nom/denom
    #state = scale(state, 0, 1)
    return state

def step(action,seed):# seed is where the random tile spawns and simulated is if its predicting future steps
    r = [0,[],False]
    
    if action == 0:    
        r = game.moveTiles([1,0],seed)        
    if action == 1:
        r = game.moveTiles([-1,0],seed)        
    if action == 2:
        r = game.moveTiles([0,1],seed)       
    if action == 3:
        r = game.moveTiles([0,-1],seed)
    
    return r


def get_best_action(state):
    Rewards = np.zeros((4,4,4))
    seeds = []
    tic = time.perf_counter()
    for t0action in range(n_actions):
        game.setGrid(state)
        t0r = step(t0action, [])
        Rewards[t0action,:,:] += t0r[0]
        seeds.append(t0r[1])
        next_state = game.gridValues()[0]
        for t1action in range(n_actions):
            game.setGrid(next_state)
            t1r = step(t1action, [])
            Rewards[t0action,t1action,:] += (gamma**1)*t1r[0]
            next_state = game.gridValues()[0]
            #for t2action in range(n_actions):
                #game.setGrid(next_state)
                #t2r = step(t2action, [], True)
                #Rewards[t0action,t1action,t2action] += (gamma**2)*t2r[0]
    toc = time.perf_counter()
    print(f"took {toc - tic:0.4f} seconds to find best action")
    game.setGrid(state)
    print(Rewards)
    if np.sum(Rewards) <= 0.0:
        sys.exit()
    best_action = np.unravel_index(Rewards.argmax(), Rewards.shape)
    print("best seed was {}.".format(seeds[best_action[0]]))
    print("best action was {}.".format(best_action[0]))
    return best_action[0], seeds[best_action[0]]

def run(time_steps):
    game.restart()
    for i in range(time_steps):
        tic = time.perf_counter()
        game.updateGrid()
        pygame.display.update()
        state = game.gridValues()[0]
        action, seed = get_best_action(state)
        reward, seed, running = step(action, seed)
        #time.sleep(10)
        toc = time.perf_counter()
        print(f"took {toc - tic:0.4f} seconds to run 1 timestep")
        
if __name__ == "__main__":
    run(2000)

