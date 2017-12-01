#----------------------------------------------------#
#             Kalman filter 3.0
#
#   Copyright: Martin Skaldebo
#----------------------------------------------------#

import math
from numpy import identity
from numpy import array
from numpy import vstack
from numpy import random
import numpy as np 


def jacobmat(g,x,odom):
	#Jacobian through omplex step differentation
	#[z,J] = jacobian(f,x)
	#z = f(x)
	#J = f'(x)

	z = g(x,odom);
	n = np.size(x);
	m = np.size(z);
	A = np.zeros((m,n));
	v = n*np.spacing(1);
	x1 = np.zeros((n,))

	for k in range (0,n):
		x1 = x + 0j;
		x1[k] = x1[k] + v*1j;
		x2 = g(x1,odom);
		ll = x2.shape[0];
		for l in range (0,ll):
			x3 = x2[l,0];
			A[l,k] = x3.imag / v;

	return [z,A]


