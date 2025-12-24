import Mathlib

open Set Topology Filter

-- fun (a, b) => (Real.exp (-1))*(b^b/a^a)^(1/(b-a))
/--
If $0 < a < b$, find $$\lim_{t \to 0} \left( \int_{0}^{1}(bx + a(1-x))^t dx \right)^{\frac{1}{t}}$$ in terms of $a$ and $b$.
-/
theorem putnam_1979_b2
: ∀ a b : ℝ, 0 < a ∧ a < b → Tendsto (fun t : ℝ => (∫ x in Icc 0 1, (b*x + a*(1 - x))^t)^(1/t)) (𝓝[≠] 0) (𝓝 (((fun (a, b) => (Real.exp (-1))*(b^b/a^a)^(1/(b-a))) : ℝ × ℝ → ℝ ) (a, b))) :=
sorry
