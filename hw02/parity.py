from z3 import *

p1, p2, p3, p4 = Bools('p1 p2 p3 p4')

phi = And( \
	Or(Not(p1), Not(p2), Not(p3), p4), \
	Or(p1, p2, p3, Not(p4)), \
	Or(Not(p1), Not(p2), p3, Not(p4)), \
	Or(p1, p2, Not(p3), p4), \
	Or(Not(p1), p2, Not(p3), Not(p4)), \
	Or(p1, Not(p2), p3, p4), \
	Or(p1, Not(p2), Not(p3), Not(p4)), \
	Or(Not(p1), p2, p3, p4) \
	)

psi = Or( \
	And(p1, p2, p3, p4), \
	And(Not(p1), Not(p2), Not(p3), Not(p4)), \
	And(p1, p2, Not(p3), Not(p4)), \
	And(Not(p1), Not(p2), p3, p4), \
	And(p1, Not(p2), p3, Not(p4)), \
	And(Not(p1), p2, Not(p3), p4), \
	And(p1, Not(p2), Not(p3), p4), \
	And(Not(p1), p2, p3, Not(p4)) \
	)

theta = ((((p1 == True) == (p4 == False)) == ((p1 == p2) == (p1 == p3))) == False)

a = Solver()
a.add(Not(phi == psi))
print a.check()

b = Solver()
b.add(Not(phi == theta))
print b.check()

c = Solver()
c.add(Not(psi == theta))
print c.check()
