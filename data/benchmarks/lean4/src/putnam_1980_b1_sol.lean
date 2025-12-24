import Mathlib

open Real

-- {c : ℝ | c ≥ 1 / 2}
/--
For which real numbers $c$ is $(e^x+e^{-x})/2 \leq e^{cx^2}$ for all real $x$?
-/
theorem putnam_1980_b1
(c : ℝ)
: (∀ x : ℝ, (exp x + exp (-x)) / 2 ≤ exp (c * x ^ 2)) ↔ c ∈ (({c : ℝ | c ≥ 1 / 2}) : Set ℝ ) :=
sorry
