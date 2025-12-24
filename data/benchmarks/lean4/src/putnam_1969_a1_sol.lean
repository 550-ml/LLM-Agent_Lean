import Mathlib

open Matrix Filter Topology Set Nat

-- {{x} | x : ℝ} ∪ {Set.Ici x | x : ℝ} ∪ {Set.Iic x | x : ℝ} ∪ {Set.Iio x | x : ℝ} ∪ {Set.Ioi x | x : ℝ} ∪ {Set.univ}
/--
What are the possible ranges (across all real inputs $x$ and $y$) of a polynomial $f(x, y)$ with real coefficients?
-/
theorem putnam_1969_a1
: {{z : ℝ | ∃ x : Fin 2 → ℝ, MvPolynomial.eval x f = z} | f : MvPolynomial (Fin 2) ℝ} = (({{x} | x : ℝ} ∪ {Set.Ici x | x : ℝ} ∪ {Set.Iic x | x : ℝ} ∪ {Set.Iio x | x : ℝ} ∪ {Set.Ioi x | x : ℝ} ∪ {Set.univ}) : Set (Set ℝ) ) :=
sorry
