import csv
import math
import json

class KNN:
    k = 3
    flowersCases = []
    flowersTests = []
    classes = []
    
    def read(self, file, data):
        with open(file) as ficheiro:
            reader = csv.reader(ficheiro, delimiter=";")
            next(reader)
            for line in reader:
                if line[5] not in self.classes:
                    self.classes.append(line[5])
                object = {
                    'id':line[0],
                    'sepalLength':float(line[1]),
                    'sepalWidth':float(line[2]),
                    'petalLength':float(line[3]),
                    'petalWidth':float(line[4]),
                    'species':line[5]
                }
                data.append(object)
                
    def euclideanDistance(self, flowerTest, flowerCase):
        y = (((flowerTest['sepalLength'] - flowerCase['sepalLength'])**2) 
        + ((flowerTest['sepalWidth'] - flowerCase['sepalWidth'])**2) 
        + ((flowerTest['petalLength'] - flowerCase['petalLength'])**2) 
        + ((flowerTest['petalWidth'] - flowerCase['petalWidth'])**2))

        return math.sqrt(y)

    def learning(self):
        hits = 0
        miss = 0
        for flowerTest in self.flowersTests:
            distances = []
            for flowerCase in self.flowersCases:
                distance = self.euclideanDistance(flowerTest, flowerCase)
                object = {
                    'distance':distance,
                    'speciesCase':flowerCase['species'],
                    'speciesTest':flowerTest['species']
                }
                distances.append(object)
            distances.sort(key = lambda d: d['distance'])
            decision = []
            for k in range(len(self.classes)):
                object = {
                    'class':self.classes[k],
                    'count':0
                }
                decision.append(object)
            for k in range(self.k):
                for i in decision:
                    if(distances[k]['speciesCase'] == i['class']):
                        i['count'] += 1
            decision.sort(key = lambda d: d['count'], reverse=True)
            print("A classe definida foi ", decision[0]['class'], " e a classe correta é ", flowerTest['species'])
            if(decision[0]['class'] == flowerTest['species']):
                print("Acerto da classe!")
                hits += 1
            else:
                print("Erro da classe!")
                miss += 1
        print("A porcentagem de acerto foi de ",  round(hits/(hits+miss),2) * 100,"\n")
        print("Pressione enter para voltar ao menu")
        input()
            

                