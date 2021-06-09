from knn import *


alo = KNN()

alo.read('iris-tests.csv', alo.flowersTests)
alo.read('iris-cases.csv', alo.flowersCases)
alo.learning()