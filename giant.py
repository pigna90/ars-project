#The package which handles the graph objects
import networkx as nx

# Matplotlib is the default package for rendering the graphs
try:
    import matplotlib.pyplot as plt
except:
    raise

import math
import operator
import numpy

try:
    from networkx import graphviz_layout
    layout=nx.graphviz_layout
except ImportError:
    print("PyGraphviz not found; drawing with spring layout; will be slow.")
    layout=nx.spring_layout



    # read graph from edgelist file in csv format
    # filename input will be file path
    def read_graph(filename):
        g = nx.Graph()
        f = open(filename)
        for l in f:
            l = l.rstrip().replace(" ", ";").replace(",", ";").replace("\t", ";").split(";")
            g.add_edge(l[0], l[1])
        return g



    #Degree distribution
    def degree_distribution(g):
        # get the degree histogram
        hist = nx.degree_histogram(g)

        plt.plot(range(0, len(hist)), hist, ".")
        plt.title("Degree Distribution")
        plt.xlabel("Degree")
        plt.ylabel("#Nodes")
        plt.loglog()  #Draw LogLog distribution
        plt.savefig("distr_log_giant_015.png")
        plt.show()#show result



  # compute network characteristics
    def write_network_characteristics(g):
        nodes = len(g.nodes())
        edges = len(g.edges())
        avg_degree = float(2*edges)/nodes
        max_conn = (nodes*(nodes-1))/2
        clustering = nx.average_clustering(g)
        density = nx.density(g)
        diameter = nx.diameter(g)
        a_p_l = nx.average_shortest_path_length(g)
        conn = nx.is_connected(g)
        n_comp_con = nx.number_connected_components(g)
        # write them on file
        out = open("statistics_giant.csv", "w")
        out.write("#Nodes,#Edges,Avg_Degree, Max Connection, Clustering Coefficient, Density, Diameter , Average Shortest Path ,  Is Connected? , Number Connected Component\n")
        out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (nodes, edges, avg_degree , max_conn, clustering, density ,diameter ,a_p_l, conn , n_comp_con))

        g = read_graph("dataset/cutted_graph(0.15).csv")

        degree_distribution(g0)

        #Extract max Giant component
        cc=sorted(nx.connected_component_subgraphs(g), key = len, reverse=True)
        g0=gcc[0]

        write_network_characteristics(g0)
