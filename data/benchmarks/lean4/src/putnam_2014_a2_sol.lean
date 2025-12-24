import Mathlib

open Topology Filter Nat

-- (fun n : ℕ => (-1) ^ (n - 1) / ((n - 1)! * (n)!))
/--
Let $A$ be the $n \times n$ matrix whose entry in the $i$-th row and $j$-th column is $\frac{1}{\min(i,j)}$ for $1 \leq i,j \leq n$. Compute $\det(A)$.
-/
theorem putnam_2014_a2
(n : ℕ)
(A : Matrix (Fin n) (Fin n) ℝ)
(npos : n > 0)
(hA : ∀ i j : Fin n, A i j = 1 / min (i.1 + 1 : ℚ) (j.1 + 1))
: A.det = ((fun n : ℕ => (-1) ^ (n - 1) / ((n - 1)! * (n)!)) : ℕ → ℝ ) n :=
sorry
