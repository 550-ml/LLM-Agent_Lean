import Mathlib

open Topology Filter Polynomial Set

-- 3
/--
For any positive integer $n$, let $\langle n \rangle$ denote the closest integer to $\sqrt{n}$. Evaluate $\sum_{n=1}^\infty \frac{2^{\langle n \rangle}+2^{-\langle n \rangle}}{2^n}$.
-/
theorem putnam_2001_b3
: ∑' n : Set.Ici 1, ((2 : ℝ) ^ (round (Real.sqrt n)) + (2 : ℝ) ^ (-round (Real.sqrt n))) / 2 ^ (n : ℝ) = ((3) : ℝ ) :=
sorry
