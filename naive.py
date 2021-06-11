import csv
from copy import deepcopy
from os import supports_effective_ids

class Naive:
    divider = 3
    sepalL = []
    sepalW = []
    petalL = []
    petalW = []

    def __init__(self, case, tests) :
        self.fileCase = case
        self.fileTest = tests

    def read(self):
        with open(self.fileCase) as ficheiro:
            reader = csv.reader(ficheiro, delimiter=";")
            next(reader)
            for line in reader:
                self.sepalL.append(float(line[1]))
                self.sepalW.append(float(line[2]))
                self.petalL.append(float(line[3]))
                self.petalW.append(float(line[4]))

    def defineSize(self, j, data):
        j = int(len(data)/3)

        small = data[j-j]
        large = data[2*j]

        object = {
            'firstRange':small,
            'lastRange':large
        }

        return object


    def setSize(self, range, value):
        if value <= range['firstRange']:
            size = 'S'
        elif value > range['lastRange']:
            size = 'L'
        else:
            size = 'M'
    
        return size


    def discretize(self, fileName, fileAnalyze):
        discretizeSL = deepcopy(self.sepalL)
        discretizeSW = deepcopy(self.sepalW)
        discretizePL = deepcopy(self.petalL)
        discretizePW = deepcopy(self.petalW)

        discretizeSL.sort()
        discretizeSW.sort()
        discretizePL.sort()
        discretizePW.sort()

        dslRange = self.defineSize(self.divider, discretizeSL)
        dswRange = self.defineSize(self.divider,discretizeSW)
        dplRange = self.defineSize(self.divider, discretizePL)
        dpwRange = self.defineSize(self.divider, discretizePW)
        
        with open(fileAnalyze) as ficheiro:
            f = open(fileName, 'w', newline='')
            w = csv.writer(f)
            classes = []
            w.writerow(['Id;SepalLengthCm;SepalWidthCm;PetalLengthCm;PetalWidthCm;Species'])
            reader = csv.reader(ficheiro, delimiter=";")
            next(reader)
            for line in reader:
                id = line[0]
                dsl = self.setSize(dslRange, float(line[1]))
                dsw = self.setSize(dswRange, float(line[2]))
                dpl = self.setSize(dplRange, float(line[3]))
                dpw = self.setSize(dpwRange, float(line[4]))
                species = line[5]
                if species not in classes:
                    classes.append(species)
                w.writerow([id+';'+dsl+';'+dsw+';'+dpl+';'+dpw+';'+species])
        return classes
        
    def createP(self, classes):
        n = []
        for i in classes:
            object = {
                'species':i,
                'S':0,
                'M':0,
                'L':0,
                'total':0
            }
            n.append(object)
        return n

    def count(self, k, size, species):
        for i in range(len(k)):
            if k[i]['species'] == species:
                k[i][size] += 1
                k[i]['total'] += 1


    def probability(self, n):
        prob = []
        for k in n:
            object = {
                'class':k['species'],
                'S':k['S']/k['total'],
                'M':k['M']/k['total'],
                'L':k['L']/k['total']
            }
            prob.append(object)

        return prob

    def probabilityClass(self, n, total):
        prob = []
        for k in n:
            object = {
                'class':k['species'],
                'prob':k['total']/total
            }
            prob.append(object)

        return prob
        
    def setProbability(self, dslP, dswP, dplP, dpwP, classP):
        object = {
            'class':classP['class'],
            'prob': dslP * dswP * dplP * dpwP * classP['prob']
        }
        return object
        

    def learning(self, fileCase, classes, fileTest):
        hits = 0
        miss = 0
        dsl = self.createP(classes)
        dsw = self.createP(classes)
        dpl = self.createP(classes)
        dpw = self.createP(classes)
        
        with open(fileCase) as ficheiro:
            reader = csv.reader(ficheiro, delimiter=";")
            next(reader)
            total = 0
            for line in reader:
                total += 1
                if(line[0] != ''):
                    self.count(dsl, line[1], line[5])
                    self.count(dsw, line[2], line[5])
                    self.count(dpl, line[3], line[5])
                    self.count(dpw, line[4], line[5])

        dslP = self.probability(dsl)
        dswP = self.probability(dsw)
        dplP = self.probability(dpl)
        dpwP = self.probability(dpw)
        classP = self.probabilityClass(dsl, total)
        
        with open(fileTest) as ficheiro:
            total = 0
            reader = csv.reader(ficheiro, delimiter=";")
            next(reader)
            
            for line in reader:
                prob = []
                for i in range(len(dslP)):
                    probT = self.setProbability(dslP[i][line[1]],dswP[i][line[2]],dplP[i][line[3]],dpwP[i][line[4]],classP[i])
                    prob.append(probT)
            
                prob.sort(key = lambda d: d['prob'], reverse=True)
                print('A classe escolhida foi ', prob[0]['class'], ' e a classe é ', line[5])
                if prob[0]['class'] == line[5]:
                    hits += 1
                    print('Acerto da classe!')
                else:
                    miss += 1
                    print('Erro da classe!')
            
            print("A porcentagem de acerto foi de ",  round(hits/(hits+miss),2) * 100,'\n')
            print("Pressione enter para voltar ao menu")
            input()