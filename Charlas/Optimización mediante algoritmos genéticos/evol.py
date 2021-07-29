#!/usr/bin/env python
import math
import numpy as np
from bike import Bike
from random import sample
from copy import deepcopy

def next_gen(bike_list,survivor_frac=0.2, n_crosses=20, n_mutations=20):
    bike_list = selection(bike_list,survivor_frac)
    bike_list.extend(mutations(bike_list,n_mutations))
    bike_list.extend(crossovers(bike_list,n_crosses))
    return bike_list

def selection(bike_list, survivor_frac=0.2):
    bike_list.sort(key=lambda x: x.score, reverse=True)
    bike_list = bike_list[:int(len(bike_list)*survivor_frac)]
    return bike_list

def crossovers(bike_list, n_crosses=20):
    def crossover(bike1,bike2):
        new_bike_mass = np.zeros(4)
        new_bike_pos =  np.array([np.zeros(2) for _ in range(4)])
        for i in range(4):
            new_bike_mass[i] = (bike1.bike_mass[i]+bike2.bike_mass[i])/2.0
            for i_dim in range(2):
                new_bike_pos[i][i_dim] = (bike1.init_pos[i][i_dim]+bike2.init_pos[i][i_dim])/2
        new_k_sp = (bike1.k_sp+bike2.k_sp)/2.0
        new_bike = Bike(pos=new_bike_pos, mass=new_bike_mass, k_sp=new_k_sp)
        return new_bike

    crossovers = []
    for _ in range(n_crosses):
        bike_1, bike_2 = sample(bike_list, 2)
        crossovers.append(crossover(bike_1, bike_2))
    return(crossovers)

def mutations(bike_list, n_mutations=20):
    def mutation(bike):
        new_bike_attrs = {}
        attrs = ['bike_mass','init_pos','k_sp']
        for attr in attrs:
            new_bike_attrs[attr] = deepcopy(getattr(bike, attr))
        mut_attr = sample(attrs,1).pop()
        new_bike_attrs[mut_attr] *= .5+np.random.random()
        new_bike = Bike(
                pos=new_bike_attrs['init_pos'], 
                mass=new_bike_attrs['bike_mass'], 
                k_sp=new_bike_attrs['k_sp'])

        return new_bike

    mutations = []
    for _ in range(n_mutations):
        mutations.append(mutation(sample(bike_list, 1).pop()))
    return mutations
