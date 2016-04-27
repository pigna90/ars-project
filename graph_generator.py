import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from attributes_distance import *

def data_preparation(df):
	# Elimino tutti i valori nulli e \N
	iterDim = iter(df)
	next(iterDim)
	for dim in iterDim:
		df = df[df[dim] != "\\N"]
		df = df[df[dim] != "unknown"]
		df = df[df[dim] != "other"]
		df = df.dropna(subset=[dim], how="any")

	# Elimino attributi non necessari
	df = df.drop("diskSpace",1)
	df = df.drop("swap",1)
	df = df.drop("memory",1)
	df = df.drop("distroVersion",1)
	df["numCores"] = df["numCores"].astype(int)

	# Normalizzazione userId e numCores [0,1]
	df["userId"] = ((df["userId"] - df["userId"].min()) / (df["userId"].max() - df["userId"].min()))
	df["numCores"] = ((df["numCores"] - df["numCores"].min()) / (df["numCores"].max() - df["numCores"].min()))

	return df

# Plot distribuzione distanze in ordine crescente
# values - lista delle distanze
def plot_distances_distribution(values):
	l = [float(x) for x in values]
	l.sort()
	plt.plot(l)
	plt.title("Distances distribution")
	plt.ylabel("Distance")
	plt.xlabel("Edges")
	plt.show()

# Legge csv molto grande
# path - percorso file csv
def load_big_csv(path):
	tp = pd.read_csv(path, iterator=True, chunksize=1000)
	df = pd.concat(tp, ignore_index=True)
	df = df.drop_duplicates()
	return df
	
def main():
	dataset_path = "./data/lico_fixed.csv"
	graph_path = "/tmp/graph.csv"
	#cutted_graph_path = "./data/cutted_graph.csv"
	# Leggo csv contenente dataset Linux Counter
	df = pd.read_csv(dataset_path, skipinitialspace=True)

	# Preparo il dataset
	df = data_preparation(df)

	# Creo il grafo
	graph_distance(df.head(10),graph_path,0)

	# Leggo il grafo creato
	#df_graph = load_big_csv(graph_path)

	# Plot della distribuzione delle distanze
	#plot_distances_distribution(df_graph["Weight"].tolist())

	# Taglio del grafo
	#th = 0.7
	#df_graph = df_graph[df_graph["Weight"] <= 0.7]

	# Salvataggio del grafo tagliato
	#df_graph.to_csv(cutted_graph_path.split(".csv")[0] + "(" + str(th) + ").csv",index=False)
	
if __name__ == "__main__":
	main()
