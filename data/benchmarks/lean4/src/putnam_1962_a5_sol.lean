import Mathlib

-- fun n : ℕ => n * (n + 1) * 2^(n - 2)
/--
Evaluate in closed form \[ \sum_{k=1}^n {n \choose k} k^2. \]
-/
theorem putnam_1962_a5
: ∀ n ≥ 2, ((fun n : ℕ => n * (n + 1) * 2^(n - 2)) : ℕ → ℕ ) n = ∑ k ∈ Finset.Icc 1 n, Nat.choose n k * k^2 :=
sorry
