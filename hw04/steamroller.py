## @Author Charles Henneberger (cihen)

from z3 import *

s = Solver()

Steamroller = DeclareSort('Steamroller')

x, y, z, u = Consts('x y z u', Steamroller)

Wolf = Function('Wolf', Steamroller, BoolSort())
Fox = Function('Fox', Steamroller, BoolSort())
Bird = Function('Bird', Steamroller, BoolSort())
Caterpillar = Function('Caterpillar', Steamroller, BoolSort())
Snail = Function('Snail', Steamroller, BoolSort())
Grain = Function('Grain', Steamroller, BoolSort())

s.add(Exists(x, Wolf(x)))
s.add(Exists(x, Fox(x)))
s.add(Exists(x, Bird(x)))
s.add(Exists(x, Caterpillar(x)))
s.add(Exists(x, Snail(x)))
s.add(Exists(x, Grain(x)))

Animal = Function('Animal', Steamroller, BoolSort())
Plant = Function('Plant', Steamroller, BoolSort())

s.add(Implies(Wolf(x), Animal(x)))
s.add(Implies(Fox(x), Animal(x)))
s.add(Implies(Bird(x), Animal(x)))
s.add(Implies(Caterpillar(x), Animal(x)))
s.add(Implies(Snail(x), Animal(x)))
s.add(Implies(Grain(x), Plant(x)))

Smaller = Function('Smaller', Steamroller, Steamroller, BoolSort())

s.add(Implies(And(Caterpillar(x), Bird(y)), Smaller(x,y)))
s.add(Implies(And(Snail(x), Bird(y)), Smaller(x,y)))
s.add(Implies(And(Bird(x), Fox(y)), Smaller(x,y)))
s.add(Implies(And(Fox(x), Wolf(y)), Smaller(x,y)))

Eats = Function('Eats', Steamroller, Steamroller, BoolSort())

s.add(Implies(And(Bird(x), Caterpillar(y)), Eats(x,y)))
s.add(Implies(Caterpillar(x), Exists(y, And(Plant(y), Eats(x,y)))))
s.add(Implies(Snail(x), Exists(y, And(Plant(y), Eats(x,y)))))

s.add(ForAll(x, Implies(Animal(x), \
	Or( \
		ForAll(y, Implies(Plant(y), Eats(x,y))), \
		ForAll(y, Implies(And( \
			Animal(y), \
			Smaller(y,x), \
			Exists(z, And(Plant(z), Eats(y,z)))), \
		Eats(x,y) ))))))

s.add(Implies(And(Wolf(x), Fox(y)), Not(Eats(x,y))))
s.add(Implies(And(Wolf(x), Grain(y)), Not(Eats(x,y))))
s.add(Implies(And(Bird(x), Snail(y)), Not(Eats(x,y))))

print(s.check())

a, b, c = Consts('a b c', Steamroller)
s.add(Exists(a, Exists(b, And( \
	Animal(a), \
	Eats(a,b), \
	ForAll(c, Implies(Grain(c), Eats(b,c)))))))

print(s.check())
print(s.model())
print(Wolf(a))
