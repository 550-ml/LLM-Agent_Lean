import Mathlib

-- Note: this problem admits several possible correct solutions; this is the one shown on the solutions document
-- 181
/--
Let $a_0=1$, $a_1=2$, and $a_n=4a_{n-1}-a_{n-2}$ for $n \geq 2$. Find an odd prime factor of $a_{2015}$.
-/
theorem putnam_2015_a2
(a : ℕ → ℤ)
(abase : a 0 = 1 ∧ a 1 = 2)
(arec : ∀ n ≥ 2, a n = 4 * a (n - 1) - a (n - 2))
: Odd ((181) : ℕ ) ∧ ((181) : ℕ ).Prime ∧ ((((181) : ℕ ) : ℤ) ∣ a 2015) :=
sorry
