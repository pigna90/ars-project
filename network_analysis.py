import networkx as nx
import matplotlib.pyplot as plt
import operator
import numpy

# read graph from edgelist file in csv format
# filename input will be file path
def read_graph(filename):
    # read graph from edgelist file
    g = nx.Graph()
    f = open(filename)
    for l in f:
        l = l.rstrip().replace(" ", ";").replace(",", ";").replace("\t", ";").split(";")
        g.add_edge(l[0], l[1])
    return g

 # compute network characteristics
def write_network_characteristics(g):
    nodes = len(g.nodes())
    edges = len(g.edges())
    avg_degree = float(2*edges)/nodes
    max_conn = (nodes*(nodes-1))/2
    clustering = nx.average_clustering(g)
    density = nx.density(g)
    conn = nx.is_connected(g)
    n_comp_con = nx.number_connected_components(g)

    # write them on file
    out = open("statistics.csv", "w")
    out.write("Nodes,Edges,Avg_degree, Massime connessioni , Clustering,Density,  Is Connected? , Number Connected Component\n")
    out.write("%s,%s,%s,%s,%s, %s,%s, %s\n" % (nodes, edges, avg_degree , max_conn, clustering, density ,conn , n_comp_con))



#Degree distribution
    def degree_distribution(g):
        hist = nx.degree_histogram(g)  # get the degree histogram
        plt.plot(range(0, len(hist)), hist, ".")
        plt.title("Degree Distribution")
        plt.xlabel("Degree")
        plt.ylabel("#Nodes")
        plt.loglog()  #Draw LogLog distribution
        plt.savefig("network_distribution.png")
        plt.show()#show result




   # The degree centrality for a node v is the fraction of nodes it is connected to.
   # Closeness centrality of a node u is the reciprocal of the sum of the shortest path distances from u to all n-1 other nodes
   # Betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v

    def get_centrality(g):
    # compute centrality
    bt = nx.betweenness_centrality(g)
    deg_cent = nx.degree_centrality(g)
    clo = nx.closeness_centrality(g)
    # order nodes by decreasing centrality
    bt_sorted = sorted(bt.items(), key=operator.itemgetter(1), reverse=True)
    deg_cent_sorted = sorted(deg_cent.items(), key=operator.itemgetter(1), reverse=True)
    clo_sorted = sorted(clo.items(), key=operator.itemgetter(1), reverse=True)
    # Print the results betweenness
    out = open("betweenness.csv", "w")
    out.write("Node,Betweenness\n")
    for (node, betweenness) in bt_sorted:
        out.write("%s,%s\n" % (node, betweenness))
        out.flush()
    # Print the results closeness
    out = open("closeness.csv", "w")
    out.write("Node,Closeness\n")
    for (node, closeness) in clo_sorted:
        out.write("%s,%s\n" % (node, closeness))
        out.flush()
    # Print the results Degree Centrality
    out = open("deg_cent.csv", "w")
    out.write("Node,Degree Centrality\n")
    for (node, deg_cent) in deg_cent_sorted:
        out.write("%s,%s\n" % (node, deg_cent))
        out.flush()



        #Draw Network
        def draw_connected_components(g):
            # get the connected components
            cc = nx.connected_components(g)
            i = 0
            for c in cc:
                # extract the subgraph identifying the actual component
                sub = g.subgraph(c)
                # plot only components having at least 3 nodes
                if len(sub) > 3:
                    nx.draw(sub)
                    plt.show()

            g = read_graph("dataset/cutted_graph(0.15).csv")

            write_network_characteristics(g)

            degree_distribution(g)

            get_centrality(g)

            draw_connected_components(g)
