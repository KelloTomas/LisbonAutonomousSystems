#----------------------------------------------------#
#             Kalman filter 3.0
#
#   Copyright: Martin Skaldebo
#----------------------------------------------------#
from numpy.linalg import inv
from jacobmat import jacobmat
import numpy as np
from numpy import identity

def ekf(f,x,P,h,z,Q,R,n,odom):
	#print(x)
	[x1,A] = jacobmat(f,x,odom);
	[z1,H] = jacobmat(h,x1,odom);

	# Creating the transpose matrices
	A = np.matrix(A)
	H = np.matrix(H)

	A1 = A.transpose();
	H1 = H.transpose();

	#----------------------------------------------------#
	#			Predict step

	#	Predicting the P
	#	P = A*P*A'+ Q;
	P = A*P*A1 + Q;

	#----------------------------------------------------#
	#			Update step

	#	G = (P*H')/(H*P*H'+R);
	
	G = (P*H1)*inv(H*P*H1+R)
	x = x1 + G*(z-z1);

	#	P = (eye(n)-G*H)*P;
	P = (identity(n)-G*H)*P


	return [x, P]