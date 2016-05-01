import networkx as nx #The package which handles the graph objects
import matplotlib.pyplot as plt # Matplotlib is the default package for rendering the graphs
import operator
import numpy

    def degree_distribution(g):
        hist = nx.degree_histogram(g)     # get the degree histogram
        plt.plot(range(0, len(hist)), hist, ".")
        plt.title("Degree Distribution")
        plt.xlabel("Degree")
        plt.ylabel("#Nodes")
        plt.loglog()   #Draw LogLog distribution
        plt.show()     #show result
        plt.savefig("randomnetwork_distribution.png")   #save result





        #Return a random graph G_{n,p} (Erdős-Rényi graph, binomial graph).
        #Chooses each of the possible edges with probability p.
        #n (int) – The number of nodes.
        #p (float) – Probability for edge creation.

            g_ran = nx.erdos_renyi_graph(n, p)
            nx.draw(g)  #Draw Random Network
            plt.show()  #Show result
            degree_distribution(g_ran)
