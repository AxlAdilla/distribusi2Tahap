#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 01:52:05 2019

@author: axl
"""
import random

class Individu:
    def __init__(self,rules):
        self.rules = rules
        self.dataPD = []
        self.dataDA = []
        self.kebutuhanDistibutor = [0,0]
        self.kebutuhanPabrik = [0,0]
        self.fitness = 0
        self.biaya = 0
        self.randomDA()   
        self.randomPD()
    
    def randomDA(self):
        kapasitasAnow=[0,0]
        while self.isDANotComplete(kapasitasAnow):
            randomA = random.randint(1,2)
            distrib = random.randint(1,2)
            maxVal = self.rules['kapasitasA'][randomA-1] - kapasitasAnow[randomA-1]
            maxVal2 = self.rules['kapasitasD'][distrib-1]
            maxVal = min(maxVal,maxVal2)
            if maxVal > 0:
                val = random.randint(1,maxVal)
                node = {'value':val,'Distributor':distrib,'Agen':randomA}
                kapasitasAnow[randomA-1] += node['value']
                self.kebutuhanDistibutor[distrib-1] += val
                self.dataDA.append(node)
    
    def randomPD(self):
        kapasitasDnow=[0,0]
        while self.isPDNotComplete(kapasitasDnow):
            randomD = random.randint(1,2)
            pabrik = random.randint(1,2)
            maxVal = self.kebutuhanDistibutor[randomD-1] - kapasitasDnow[randomD-1]
            maxVal2 = self.rules['kapasitasP'][pabrik-1]
            maxVal = min(maxVal,maxVal2)
            if maxVal > 0:
                val = random.randint(1,maxVal)
                
                node = {'value':val,'Pabrik':pabrik,'Distributor':randomD}
                kapasitasDnow[randomD-1] += node['value']
                self.kebutuhanPabrik[pabrik-1] += val
                self.dataPD.append(node)

    def isDANotComplete(self,kapasitasAnow):
        for i in range(0,len(kapasitasAnow)):
            if kapasitasAnow[i] != self.rules['kapasitasA'][i]:
                return True
        return False
    
    def isPDNotComplete(self,kapasitasDnow):
        for i in range(0,len(kapasitasDnow)):
            if kapasitasDnow[i] != self.kebutuhanDistibutor[i]:
                return True
        return False
         
    def isAllSended(self):
        kapasitasAnow=[0,0]
        kapasitasDnow=[0,0]
        for node in self.dataDA:
            kapasitasAnow[node['Agen']-1] += node['value']
        for node in self.dataPD:
            kapasitasDnow[node['Distributor']-1] += node['value']
        if not self.isDANotComplete(kapasitasAnow) and not self.isPDNotComplete(kapasitasDnow):
            return True 
        else:
            return False
    
    def evaluasiFitness(self):
        if self.isAllSended():    
            biayaTransport = 0
            for node in self.dataPD:
                pabrik = node['Pabrik']-1
                distributor = node['Distributor']-1
                biayaTransport += self.rules['biayaPD'][distributor][pabrik]
            for node in self.dataDA:
                agen = node['Agen']-1
                distributor = node['Distributor']-1
                biayaTransport += self.rules['biayaDA'][agen][distributor]
            self.biaya = biayaTransport
            self.fitness = 1/biayaTransport
        else:
            self.biaya = 0
            self.fitness = 0
    def sortAgen(self,listAgen):
        temp = [[],[]]
        for index,nodes in enumerate(listAgen):    
            for node in nodes:
                terkecil = True
                if len(temp[index]) == 0 :
                    temp[index].append(node)
                else:
                    #swap=[]
                    for i,val in enumerate(temp[index]):
                        #print("node val {0}\nval {1}".format(node['value'],val))
                        if node['value'] > val['value']:
                            temp[index].insert(i,node)
                            terkecil  = False
                            break
                    if terkecil :
                        temp[index].append(node)
        return temp
    
    def sortDistributor(self,listDistributor):
        temp = [[],[]]
        for index,nodes in enumerate(listDistributor):    
            for node in nodes:
                terkecil = True
                if len(temp[index]) == 0 :
                    temp[index].append(node)
                else:
                    #swap=[]
                    for i,val in enumerate(temp[index]):
                        #print("node val {0}\nval {1}".format(node['value'],val))
                        if node['value'] > val['value']:
                            temp[index].insert(i,node)
                            terkecil  = False
                            break
                    if terkecil :
                        temp[index].append(node)
        return temp
    
    def crossover(self,pasangan):
        #random DA&PD atau random PD
        jenisRandom = random.randint(1,2)
        if jenisRandom == 1:
       #     print('panajang Data DA awal:{0}'.format(len(self.dataDA)))
       #     for node in self.dataDA:
       #         print(node)
       #     print('panajang pasangan awal:{0}'.format(len(pasangan.dataDA)))
       #     for node in pasangan.dataDA:
       #         print(node)
            
            #DA 
            panjangParent1 = len(self.dataDA)-1
            panjangParent2 = len(pasangan.dataDA)-1
            
            randomOnePoint = random.randint(0,min(panjangParent1,panjangParent2))
        #    print('random one point = {0}'.format(randomOnePoint))
            temp = self.dataDA[0:randomOnePoint]
            temp.extend(pasangan.dataDA[randomOnePoint:])
            
            self.dataDA.clear()
            self.dataDA = temp[:]
       #     print ('Data DA setelah')
       #     for node in self.dataDA:
       #         print(node)
            #Apakah dengan di cross Kebutuhan Agen terpenuhi ?
       #     print('sini1')
            kapasitasAnow=[0,0]
            for node in self.dataDA:
                kapasitasAnow[node['Agen']-1] += node['value']
       #     print('kapasitas Agen lama:')
       #     print(kapasitasAnow)
            if kapasitasAnow != self.rules['kapasitasA']:
       #         print('sini 2')
                tempIndex = [[],[]]
                for index,node in enumerate(self.dataDA):
 #                   tempIndex[node['Agen']-1].append({'index':index,'value':node['value']})
                    tempIndex[node['Agen']-1].append(node)
                tempIndex = self.sortAgen(tempIndex)[:]
       #         print('urutan adalah: ')
       #         for index,hh in enumerate(tempIndex):
       #             print("Agen ke-{0}".format(index+1))
       #             for nn in hh:
       #                 print(nn)
                        
                for i in range(0,len(kapasitasAnow)):
                    while kapasitasAnow[i] > self.rules['kapasitasA'][i]:
                        eraseNode = tempIndex[i].pop()
                        valueTerhapus = eraseNode['value']
                        self.dataDA.remove(eraseNode)
      #                  print('Terhapus Value : {0}'.format(valueTerhapus))
                        kapasitasAnow[i] = kapasitasAnow[i]-valueTerhapus
                        
                    while kapasitasAnow[i] < self.rules['kapasitasA'][i]:
                        distrib = random.randint(1,2)
                        maxVal = self.rules['kapasitasA'][i] - kapasitasAnow[i]
                        maxVal2 = self.rules['kapasitasD'][distrib-1]
                        maxVal = min(maxVal,maxVal2)
                        if maxVal > 0:
                            val = random.randint(1,maxVal)
                            node = {'value':val,'Distributor':distrib,'Agen':i+1}
                            kapasitasAnow[i] += val
                            self.dataDA.append(node)
                    
     #               print('kapasitas Agen kini:')
     #               print(kapasitasAnow)
                
        #Berapa Kebutuhan distributor yang harus dipenuhi saat ini ? 
        kapasitasDnow=[0,0]
        for node in self.dataDA:
            kapasitasDnow[node['Distributor']-1] += node['value']
    #    print('Kebutuhan Distributor lama:')
    #    print(kapasitasDnow)
        self.kebutuhanDistibutor = kapasitasDnow[:]
      #  print('Sini 3')
        #PD
        #print('panajang Data PD awal:{0}'.format(len(self.dataPD)))
        #for node in self.dataPD:
        #    print(node)
        #print('panajang pasangan PD awal:{0}'.format(len(pasangan.dataPD)))
        #for node in pasangan.dataPD:
        #    print(node)
        panjangParent1 = len(self.dataPD)-1
        panjangParent2 = len(pasangan.dataPD)-1
        
        randomOnePoint = random.randint(0,min(panjangParent1,panjangParent2))
        #print('random one point = {0}'.format(randomOnePoint))
        tempPD = self.dataPD[0:randomOnePoint]
        tempPD.extend(pasangan.dataPD[randomOnePoint:])
            
        self.dataPD.clear()
        self.dataPD = tempPD[:]
        #print ('Data PD setelah')
        #for node in self.dataPD:
        #    print(node)
            
        #Apakah kebutuhan Distribusi sudah terpenuhi ? 
        kapasitasDnow=[0,0]
        for node in self.dataPD:
            kapasitasDnow[node['Distributor']-1] += node['value']
    #    print('pengiriman Distributor saat ini:')
    #    print(kapasitasDnow)
        
        if kapasitasDnow != self.kebutuhanDistibutor:
         #       print('sini 4')
                tempIndexPD = [[],[]]
                for index,node in enumerate(self.dataPD):
 #                   tempIndex[node['Agen']-1].append({'index':index,'value':node['value']})
                    tempIndexPD[node['Distributor']-1].append(node)
                tempIndexPD = self.sortDistributor(tempIndexPD)[:]
           #     print('urutan adalah: ')
           #     for index,hh in enumerate(tempIndexPD):
           #         print("Distibutor ke-{0}".format(index+1))
           #         for nn in hh:
           #             print(nn)
                        
                for i in range(0,len(kapasitasDnow)):
                    while kapasitasDnow[i] > self.kebutuhanDistibutor[i]:
                        eraseNodePD = tempIndexPD[i].pop()
                        valueTerhapus = eraseNodePD['value']
                        self.dataPD.remove(eraseNodePD)
          #              print('Distributor Terhapus Value : {0}'.format(valueTerhapus))
                        kapasitasDnow[i] = kapasitasDnow[i]-valueTerhapus
                        
                    while kapasitasDnow[i] < self.kebutuhanDistibutor[i]:
                        pabrik = random.randint(1,2)
                        maxVal = self.rules['kapasitasD'][i] 
                        maxVal2 = self.kebutuhanDistibutor[i]- kapasitasDnow[i]
                        maxVal = min(maxVal,maxVal2)
                        if maxVal > 0:
                            val = random.randint(1,maxVal)
                            node = {'value':val,'Pabrik':pabrik,'Distributor':i+1}
                            kapasitasDnow[i] += node['value']
                            self.dataPD.append(node)
                    
      #              print('pengiriman Distrikbutor kini:')
     #               print(kapasitasDnow)
    def mutation2(self,mutationRate):
        if random.randint(0,100) < (mutationRate*100):
            self.dataPD = []
            self.dataDA = []
            self.kebutuhanDistibutor = [0,0,0]
            self.kebutuhanPabrik = [0,0]
            self.fitness = 0
            self.biaya = 0
            self.randomDA()
            self.randomPD()
            
    def mutation(self,mutationRate):
        if random.randint(0,100) < (mutationRate*100):
            jenisRandom = random.randint(1,2)
            if jenisRandom == 1:
                #DA
                #print ('Data DA sebelum')
           #     for node in self.dataDA:
           #         print(node)
                    
                randomFirstNode = random.randint(0,len(self.dataDA)-1)
                randomSecondNode = random.randint(0,len(self.dataDA)-1)
           #     print('random one point = {0}'.format(randomFirstNode))
          #      print('random second point = {0}'.format(randomSecondNode))
                temp = self.dataDA[randomFirstNode]['value']
                self.dataDA[randomFirstNode]['value'] = self.dataDA[randomSecondNode]['value']
                self.dataDA[randomSecondNode]['value'] = temp
                
            #    print ('Data DA setelah')
             #   for node in self.dataDA:
              #      print(node)
                #Apakah dengan di cross Kebutuhan Agen terpenuhi ?
               # print('sini1')
                kapasitasAnow=[0,0]
                for node in self.dataDA:
                    kapasitasAnow[node['Agen']-1] += node['value']
            #    print('kapasitas Agen lama:')
            #    print(kapasitasAnow)
                if kapasitasAnow != self.rules['kapasitasA']:
             #       print('sini 2')
                    tempIndex = [[],[]]
                    for index,node in enumerate(self.dataDA):
                        tempIndex[node['Agen']-1].append(node)
                    tempIndex = self.sortAgen(tempIndex)[:]
             #       print('urutan adalah: ')
             #       for index,hh in enumerate(tempIndex):
             #           print("Agen ke-{0}".format(index+1))
             #           for nn in hh:
             #               print(nn)
                                
                    for i in range(0,len(kapasitasAnow)):
                        while kapasitasAnow[i] > self.rules['kapasitasA'][i]:
                            eraseNode = tempIndex[i].pop()
                            valueTerhapus = eraseNode['value']
                            self.dataDA.remove(eraseNode)
              #              print('Terhapus Value : {0}'.format(valueTerhapus))
                            kapasitasAnow[i] = kapasitasAnow[i]-valueTerhapus
                                
                        while kapasitasAnow[i] < self.rules['kapasitasA'][i]:
                            distrib = random.randint(1,2)
                            maxVal = self.rules['kapasitasA'][i] - kapasitasAnow[i]
                            maxVal2 = self.rules['kapasitasD'][distrib-1]
                            maxVal = min(maxVal,maxVal2)
                            if maxVal > 0:
                                val = random.randint(1,maxVal)
                                node = {'value':val,'Distributor':distrib,'Agen':i+1}
                                kapasitasAnow[i] += val
                                self.dataDA.append(node)
                    
               #     print('kapasitas Agen kini:')
               #     print(kapasitasAnow)
            kapasitasDnow=[0,0]
            for node in self.dataDA:
                kapasitasDnow[node['Distributor']-1] += node['value']
            self.kebutuhanDistibutor = kapasitasDnow[:]
          #  print('kebutuhan distributor :')
          #  print(self.kebutuhanDistibutor)
          #  print('Sini 3')
            
            #PD
          #  print('panajang Data PD awal:{0}'.format(len(self.dataPD)))
          #  for node in self.dataPD:
          #      print(node)
            
            randomFirstNode = random.randint(0,len(self.dataPD)-1)
            randomSecondNode = random.randint(0,len(self.dataPD)-1)
          #  print('random one point = {0}'.format(randomFirstNode))
          #  print('random second point = {0}'.format(randomSecondNode))
            
            temp = self.dataPD[randomFirstNode]['value']
            self.dataPD[randomFirstNode]['value'] = self.dataPD[randomSecondNode]['value']
            self.dataPD[randomSecondNode]['value'] = temp
            
          #  print ('Data PD setelah')
          #  for node in self.dataPD:
          #      print(node)
            
            #Apakah kebutuhan Distribusi sudah terpenuhi ? 
            kapasitasDnow=[0,0]
            for node in self.dataPD:
                kapasitasDnow[node['Distributor']-1] += node['value']
           # print('pengiriman Distributor saat ini:')
           # print(kapasitasDnow)
        
            if kapasitasDnow != self.kebutuhanDistibutor:
            #    print('sini 4')
                tempIndexPD = [[],[]]
                for index,node in enumerate(self.dataPD):
                    tempIndexPD[node['Distributor']-1].append(node)
                tempIndexPD = self.sortDistributor(tempIndexPD)[:]
           #     print('urutan adalah: ')
           #     for index,hh in enumerate(tempIndexPD):
           #         print("Distibutor ke-{0}".format(index+1))
           #         for nn in hh:
           #             print(nn)
                        
                for i in range(0,len(kapasitasDnow)):
                    while kapasitasDnow[i] > self.kebutuhanDistibutor[i]:
                        eraseNodePD = tempIndexPD[i].pop()
                        valueTerhapus = eraseNodePD['value']
                        self.dataPD.remove(eraseNodePD)
          #              print('Distributor Terhapus Value : {0}'.format(valueTerhapus))
                        kapasitasDnow[i] = kapasitasDnow[i]-valueTerhapus
                        
                    while kapasitasDnow[i] < self.kebutuhanDistibutor[i]:
                        pabrik = random.randint(1,2)
                        maxVal = self.rules['kapasitasD'][i] 
                        maxVal2 = self.kebutuhanDistibutor[i]- kapasitasDnow[i]
                        maxVal = min(maxVal,maxVal2)
                        if maxVal > 0:
                            val = random.randint(1,maxVal)
                            node = {'value':val,'Pabrik':pabrik,'Distributor':i+1}
                            kapasitasDnow[i] += node['value']
                            self.dataPD.append(node)
             #       print('pengiriman Distrikbutor kini:')
             #       print(kapasitasDnow)