import pandas as pd
import numpy as np
from distance_matrix_generator import *

# Dataset albero distribuzioni linux
df_distro = pd.read_csv('./data/distro_parent.csv', skipinitialspace=True)
# Dataset distanze geografiche normalizzate [0,1]
df_geo = np.genfromtxt("./data/geo_distance_norm.csv", delimiter=",",dtype=str)

# Crea un arco completo simmetrico computando tutte le distanze
# tra i record del dataset df contenente le macchine linux.
# Salva nella forma "Source Target Type Weight" utilizzata da gephi 
# df - dataset contenente le macchine
# out_path - file in cui salvare il grafo
# index - indice del dataset da cui iniziare a calcolare gli archi
def graph_distance(df,out_path,index=0):
	
	values = df.values
	f = open(out_path,"a")
	for i_a in range(index,len(values)-1):
		for i_b in range(i_a+1,len(values)):
			ris = machine_distance((values[i_a],values[i_b]))
			f.write("%s %s Undirected %s\n" % (i_a,i_b,ris))
			#time.sleep(0.01)
	f.close()

# Calcola la distanza tra due macchine
# pair - tupla contenente le due macchine come lista di attributi
def machine_distance(pair):
	a = pair[0]
	b = pair[1]
	
	numCores_dist = abs(a[1] -b[1])
	kernel_dist = kernel_distance(a[2],b[2])
	class_dist = class_distance(a[3],b[3])
	cpu_dist = cpu_distance(a[4],b[4])
	country_dist = country_distance(a[5],b[5])
	architecture_dist = architecture_distance(a[6],b[6])
	distro_dist = distribution_dist(a[7],b[7])
	
	return (numCores_dist + kernel_dist + class_dist + country_dist + architecture_dist + distro_dist)

# Recupera da file la distanza precomputata tra due location
def country_distance(a,b,df=df_geo):
	for e in df:
		if a in e and b in e:
			return float(e[2])

# Calcola la distanza tra due stringhe a e b
# rappresentanti due CPU
def cpu_distance(a,b):
	return 1 - similarity_string(a,b,"matcher")

# Calcola la distanza tra due stringhe a e b
# rappresentanti due architetture
def architecture_distance(a,b):
	return 1 - similarity_string(a,b,"matcher")

# Calcola la distanza tra due classi di computer a e b
# utilizzando delle categorie che raggruppano classi simili
def class_distance(a,b):
	set1 = ["desktop","games","laptop","netbook","notebook","personal","workstation"]
	set2 = ["embedded","raspberry pi","smarphone","tablet"]
	set3 = ["server","server/workstation","workstation"]

	if a == b:
		return 0
	elif (a in set1 and b in set1) or (a in set2 and b in set2) or (a in set3 and b in set3):
		return 0.5
	else:
		return 1

# Calcola la distanza tra due distribuzioni utilizzando un albero
# delle derivazioni linux
def distribution_dist(a,b,df=df_distro):
	if a==b:
		return 0
	else:
		parent_a = df[df["distro"] == a]["parent"].iloc[0]
		parent_b = df[df["distro"] == b]["parent"].iloc[0]
		if a == parent_b or b == parent_a or parent_a == parent_b:
			return 0.3
		else:
			parent_a = df[df["distro"] == parent_a]["parent"].iloc[0]
			parent_b = df[df["distro"] == parent_b]["parent"].iloc[0]
			if parent_a == parent_b:
				return 0.6
			else:
				return 1

# Ritorna la distanza tra due kernel trasformandoli in numeri interi
# e calcolando la differenza
def kernel_distance(a,b):
	a_int_norm = norm_kernel(int("".join(str(a).replace("+","").split("."))))
	b_int_norm = norm_kernel(int("".join(str(b).replace("+","").split("."))))

	if (a.find("+") != -1) !=  (b.find("+") != -1):
		return abs(a_int_norm - b_int_norm) - norm_kernel(1)
	else:
		return abs(a_int_norm - b_int_norm)
		
# Normalizzazione del numero intero che rappresenta il kernel
# utilizzando il più alto valore e il più basso valore presenti
# nel dataset
# k - kernel da normalizzare
def norm_kernel(k):
	max_kernel = 34110
	min_kernel = 32
	return ((k-min_kernel)/(max_kernel-min_kernel))

# Ritorna due interi rappresentanti il più grande e più
# piccolo kernel come intero all'interno del dataset
# kernels - lista dei kernel
def min_max_kernel(kernels):
	kernels_int = [int("".join(str(x).replace("+","").split("."))) for x in kernels]
	return max(kernels_int),min(kernels_int)
