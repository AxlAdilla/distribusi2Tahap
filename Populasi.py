#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 01:24:29 2019

@author: axl
"""
from Individu import Individu
import copy
import math
import random
class Populasi:
    def __init__(self,populasi,mutationRate,aturan):
        self.dataPop = []
        self.offSpringPop = []
        self.populasi = populasi
        self.aturan = aturan
        self.mutationRate = mutationRate
        self.randomPopulasi()
        self.matingPool = []
        
    def randomPopulasi(self):
        for i in range(0,self.populasi):
            individu = Individu(self.aturan)
            self.dataPop.append(individu)
        pass
    def evaluasiFitness(self):
        for node in self.dataPop:
            node.evaluasiFitness()
        pass   
    
    def bestIndividu(self):
        bestIndv = Individu(self.aturan)
        for node in self.dataPop:
            if bestIndv.fitness < node.fitness:
                bestIndv = copy.deepcopy(node)     
        return bestIndv
        pass
    
    def sortNextOffspring(self,allPool):
        temp = []
        for index,nodes in enumerate(allPool):    
            terkecil = True
            if len(temp) == 0 :
                temp.append(nodes)
            else:
                for i in range(0,len(temp)):
                    if nodes.fitness > temp[i].fitness:
                        temp.insert(i,nodes)
                        terkecil  = False
                        break
                if terkecil :
                    temp.append(nodes)
        return temp
        
    def selection(self):
        #Elitism Seleksi
        allPool = []
        allPool.extend(self.dataPop)
        allPool.extend(self.offSpringPop)
        #print(len(allPool))
        print('DataPop Sebelum')
        for index,nodes in enumerate(self.dataPop[:5]):
            print("Index:{0} ,fitness:{1} ,biaya:{2}".format(index,nodes.fitness,nodes.biaya))
        print('Anak Pop')
        for index,nodes in enumerate(self.offSpringPop[:5]):
            print("Index:{0} ,fitness:{1} ,biaya:{2}".format(index,nodes.fitness,nodes.biaya))    
        #print('setelah Sort')
        newPool = self.sortNextOffspring(allPool)
        #for index,nodes in enumerate(allPool):
        #    print("Index:{0} ,fitness:{1} ,biaya:{2}".format(index,nodes.fitness,nodes.biaya))
            
        self.dataPop = newPool[:self.populasi]
        print('DataPop Baru')
        for index,nodes in enumerate(self.dataPop[:5]):
            print("Index:{0} ,fitness:{1} ,biaya:{2}".format(index,nodes.fitness,nodes.biaya))
    
    def fortuneWheel(self):
        totalFitness = 0
        for node in self.dataPop:
            totalFitness+=node.fitness
        for node in self.dataPop:
            persentase = math.floor(node.fitness/totalFitness*100)
            for i in range(0,persentase):
                self.matingPool.append(node)
    
    def crossover(self):
        self.offSpringPop = []
        while len(self.offSpringPop) < len(self.dataPop):
            randParent1 = random.randint(0,len(self.matingPool)-1)
            randParent2 = random.randint(0,len(self.matingPool)-1)
        
            Parent1 = self.matingPool[randParent1]
            Parent2 = self.matingPool[randParent2]
        
            offSpring1 = copy.deepcopy(Parent1)
            offSpring2 = copy.deepcopy(Parent2)
        
            offSpring1.crossover(offSpring2)
            
            offSpring1.mutation(self.mutationRate)
            offSpring1.evaluasiFitness()
          #  print("ANAK : {0}".format(len(self.offSpringPop)))
            
          #  print("Data DA")
          #  for node in offSpring1.dataDA:
          #      print(node)
          #  print("Data PD")
          #  for node in offSpring1.dataPD:
          #      print(node)
          #  print("BIAYA: {}".format(offSpring1.biaya))
            self.offSpringPop.append(offSpring1)
            
                
        
    
            
        