import networkx as nx
import re
import numpy as np
import tspdatahandlers
import tsproblem

specparams = ["NAME", "TYPE", "COMMENT", "DIMENSION", "CAPACITY", "EDGE_WEIGHT_TYPE", "EDGE_WEIGHT_FORMAT", "EDGE_DATA_FORMAT", "NODE_COORD_TYPE", "DISPLAY_DATA_TYPE", "EOF"]
dataparams = ["NODE_COORD_SECTION", "DEPOT_SECTION", "DEMAND_SECTION", "EDGE_DATA_SECTION", "FIXED_EDGES_SECTION", "DISPLAY_DATA_SECTION", "TOUR_SECTION", "EDGE_WEIGHT_SECTION", "EOF"]

class LoadedTSProblem(tsproblem.TSProblem):
    def __init__(self, tspin):
        if "NAME" in tspin:
            self.name = tspin["NAME"]
        if tspin["TYPE"] == "TSP":
            self.directed = False
        elif tspin["TYPE"] == "ATSP":
            self.directed = True
        else:
            raise ValueError()
        if "COMMENT" in tspin:
            self.comment = tspin["COMMENT"]
        self.size = int(tspin["DIMENSION"])

        if self.directed:
            self.graph = nx.complete_graph(range(1,self.size+1), create_using=nx.DiGraph())
        else:
            self.graph = nx.complete_graph(range(1,self.size+1))
        
        if tspin["EDGE_WEIGHT_TYPE"] == "EUC_2D":
            for fnode in range(self.size):
                for snode in range(self.size):
                    if fnode != snode:
                        myweight = 0.0
                        for dim in range(tspin["NODE_COORD_SECTION"].shape[1]):
                            myweight += pow((tspin["NODE_COORD_SECTION"][fnode][dim] - tspin["NODE_COORD_SECTION"][snode][dim]),2)
                        myweight = pow(myweight, 0.5)
                        self.graph.edges[fnode+1, snode+1]["weight"] = int(round(myweight))
                self.graph.nodes[fnode+1]["coords"] = tspin["NODE_COORD_SECTION"][fnode]

        if tspin["EDGE_WEIGHT_TYPE"] == "EXPLICIT":
            for fnode in range(self.size):
                for snode in range(self.size):
                    if fnode != snode:
                        self.graph.edges[fnode+1, snode+1]["weight"] = int(tspin["EDGE_WEIGHT_SECTION"][fnode][snode])
                if "DISPLAY_DATA_SECTION" in tspin:
                    self.graph.nodes[fnode+1]["coords"] = tspin["DISPLAY_DATA_SECTION"][fnode]


def load(filename):
    infile = open(filename, "r")

    inline = infile.readline()
    tspfile = {}
    tagfound = True
    while tagfound:
        tagfound = False
        for tagname in specparams:
            if inline.startswith(tagname):
                tspfile[tagname] = "".join(re.split(r"[ :]+", inline, maxsplit=1)[1:]).rstrip()
                tagfound = True
                break
        if tagfound:
            inline = infile.readline()

    while inline != "":
        for tagname in dataparams:
            if inline.startswith(tagname):
                if tagname in tspdatahandlers.section_fmap:
                    tspfile[tagname] = tspdatahandlers.section_fmap[tagname](tspfile, infile)
                    break
        inline = infile.readline()

    return LoadedTSProblem(tspfile)


def loadSolution(fname):
    infile = open(fname, "r")
    inline = infile.readline()
    solution = []
    while (inline != ""):
        if inline.startswith("TOUR_SECTION"):
            solution = tspdatahandlers.tourData("", infile)
        inline = infile.readline()
    return solution[0]




        



