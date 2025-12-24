import Mathlib

open Set

-- {Polynomial.X}
/--
Determine all polynomials $P(x)$ such that $P(x^2 + 1) = (P(x))^2 + 1$ and $P(0) = 0$.
-/
theorem putnam_1971_a2
    (P : Polynomial ℝ) :
    (P.eval 0 = 0 ∧ (∀ x : ℝ, P.eval (x^2 + 1) = (P.eval x)^2 + 1)) ↔ P ∈ (({Polynomial.X}) : Set (Polynomial ℝ) ) :=
  sorry
