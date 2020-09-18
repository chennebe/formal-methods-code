(declare-const p1 Bool)
(declare-const p2 Bool)
(declare-const p3 Bool)
(declare-const p4 Bool)

; I don't know if declare + assert (as seen in hw01 solution) is better,
; but this style works too

; CNF
; dnf converted to cnf by creating dnf of false cases, negating all terms,
; and switching and to or and vice versa
(define-fun phi ((p1 Bool) (p2 Bool) (p3 Bool) (p4 Bool)) Bool
    (and
      (or (not p1) (not p2) (not p3) p4)
      (or p1 p2 p3 (not p4))
      (or (not p1 ) (not p2) p3 (not p4))
      (or p1 p2 (not p3) p4)
      (or (not p1) p2 (not p3) (not p4))
      (or p1 (not p2) p3 p4)
      (or p1 (not p2) (not p3) (not p4))
      (or (not p1) p2 p3 p4)
    )
)

; DNF
; "or-ing" of all true cases
(define-fun psi ((p1 Bool) (p2 Bool) (p3 Bool) (p4 Bool)) Bool
  (or
    (and p1 p2 p3 p4)
    (and (not p1) (not p2) (not p3) (not p4))
    (and p1 p2 (not p3) (not p4))
    (and (not p1) (not p2) p3 p4)
    (and p1 (not p2) p3 (not p4))
    (and (not p1) p2 (not p3) p4)
    (and p1 (not p2) (not p3) p4)
    (and (not p1) p2 p3 (not p4))
  )
)

; biconditional
; top pair is T if p1 and p4 are different, F otherwise.
; bottom pair is T if p1 = p2 = p3, false otherwise.
(define-fun theta ((p1 Bool) (p2 Bool) (p3 Bool) (p4 Bool)) Bool
    (=
      (=
        (=
          (= p1 true)
          (= p4 false)
        )
        (=
          (= p1 p2)
          (= p1 p3)
        )
      )
      false
    )
)

; I was not sure if this is the correct way to check multiple different
; assertions, but I saw a tutorial do this
(push)
(assert (not (= (phi p1 p2 p3 p4) (psi p1 p2 p3 p4))))
(check-sat)
(pop)

(push)
(assert (not (= (phi p1 p2 p3 p4) (theta p1 p2 p3 p4))))
(check-sat)
(pop)

(push)
(assert (not (= (psi p1 p2 p3 p4) (theta p1 p2 p3 p4))))
(check-sat)
