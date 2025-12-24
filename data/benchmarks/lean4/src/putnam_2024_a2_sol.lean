import Mathlib

open Polynomial

-- {s • X + C a | (s : ℤˣ) (a : ℝ)}
/--
For which real polynomials $p$ is there a real polynomial $q$ such that
$p(p(x)) - x = (p(x) - x)^2q(x)$ for all real $x$?
-/
theorem putnam_2024_a2 :
    { p : Polynomial ℝ | ∃ (q : Polynomial ℝ),
      ∀ x, p.eval (p.eval x) - x = (p.eval x - x) ^ 2 * q.eval x } = (({s • X + C a | (s : ℤˣ) (a : ℝ)}) : Set ℝ[X] ) :=
  sorry
