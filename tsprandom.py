import networkx as nx
import numpy as np
import tsproblem
import random

class RandomTSProblem(tsproblem.TSProblem):
    def __init__(self, nodes=20, symetric=True):
        self.name = "Random TSP problem"
        self.directed = (not symetric)
        self.comment = "Random {0} problem with {1} nodes".format("symetric" if symetric else "asymetric", nodes)
        self.size = nodes
        if self.directed:
            self.graph = nx.complete_graph(range(1,self.size+1), create_using=nx.DiGraph())
        else:
            self.graph = nx.complete_graph(range(1,self.size+1))
        if self.directed:
            for nodestart in self.graph.nodes:
                for nodeend in self.graph.nodes:
                    if nodestart != nodeend:
                        self.graph.edges[nodestart, nodeend]["weight"] = random.randrange(1,10000)
        else:
            for node in self.graph.nodes:
                self.graph.nodes[node]["coords"] = [random.uniform(-1000.0, 1000.0) for x in range(2)]
            for nodestart in self.graph.nodes:
                for nodeend in self.graph.nodes:
                    if nodestart != nodeend:
                        myweight = 0.0
                        for dim in range(2):
                            myweight += pow((self.graph.nodes[nodestart]["coords"][dim] - self.graph.nodes[nodeend]["coords"][dim]),2)
                        myweight = pow(myweight, 0.5)
                        self.graph.edges[nodestart, nodeend]["weight"] = int(round(myweight))


