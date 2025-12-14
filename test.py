import re

generated_text = """
Generated text: user
You are a Lean 4 prover.
Complete the following Lean 4 code so that it compiles.

Rules:
1. Output ONLY a single Lean code block (```lean ... ```).
2. Do NOT include any explanation, proof plan, or comments.
3. Do NOT include imports or open statements unless they already appear in the given code.
4. Do NOT use `sorry`.
5. Do NOT change the theorem/lemma statement (name, arguments, types, statement). Only fill in the proof.
6. Keep the result self-contained and compilable.

```lean
import Mathlib
open Set Filter Topology
theorem hx_pos
  (a : ℤ) (ha : a ≥ 2)
  (b : ℤ) (hb : b ≥ 2)
  (x : ℤ) (hx : x = a - 1)
  (y : ℤ) (hy : y = b - 1)
  (z : ℤ) (hz : z = 1) :
  x > 0 := by
  sorry
assistant
```
### Lean 4 Proof

```lean
theorem hx_pos
  (a : ℤ) (ha : a ≥ 2)
  (b : ℤ) (hb : b ≥ 2)
  (x : ℤ) (hx : x = a - 1)
  (y : ℤ) (hy : y = b - 1)
  (z : ℤ) (hz : z = 1) :
  x > 0 := by
  have h₁ : x = a - 1 := hx
  have h₂ : a ≥ 2 := ha
  have h₃ : x > 0 := by
    rw [h₁]
    -- Since a ≥ 2, a - 1 ≥ 1, which is greater than 0.
    have h₄ : (a : ℤ) - 1 ≥ 1 := by
      linarith
    linarith
  exact h₃
```
"""
pattern = re.compile(r"```(?:lean4?)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
matches = pattern.findall(generated_text)
if matches:
    print(matches[-1])

subgoals = ["1", "2", "3", "4", "5"]
proved_subgoals = {}
proved_subgoals["1"] = "1"
proved_subgoals["2"] = "2"
remaining = [s for s in subgoals if s not in proved_subgoals]
print(remaining)
