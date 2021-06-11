#Karín Morais
from knn import *
from naive import *

cases = 'iris-cases.csv'
tests = 'iris-tests.csv'
discretizeC = 'discretizeC.csv'
discretizeT = 'discretizeT.csv'

x = 1

while x != 0:
    print('Escolha uma opção!\n1 - Algoritmo KNN\n2 - Algoritmo Naive\n0 - sair')
    x = int(input())

    if x == 1:
        knn = KNN()
        knn.read(tests, knn.flowersTests)
        knn.read(cases, knn.flowersCases)
        knn.learning()
    elif x == 2:
        naive = Naive(cases, tests)
        naive.read()
        classes = naive.discretize(discretizeC, cases)
        naive.discretize(discretizeT, tests)
        naive.learning(discretizeC, classes, discretizeT)
    else:
        print('Até Mais!\n')