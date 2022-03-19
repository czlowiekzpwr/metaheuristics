import matplotlib.pyplot as plt
import networkx as nx

class TSProblem():
    def display(self):
        for endnode in self.graph.nodes:
            for startnode in self.graph.nodes:
                if startnode == endnode:
                    print(0, end=" ")
                else:
                    print(self.graph.edges[startnode, endnode]["weight"], end=" ")
            print("")

    def printSolution(self, solution):
        print(solution)

    def drawSolution(self, solution):
        nx.draw_networkx(self.graph, pos={nod: self.graph.nodes[nod]["coords"] for nod in self.graph.nodes}, edgelist=[(solution[x],solution[x+1]) for x in range(0,len(solution)-1)] + [(solution[-1], solution[0])])
        plt.show()

    def getSolutionLength(self, solution):
        length = 0
        for edge in [(solution[x],solution[x+1]) for x in range(0,len(solution)-1)] + [(solution[-1], solution[0])]:
            length += self.graph.edges[edge]["weight"]
        return length
    
    def getPartialSolutionLength(self, solution):
        length = 0
        for edge in [(solution[x],solution[x+1]) for x in range(0,len(solution)-1)]:
            length += self.graph.edges[edge]["weight"]
        return length
    
    def getSolutionComparison(self, base, newsol):
        fx = self.getSolutionLength(newsol)
        fopt = self.getSolutionLength(base)
        return 100.0 * ((fx - fopt) / fopt)

