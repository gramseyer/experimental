import numpy as np

from scipy import linalg

def state(i, j, cap):
	return i* cap + j
def run_sim(cap):
	states = cap * cap
	matrix = np.zeros((states+1, states))


	for i in range(0, cap):
		for j in range(0, cap):
			cur = state(i, j, cap)
			outdeg = 0
			if (i < cap-1):
				outdeg = outdeg + 1
			if (j < cap-1):
				outdeg = outdeg + 1
			if (i>0 and j >0):
				outdeg = outdeg + 1
			matrix[cur, cur] = -outdeg
			if (i > 0):
				matrix[cur, state(i-1, j, cap)] = 1
			if (j > 0):
				matrix[cur, state(i, j-1, cap)] = 1
			if (i < cap-1 and j < cap-1):
				matrix[cur, state(i+1, j+1, cap)] = 1
			matrix[states, cur] = 1
	#matrix[states, states] = 1

	rhs = np.zeros((states+1, 1))
	rhs[states, 0] = 1


	#print matrix
	#print rhs

	sols, err, _, _ = np.linalg.lstsq(matrix, rhs, rcond = None)
	print "comp. err is " + str(err)

	sols = sols - 1.0/states
	#print sols
	sols = np.abs(sols)
	print "stat err is " + str(np.sum(sols)/2)

cap = 1
while True:
	cap = cap + 1
	print "cap is " + str(cap)
	run_sim(cap)
