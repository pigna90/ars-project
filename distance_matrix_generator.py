import pandas as pd
import numpy as np
import distance
from difflib import SequenceMatcher
from itertools import combinations_with_replacement
from geopy.geocoders import ArcGIS
from geopy.distance import vincenty
import time

# Similarità tra due stringhe utilizzando
# la misura matcher o sorensen
def similarity_string(a,b,measure):
	a = a.lower()
	b = b.lower()
	measure = measure.lower()
	if (measure == "matcher"):
		return SequenceMatcher(None,a,b).ratio()
	elif (measure == "sorensen"):
		return 1 - distance.sorensen(a, b)
	else:
		return 0

# Calcola la distanza in km tra tutte le location della lista countries
# e salva il risultato su file.
# es. Italia,Romania 1030
# countries - lista delle locations
# out_path - percorso in cui salvare il risultato
def geo_distance(countries,out_path):
	in_file = open(out_path,"a")
	for pair in list(combinations_with_replacement(countries,2)):
		a = pair[0]
		b = pair[1]
		geolocator = ArcGIS(timeout=None)
		loc1 = geolocator.geocode(a)
		loc2 = geolocator.geocode(b)
		time.sleep(1)
		dist = vincenty(loc1[1],loc2[1]).kilometers

		# Salvo ogni distanza su file 
		in_file.write("%s,%s,%s\n" % (a,b,dist))
	in_file.close()

# Crea un file contenente la lista delle cpu confrontate con una lista
# di cpu conosciute e relativa similarità.
# es: intl i3782 x -> Intel i3782 @3.00 Ghz
# cpu - lista delle cpu
# known_cpu - lista delle cpu conosciute
# out_path - file in cui salvare il risultato
# sim -  tipo di matching da effettuare tra le stringhe
# th - threshold matching
def class_matching(cpu,known_cpu,out_path,sim="matcher",th=0):

	in_file = open(out_path,"w")
	for a in cpu:
		candidate=""
		for b in known_cpu:
			if (similarity_string(a,b,sim) >= th):
				if (similarity_string(a,b,sim) > similarity_string(a,candidate,sim)):
					candidate=b
		in_file.write("%s,%s,%s\n" % (a,candidate,similarity_string(a,candidate,sim)))
	in_file.close()

def main():
	pass

if __name__ == "__main__":
	main()
