import numpy as np
import subprocess
import time
import sys



def zconverter(w,mapp):
	#Finds the total length of map file
	L = len(mapp)
	count_vec = [];
	delta_vec = [];
	coord_vec = [];
	for k in range (0,L):
		#Creates a new ID for map name
		mapp_id = mapp[k];
		a = k + 1;
		if mapp_id[0:4] == 'NEXT':
			coord_vec = coord_vec + [mapp[a]]
			#Resets these values for each block
			count = 0;
			delta = [];
			#Checking all values in one block for the vales in signal
			while mapp_id[0:3] != 'END':
				a = a + 1;
				mapp_id = mapp[a];
				tester = mapp_id[0:17];
				if len(mapp_id) == 24:
					tester_value = int(float(mapp_id[19:23]));
				#Checks one value in map for all the values in signal file
				
				for key,value in w.items():
					checker = key 
					signal_value = float(value)
					if checker == tester:
						count = count + 1;
						delta = delta + [abs(signal_value - tester_value)];
						break
			if delta != []:
				delt = sum(delta)/len(delta);
				delta_vec = delta_vec + [delt];
			count_vec = count_vec + [count];		
	if delta_vec == []:
		print ('No Matching signals')
		return np.array([[0], [0]]);
	div = np.power(count_vec,0.5)
	winner = np.divide(delta_vec, div)

	#sorting the most possible positions
	winner_sort = np.argsort(winner)
	n_winner = 4;		#Can be adjusted (number of most likely positions to take into account)
	coord = [];

	#Gets the coordinates of the most possible positions
	for k in range (0,n_winner):
		winner = winner_sort[k];
		coordt = coord_vec[winner];
		coordtt = coordt.split(',');
		coordttt = [coordtt[0], coordtt[1]];
		a = float(coordttt[0]);
		b = float(coordttt[1]);
		coord = coord + [[a,b]]


	x_val = [];
	y_val = [];

	#Calulates the median of the most likey positions
	for k in range (0,n_winner):
		val = coord[k];
		x_val1 = val[0];
		y_val1 = val[1];
		x_val = x_val + [x_val1];
		y_val = y_val + [y_val1];

	xmed = np.median(x_val);
	ymed = np.median(y_val);

	limit = 1.5;		#Can be adjusted (Limit from the median)

	#Check if any of the most likly positions is way different than the others
	val_val = np.zeros(n_winner);
	for k in range (0,n_winner):
		val = coord[k];
		a = val[0];
		b = val[1];
		if xmed - limit < a < xmed + limit and ymed - limit < b < ymed + limit:
			val_val[k] = 1;

	# Calculate the average position of the most likely positions,
	# where the off positions have been removed
	xavg = 0;
	yavg = 0;
	avg_counter = 0;
	for k in range (0,n_winner):
		if val_val[k] == 1:
			val = coord[k];
			a = val[0];
			b = val[1];
			xavg = xavg + a;
			yavg = yavg + b;
			avg_counter = avg_counter + 1;
	if avg_counter == 0:
		print ('avg_counter = 0')
		return np.array([[0], [0]]);
	xavg = xavg/avg_counter;
	yavg = yavg/avg_counter;

	return np.array([[xavg], [yavg]]);
