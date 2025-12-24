import Mathlib

-- fun k : ℝ => k ≥ 0
/--
For which real numbers $k$ does there exist a continuous function $f : \mathbb{R} \to \mathbb{R}$ such that $f(f(x)) = kx^9$ for all real $x$?
-/
theorem putnam_1979_a2
: ∀ k : ℝ, (∃ f : ℝ → ℝ, Continuous f ∧ ∀ x : ℝ, f (f x) = k*x^9) ↔ ((fun k : ℝ => k ≥ 0) : ℝ → Prop ) k :=
sorry
