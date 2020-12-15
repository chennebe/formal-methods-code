# @author Charles Henneberger - cihen

from z3 import *
from random import randrange
from time import sleep

##
## from link in writeup for Problem 5
##
def shuffle(list):
	n = len(list)
	for i in range(n - 1):
		j = randrange(i, n-1) # i <= j < n
		value = list[i]
		list[i] = list[j]
		list[j] = value


def getDistinctRandomNumbers(inclusiveMin, exclusiveMax, amount):
	result = set()
	while len(result) != amount:
		result.add(randrange(inclusiveMin, exclusiveMax))
	
	return result


def getRandomElements(list, amount):
	length = len(list)
	amount = min(length, amount)
	if amount < 0.63212055882 * length:
		randomNumbers = getDistinctRandomNumbers(0, length, amount)
		result = [None]*amount
		i = 0
		for num in randomNumbers:
			result[i] = list[num]
			i+=1
		
		return result
	else:
		shuffle(list)
		return list[0:amount]
##
## End of code from link in writeup
##


def printBoard(n, Qs, Rs, model):
	print("Solution found!")
	row = "-"
	for i in range(n):
		row = row + "----"

	print(row)

	for i in range(n):
		cells = "|"
		for j in range(n):
			q = Qs[(i,j)]
			r = Rs[(i,j)]
			if is_true(model[q]):
				cells = cells + " Q |"
			elif is_true(model[r]):
				cells = cells + " R |"
			else:
				cells = cells + "   |"

		print(cells)
		print(row)


# n=board size
# sols=number of solutions wanted 
# exclude=list of constraints to skip, empty by default
def solve(n, sols=1, exclude=[]):
	if n < 3:
		print("n must be at least 3!")
		return

	if sols <= 0:
		print("sols must be positive!")
		return

	p = n / 3
	if n % 3 != 0: # to get ceiling
		p += 1

	print("Finding up to " + str(sols) + " solution(s) for a " + \
		str(n) + "x" + str(n) + " board...")

	nset = range(n)
	setI = getRandomElements(nset, p)
	setNotI = set(nset).difference(setI) # set without I

	Qs = {}
	Rs = {}
	s = Solver()

	for i in range(n):
		for j in range(n):
			key = (i,j)
			qname = "Q(" + str(i) + ", " + str(j) + ")"
			Qs[key] = Bool(qname)
			s.add(Or(Qs[key], Not(Qs[key])))

			rname = "R(" + str(i) + ", " + str(j) + ")"
			Rs[key] = Bool(rname)
			s.add(Or(Rs[key], Not(Rs[key])))

	# each constraint is a local function, called below

	# 1. There is a queen on each of the p selected rows:
	def P1(ss):
		for i in setI:
			clause = []
			for j in range(n):
				clause.append(Qs[(i,j)])

			ss.add(Or(clause))

	# 2. There is a rook on each of the remaining (n - p) rows:
	def P2(ss):
		for i in setNotI:
			clause = []
			for j in range(n):
				clause.append(Rs[(i,j)])

			ss.add(Or(clause))

	# 3. No position on the board contains both a queen and a knight:
	def P3(ss):
		for i in range(n):
			for j in range(n):
				ss.add(Implies(Qs[(i,j)], Not(Rs[(i,j)])))

	# 4. On every row i, if there is a queen in column j, 
	#    then there is no rook and no other queen on row i:
	def P4(ss):
		for i in range(n):
			for j in range(n):
				lhs = Qs[(i,j)]
				clause = []
				for k in range(n):
					if k != j:
						clause.append(And(Not(Qs[(i,k)]), Not(Rs[(i,k)])))

				ss.add(Implies(lhs, And(clause)))

	# 5. On every column j, if there is a queen in row i, 
	#    then there is no rook and no other queen on column j:
	def P5(ss):
		for i in range(n):
			for j in range(n):
				lhs = Qs[(i,j)]
				clause = []
				for k in range(n):
					if k != i:
						clause.append(And(Not(Qs[(k,j)]), Not(Rs[(k,j)])))

				ss.add(Implies(lhs, And(clause)))

	# 6. On every row i, if there is a rook in column j, 
	#    then there is no queen and no other rook on row i:
	def P6(ss):
		for i in range(n):
			for j in range(n):
				lhs = Rs[(i,j)]
				clause = []
				for k in range(n):
					if k != j:
						clause.append(And(Not(Qs[(i,k)]), Not(Rs[(i,k)])))

				ss.add(Implies(lhs, And(clause)))

	# 7. On every column j, if there is a rook in row i, 
	#    then there is no queen and no other rook on column j
	def P7(ss):
		for i in range(n):
			for j in range(n):
				lhs = Rs[(i,j)]
				clause = []
				for k in range(n):
					if k != i:
						clause.append(And(Not(Qs[(k,j)]), Not(Rs[(k,j)])))

				ss.add(Implies(lhs, And(clause)))

	# 8. On every diagonal, if there is a queen, 
	#    there is no rook and no other queen on the same diagonal:
	def P8(ss):
		for i in range(n):
			for j in range(n):
				lhs = Qs[(i,j)]
				clause = []
				for k in range(n):
					for ll in range(n):
						if i != k and j != ll and (k - ll) == (i - j):
							clause.append(And(Not(Qs[(k,ll)]), Not(Rs[(k,ll)])))

				s.add(Implies(lhs, And(clause)))

	# 9. On every antidiagonal, if there is a queen, 
	#    there is no rook and no other queen on the same antidiagonal:
	def P9(ss):
		for i in range(n):
			for j in range(n):
				lhs = Qs[(i,j)]
				clause = []
				for k in range(n):
					for ll in range(n):
						if i != k and j != ll and (k + ll) == (i + j):
							clause.append(And(Not(Qs[(k,ll)]), Not(Rs[(k,ll)])))

				s.add(Implies(lhs, And(clause)))

	# list of all constraint functions
	wffs = [P1, P2, P3, P4, P5, P6, P7, P8, P9]

	# executes constraint at index i if i+1 was not in the exclude list
	for i in range(9):
		if i+1 not in exclude:
			wffs[i](s)

	# loop until unsat or sols solutions found
	for i in range(sols):
		if s.check() == sat:
			m = s.model()
			printBoard(n, Qs, Rs, m)
			s.add(Not(And([e() == m[e] for e in m])))
		else:
			print("Only found " + str(i) + " solution(s) for I = " + str(setI))
			return


print("Rooks & Queens")
print("==============")
print("To run this program, call solve(n)" + \
	" where n is the size of the board. You can also " + \
	"specify a number of solutions to try and find by calling " + \
	"solve(n, sols) where sols is the number of solutions.")
print("Do note that the program will randomly generate a set I, " + \
	"so it is possible that there is no solution for a given call.")
