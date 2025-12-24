import Mathlib

open Metric Set EuclideanGeometry

-- (3, 1444)
/--
Find the length of the longest possible sequence of equal nonzero digits (in base 10) in which a perfect square can terminate. Also, find the smallest square that attains this length.
-/
theorem putnam_1970_a3
(L : ℕ → ℕ)
(hL : ∀ n : ℕ, L n ≤ (Nat.digits 10 n).length ∧
(∀ k : ℕ, k < L n → (Nat.digits 10 n)[k]! = (Nat.digits 10 n)[0]!) ∧
(L n ≠ (Nat.digits 10 n).length → (Nat.digits 10 n)[L n]! ≠ (Nat.digits 10 n)[0]!))
: (∃ n : ℕ, (Nat.digits 10 (n^2))[0]! ≠ 0 ∧ L (n^2) = ((3, 1444) : ℕ × ℕ ).1) ∧
(∀ n : ℕ, (Nat.digits 10 (n^2))[0]! ≠ 0 → L (n^2) ≤ ((3, 1444) : ℕ × ℕ ).1) ∧
(∃ m : ℕ, m^2 = ((3, 1444) : ℕ × ℕ ).2) ∧
L (((3, 1444) : ℕ × ℕ ).2) = ((3, 1444) : ℕ × ℕ ).1 ∧
(Nat.digits 10 ((3, 1444) : ℕ × ℕ ).2)[0]! ≠ 0 ∧
∀ n : ℕ, (Nat.digits 10 (n^2))[0]! ≠ 0 ∧ L (n^2) = ((3, 1444) : ℕ × ℕ ).1 → n^2 ≥ ((3, 1444) : ℕ × ℕ ).2 :=
sorry
