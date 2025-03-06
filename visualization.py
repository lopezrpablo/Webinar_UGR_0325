from music21 import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
	

def activityPlot(s):

	out = dict()
	for m, i in enumerate(s.recurse().getElementsByClass('Measure')):
		n_notes = len(i.notes)
		out[m+1] = n_notes

	x = out.keys()
	y = out.values()
        
	plt.fill_between(x, y)
	plt.xlabel('Número de compás')
	plt.ylabel('Número de ataques / compás')

	plt.show()

def activityHeatMap(s):

	file2 = s.recurse().getElementsByClass('Part')
	arr = pd.DataFrame()
	partNames = list()

	for i in file2:
		partNames.append(i.partName)
		out = dict()
		for m, i in enumerate(s.recurse().getElementsByClass('Measure')):
			n_notes = len(i.notes)
			out[m+1] = n_notes
		x = out.keys()
		data2 = out.values()
		arr = pd.concat([arr, pd.Series(data2)], axis=1)
	arr.columns = partNames

	fig, ax = plt.subplots()
	im = ax.imshow(arr.T, cmap="Blues")

	ax.set_xticks(np.arange(len(x)), labels=x)
	ax.set_yticks(np.arange(len(partNames)), labels=partNames)

	plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
	                 rotation_mode="anchor")

	for i in range(len(x)):
		for j in range(len(partNames)):
			text = ax.text(i, j, arr.iloc[i, j], ha="center", va="center", color="w")

	ax.set_title("Número de ataques / compás en las diferentes voces")
	fig.tight_layout()
	plt.show()

def melodicContour(pitches):
	offsets_list = list()
	note_list = list()
	dif = None
	for i in pitches:
	    try:
	        note_list.append(i.pitch.midi)
	        if dif is None:
	            dif = i.activeSite.offset + i.offset
	        offsets_list.append(i.activeSite.offset + i.offset - dif)
	            
	    except:
	        continue

	normalizer = MinMaxScaler(feature_range=(0, 1))
	time_scaled = normalizer.fit_transform([[x] for x in note_list])
	pitch_scaled = normalizer.fit_transform([[x] for x in offsets_list])

	plot = plt.plot(pitch_scaled, time_scaled)
	f = plt.figure()
	f.set_figwidth(4)
	f.show()