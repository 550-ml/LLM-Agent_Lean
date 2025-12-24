import Mathlib

open RingHom Set

-- RatFunc.X / (1 - RatFunc.X)
/--
Find $\sum_{n=0}^{\infty} \frac{x^{2^n}}{1 - x^{2^{n+1}}}$ as a rational function of $x$ for $x \in (0, 1)$.
-/
theorem putnam_1977_a4 :
    ∀ x ∈ Ioo 0 1,
      ((RatFunc.X / (1 - RatFunc.X)) : RatFunc ℝ ).eval (id ℝ) x = ∑' n : ℕ, x ^ 2 ^ n / (1 - x ^ 2 ^ (n + 1)) :=
  sorry
