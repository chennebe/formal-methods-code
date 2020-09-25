## @Author Charles Henneberger (cihen)

from z3 import *

s = Tactic('qflia').solver()

A, B, C, D, E, F = Ints('A B C D E F')
At, Bt, Ct, Dt, Et, Ft = Ints('At Bt Ct Dt Et Ft')
End = Int('End')

s.add(A >= 0)
s.add(B >= 0)
s.add(C >= 0)
s.add(D >= 0)
s.add(E >= 0)
s.add(F >= 0)

s.add(At == 2)
s.add(Bt == 1)
s.add(Ct == 2)
s.add(Dt == 2)
s.add(Et == 7)
s.add(Ft == 5)

s.add(End == 14)

s.add(Or((A + At) <= C, (C + Ct) <= A))
s.add(Or((B + Bt) <= D, (D + Dt) <= B))
s.add(Or((B + Bt) <= E, (E + Et) <= B))
s.add(Or((E + Et) <= D, (D + Dt) <= E))
s.add(And(D + Dt <= F, E + Et <= F))
s.add(A + At <= B)
s.add(A <= End - At)
s.add(B <= End - Bt)
s.add(C <= End - Ct)
s.add(D <= End - Dt)
s.add(E <= End - Et)
s.add(F <= End - Ft)

print(s.check())
print(s.model())
