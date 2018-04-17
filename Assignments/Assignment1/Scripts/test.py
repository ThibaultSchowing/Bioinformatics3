#!/usr/bin/python
#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
from RandomNetwork import RandomNetwork
from DegreeDistribution import DegreeDistribution

if __name__== "__main__":
    rand_net = RandomNetwork(10,5)
    rand_degree = DegreeDistribution(rand_net).getNormalizedDistribution()
    print(rand_degree)