import Mathlib

-- 6 * Real.pi ^ 2
/--
Find the volume of the region of points $(x,y,z)$ such that
\[
(x^2 + y^2 + z^2 + 8)^2 \leq 36(x^2 + y^2).
\]
-/
theorem putnam_2006_a1
: ((MeasureTheory.volume {(x, y, z) : ℝ × ℝ × ℝ | (x ^ 2 + y ^ 2 + z ^ 2 + 8) ^ 2 ≤ 36 * (x ^ 2 + y ^ 2)}).toReal = ((6 * Real.pi ^ 2) : ℝ )) :=
sorry
