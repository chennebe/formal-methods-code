from z3 import *

def run(G):
	s = Solver()
	nodes = []
	weight = {}

	# gather nodes/weights in G
	for inlist in G:
		x = Bool('N'+str(inlist[0]))
		nodes.append(x)
		weight[x] = inlist[1]


	# function that returns true if there is an edge 
	#   between the first and second arg
	Edge = Function('Edge', BoolSort(), BoolSort(), BoolSort())
	# loop through list where i is a node
	for i in range(len(G)):
		e = [False]*len(G) 			# preinitialize all edges as false
		for j in G[i][2]: 			# loop through all edges listed for i
			e[j-1] = True 			# set edge to true

		print "Edge for N" + str(G[i][0])
		print e


		# something is wrong with the assertions created below
		for j in range(len(e)): 			# loop through edges, create assertion
			s.add(Edge(nodes[i], nodes[j]) == e[j])


	# assert that x and y implies Edge(x,y)
	for i in range(len(nodes)):
		for j in range(i+1, len(nodes)):
				s.add(Implies(And(nodes[i], nodes[j]), Edge(nodes[i], nodes[j]))) 
					# perhaps more than needed, Edge is bicon so only one need be tested

	print nodes
	print weight

	clique = None
	max_weight = 0
	while s.check() == sat:
		print(s.check())
		m = s.model()
		model_sum = 0
		for i in m:
			if m[i]:
				# this line doesn't work, need to find a different way to extract weight
				model_sum += weight[i]

		if model_sum > max_weight:
			clique = m
		s.add(Not(And([m[i] == m[i] for i in m])))

	print("Max weight: " + str(max_weight))
	print(clique)
			



print("In order to run this script, \
call the function 'run' with the \
list of lists representing the input \
as defined in the writeup.")

# test to save time...
'''G = [[1,2,[2,3,4,5]],
	[2,4,[1,4]],
	[3,4,[1,5]],
	[4,7,[1,2,5]],
	[5,7,[1,3,4]]]'''
