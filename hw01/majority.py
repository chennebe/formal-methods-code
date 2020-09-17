from z3 import *

x, y, z = Bools('x y z')

phi = And(Or(x,y),Or(x,z),Or(y,z))
psi = Or(And(x,y),And(x,z),And(y,z))

s = Solver()

s.add(phi==psi)

print s.check()