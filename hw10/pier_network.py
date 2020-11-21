# @author Charles Henneberger - cihen

# encode hard constraints as rules to follow
# with result, score is number of nodes that are false 
#		(technically only free nodes matter, but pier and blocked nodes will be the same in all solutions)
# add new constraint that score must be better
# return last model that Z3 produces

from z3 import *


def pier_solver(dimms, pierP, blockedP):
	m = dimms[0]
	n = dimms[1]

	s = Solver()

	# positions can be true or false
	positions = {}
	for i in range(m+2):
		for j in range(n+2):
			name = str(i) + "-" + str(j)
			key = (i,j)
			positions[(i,j)] = Bool(name)
			s.add(Or(positions[key]==True, positions[key]==False))


	# all piers must be true
	for p in pierP:
		#name = str(p[0]) + "-" + str(p[1])
		s.add(positions[p]==True)

	# all blocked must be false
	for b in blockedP:
		#name = str(b[0]) + "-" + str(p[1])
		s.add(positions[b]==False)

	# all piers must have exactly one neighbor
	for p in pierP:
		name = str(p[0]) + "-" + str(p[1])
		i = p[0]
		j = p[1]

		a = positions[(i+1, j)]
		b = positions[(i-1, j)]
		c = positions[(i, j+1)]
		d = positions[(i, j-1)]

		# this part is incorrect, it does not correctly force piers to have a neighbor
		s.add(Or(a==False, b==False, c==False, d==False))
		s.add(Or(a==False, b==False, c==False, d==True))
		s.add(Or(a==False, b==False, c==True, d==False))
		s.add(Or(a==False, b==True, c==False, d==False))
		s.add(Or(a==True, b==False, c==False, d==False))
		s.add(Or(a==False, b==False, c==True, d==True))
		s.add(Or(a==False, b==True, c==False, d==True))
		s.add(Or(a==False, b==True, c==True, d==False))
		s.add(Or(a==True, b==False, c==False, d==True))
		s.add(Or(a==True, b==False, c==True, d==False))
		s.add(Or(a==True, b==True, c==False, d==False))
		s.add(Or(a==True, b==True, c==True, d==True))

	# all piers in free must have 2 or more neighbors
	# free inferred from double loop where i-j is not in 
	for i in range(1,m+1):
		for j in range(1,n+1):
			# i = p[0]
			# j = p[1]
			test = (i,j)
			if (test not in pierP) and (test not in blockedP):
				q = positions[(i, j)]
				a = positions[(i+1, j)]
				b = positions[(i-1, j)]
				c = positions[(i, j+1)]
				d = positions[(i, j-1)]

				s.add(Or(q==False, a==True, b==True, c==True, d==True))
				s.add(Or(q==False, a==False, b==True, c==True, d==True))
				s.add(Or(q==False, a==True, b==False, c==True, d==True))
				s.add(Or(q==False, a==True, b==True, c==False, d==True))
				s.add(Or(q==False, a==True, b==True, c==True, d==False))
	# there is also something wrong here, it does not force the result to be one connected component

	model = None
	score = m * n
	if s.check() == unsat:
		print("No satisfiable network...")
		quit()

	while s.check() == sat:
		scoretry = 0
		m = s.model()
		for v in m:
			if m[v]:
				scoretry += 1
		if scoretry < score:
			model = m
			score = scoretry
		s.add(Not(And([m[i] == m[i] for i in m])))

	print("Model using " + str(score) + " nodes:")
	for v in model:
		if model[v]:
			print(v)


print("You can call the function \"pier_solver\" with the arguments as defined in the hw10 document.")
print("As an example, we will run the example given in the writeup now.")

dimms = (6,10)
piers = [(1,1),(2,7),(3,3),(3,8),(6,8)]
blocked = [(2,3),(2,5),(2,8),(4,4),(4,5),(4,9),(5,5),(6,1)]
pier_solver(dimms, piers, blocked)
