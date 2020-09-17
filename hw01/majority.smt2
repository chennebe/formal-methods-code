(declare-const x Bool)
(declare-const y Bool)
(declare-const z Bool)

(define-fun phi ((x Bool) (y Bool) (z Bool)) Bool
	(and
		(and
			(or x y)
			(or x z)
		)
		(or y z)
	)
)

(define-fun psi ((x Bool) (y Bool) (z Bool)) Bool
	(or
		(or
			(and x y)
			(and x z)
		)
		(and y z)
	)
)

(assert (= (phi x y z) (psi x y z)))

(check-sat)
