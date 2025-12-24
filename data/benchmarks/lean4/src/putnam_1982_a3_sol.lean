import Mathlib

open Set Function Filter Topology Polynomial Real

-- (Real.pi / 2) * log Real.pi
/--
Evaluate $\int_0^{\infty} \frac{\tan^{-1}(\pi x) - \tan^{-1} x}{x} \, dx$.
-/
theorem putnam_1982_a3 :
  Tendsto (fun t ↦ ∫ x in (0)..t, (arctan (Real.pi * x) - arctan x) / x) atTop (𝓝 (((Real.pi / 2) * log Real.pi) : ℝ )) :=
sorry
