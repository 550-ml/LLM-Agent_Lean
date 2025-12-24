import Mathlib

-- (fun a b : ℝ => (Real.exp (a ^ 2 * b ^ 2) - 1) / (a * b))
/--
Evaluate $\int_0^a \int_0^b e^{\max\{b^2x^2,a^2y^2\}}\,dy\,dx$ where $a$ and $b$ are positive.
-/
theorem putnam_1989_a2
(a b : ℝ)
(abpos : a > 0 ∧ b > 0)
: ∫ x in Set.Ioo 0 a, ∫ y in Set.Ioo 0 b, Real.exp (max (b ^ 2 * x ^ 2) (a ^ 2 * y ^ 2)) = ((fun a b : ℝ => (Real.exp (a ^ 2 * b ^ 2) - 1) / (a * b)) : ℝ → ℝ → ℝ ) a b :=
sorry
