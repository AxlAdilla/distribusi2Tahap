#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 20:03:28 2019

@author: axl
"""
from Populasi import Populasi
from Individu import Individu
import os
import time
from numpy import array
if __name__ == "__main__":
    mutationRate = 0.1
    maxGenerasi = 1000
    populasi = 20
    nowGen = 0
    kapasitasP=[300,400]
    #kapasitasD=[250,600,400]
    #kapasitasA=[150,225,300,250]
    #biayaPD=array([[10,29],[17,12],[32,12]])
    #biayaDA=array([[13,8,62],[71,51,26],[11,23,24],[40,6,13]])
    kapasitasD=[500,200]
    kapasitasA=[250,450]
    biayaPD=array([[10,29],[17,12]])
    biayaDA=array([[13,8],[18,23]])
    aturan = {'kapasitasP':kapasitasP,'kapasitasD':kapasitasD,'kapasitasA':kapasitasA,'biayaPD':biayaPD,'biayaDA':biayaDA}
    #newPop
    pop = Populasi(populasi,mutationRate,aturan)
    while nowGen < maxGenerasi:
        os.system('clear')
        print ("Mutation Rate: {0}\nMax Generasi: {1}\nPopulasi: {2}\nGenerasi Sekarang: {3}\nBestIndividu :".format(mutationRate,maxGenerasi,populasi,nowGen))
        pop.evaluasiFitness()
        pop.fortuneWheel()
        pop.crossover()
        pop.selection()
        #individu = Individu(aturan)
        nowGen += 1
        
    
    
        #print('Biaya Transport:{0}\nFitness:{1}'.format(best.biaya,best.fitness))
        time.sleep(0.1)
    
    best = pop.bestIndividu()
    for node in best.dataDA:
        print(node)
    for node in best.dataPD:
        print(node)
    print('Biaya Transport:{0}\nFitness:{1}'.format(best.biaya,best.fitness))
    #print("panjang matingPool:{0}".format(len(pop.matingPool)))
    #for index,nodes in enumerate(pop.dataPop):
    #    print("Individu ke-{0}:".format(index))
    #    for node in nodes.data:
    #        print(node)
    #    print("Fitness individu-{0}:{1}".format(index,nodes.fitness))
    
    #print("BEST INDIVIDU:")
    #bestInd =pop.bestIndividu()
    #for node in bestInd.data:
    #    print("{0}".format(node))
    #print("fitness:{0}".format(bestInd.fitness))
    #
    #pop.fortuneWheel()
    #print("length Mating Pool : {0}".format(len(pop.matingPool)))
    #for nodes in pop.matingPool:
    #    for node in nodes.data:
    #       print(node)
    #time.sleep(2)
    
    #for node in individu.data:
    #    print(node)
    #print ("Fitness:{0}".format(individu.fitness))
    #individu.evaluasiFitness()
    #print ("Fitness:{0}".format(individu.fitness))
    