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
        plt.savefig("barabasinetwork_distribution.png")   #save result





#Return random graph using Barabási-Albert preferential attachment model.
#A graph of n nodes is grown by attaching new nodes each with m edges that are preferentially attached to existing nodes with high degree.
#n (int) – Number of nodes
#m (int) – Number of edges to attach from a new node to existing nodes

            g_bar = nx.barabasi_albert_graph(n,m)
            nx.draw(g_bar)   #Draw Barabasi Network
            plt.show()       # Show result
            degree_distribution(g_bar)
