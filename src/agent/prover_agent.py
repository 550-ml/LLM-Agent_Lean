import logging
import re
import time
from typing import Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ..llm.base import BaseLLM

logger = logging.getLogger(__name__)


class ProverAgent:
    """Prover 智能体：支持本地 Goedel-LM 模型和 API LLM"""

    def __init__(
        self,
        llm: Optional[BaseLLM] = None,
        model_path: Optional[str] = None,
        device_map: Optional[dict] = None,
        max_new_tokens: int = 1024,
    ):
        """
        初始化 ProverAgent

        Args:
            llm: API LLM 实例（如果提供，将使用 API 模式）
            model_path: 本地模型路径（如果提供且 llm 为 None，将使用本地模式）
            device_map: 设备映射（仅用于本地模式）
            max_new_tokens: 最大生成 token 数（仅用于本地模式）
        """
        # 确定使用哪种模式
        if llm is not None:
            self.mode = "api"
            self.llm = llm
            logger.info("ProverAgent initialized in API mode")
        elif model_path is not None:
            self.mode = "local"
            self.model_path = model_path
            self.device_map = device_map or {"": 0}
            self.max_new_tokens = max_new_tokens
            # 初始化时直接加载模型
            self._model = None
            self._tokenizer = None
            self._load_model()
            logger.info("ProverAgent initialized in local mode")
        else:
            raise ValueError("Either 'llm' or 'model_path' must be provided")

    def _load_model(self):
        """加载模型"""
        if self._model is not None:
            return

        logger.info(f"Loading Goedel-LM model from {self.model_path}")
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)

            # 设置 pad_token（如果不存在）
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token

            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map=self.device_map,
                dtype=torch.bfloat16,
                trust_remote_code=True,
            )
            logger.info("Goedel-LM model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Goedel-LM model: {e}")
            raise

    def _normalize_lean_code(self, code: str) -> str:
        """规范化 Lean 代码：移除 import/open 语句，只保留从第一个 theorem 开始到文件末尾的所有内容

        Args:
            code: 原始 Lean 代码

        Returns:
            str: 规范化后的 Lean 代码
        """
        if not code:
            return ""
        lines = code.splitlines()

        # 先查找第一个 theorem 的位置
        theorem_idx = None
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith("theorem "):
                theorem_idx = i
                break

        # 如果找到 theorem，只保留从 theorem 开始到文件末尾的所有内容
        # 这样可以保留一个 subgoal 证明中可能包含的多个 theorem
        if theorem_idx is not None:
            lines = lines[theorem_idx:]

        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("import "):
                continue
            if stripped.startswith("open "):
                continue
            cleaned_lines.append(line)
        result = "\n".join(cleaned_lines).strip()
        if result:
            result = result.rstrip() + "\n"
        return result

    def _extract_lean_code(self, response: str) -> str:
        """统一提取 Lean 代码的辅助方法

        先尝试用正则匹配代码块，如果失败则用 replace 清理
        然后进行 normalize：移除 import/open 和包装文本

        Args:
            response: LLM 的响应文本

        Returns:
            str: 提取并规范化后的 Lean 代码
        """
        if not response:
            return ""

        # 1. 先用正则匹配 ```lean 或 ```lean4 代码块
        pattern = re.compile(r"```(?:lean4?)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
        matches = pattern.findall(response)
        if matches:
            code = matches[0]
        else:
            # 2. 如果正则匹配失败，用 replace 方法清理
            code = response.replace("```lean4", "").replace("```lean", "")
            code = code.replace("```", "")
            code = code.replace("```", "")
            code = code.strip()

        # 3. 规范化代码：移除 import/open 和包装文本
        return self._normalize_lean_code(code)

    def prove_subgoal(self, subgoal: str, header: str = "", error_message: str = "", previous_proof: str = "") -> str:
        """
        证明子目标（支持本地和 API 两种模式）

        Args:
            subgoal: 需要证明的子目标（Lean 4 代码）
            header: 可选的头部代码（imports 等）
            error_message: 错误信息
            previous_proof: 之前的证明
        Returns:
            生成的证明代码
        """
        if self.mode == "api":
            return self._prove_subgoal_api(subgoal, header, error_message, previous_proof)
        else:
            return self._prove_subgoal_local(subgoal, header, error_message, previous_proof)

    def _prove_subgoal_api(
        self, subgoal: str, header: str = "", error_message: str = "", previous_proof: str = ""
    ) -> str:
        """使用 API LLM 证明子目标"""
        # 构建完整的代码
        full_code = subgoal

        # 构建 prompt
        prompt = f"""
Think step-by-step to complete the following Lean 4 proof.

```lean4
{full_code}
```
Lean Hints:
1. When dealing with inequalities, equalities and arithmetic operations like subtraction or division in `ℕ` (natural numbers), beware of truncation. Use `ℝ`, `ℚ` or `ℤ` when possible for arithmetic operations. Avoid using `ℕ` unless required by the theorem statement.
2. Be ESPECIALLY careful about implicit types while defining numeric literals. AVOID patterns like `0 - 1` or `1 / 2` without specifying the types.
3. ALWAYS specify types when dealing with numeric values to avoid ambiguities and unexpected behavior.
4. Use `simp only [specific_lemmas]` rather than bare `simp` to avoid unpredictable simplifications.
5. Use `rw [← lemma]` for reverse direction. When `rw` fails, try `conv => rhs; rw [lemma]` to target specific subterms. nth_rw n [lemma] to rewrite only the nth occurrence.
6. When `ring` fails on ring expressions, try `ring_nf` first to normalize, or cast to a concrete ring like `ℝ` where the tactic works better.
7. Apply `norm_num` for concrete arithmetic calculations and `norm_cast` to simplify type coercions systematically.
8. Use `by_contra h` for proof by contradiction, which introduces the negation of the goal as hypothesis `h`.9. If you get a `no goals to be solved` error, it means that the previous tactics already solved the goal, and you can remove the subsequent tactics.
10. When proving theorems, ALWAYS write the proof in tactic mode, starting the proof with `:= by`.
11. Do NOT use `begin`, `end` blocks in your proof. This is invalid in Lean 4.

Tactic Hints:
`rfl`: Use when there are definitionally equal terms
`exact h`: Use when hypothesis `h` matches the goal exactly  
`assumption`: Searches context for exact match to goal  
`intro x`: Use for `∀` or `→` in goal; names the new hypothesis  
`intros`: Introduces multiple variables/hypotheses at once  
`cases h`: Breaks down inductive hypothesis `h` into constructors  
`obtain ⟨x, y, h⟩ := h'`: Destructures existentials and conjunctions  
`rcases`: Recursive cases for nested inductive structures
`apply h`: Use when `h : P → Q` and goal is `Q`  
`refine h ?_ ?_`: Like apply but with explicit placeholders  
`rw [h]`: Rewrites using equality `h : a = b` left-to-right  
`rw [← h]`: Rewrites right-to-left  
`simp`: Simplifies using simp lemmas; use `simp only [...]` for control  
`simp_all`: Simplifies goal and all hypotheses  
`nth_rw n [h]`: Rewrites only the nth occurrence
`constructor`: Splits conjunctive goals or applies inductive constructors  
`left`/`right`: Choose side of disjunction  
`split`: Splits iff into both directions or conjunctions  
`by_contra h`: Proof by contradiction; adds `¬goal` as `h`  
`push_neg`: Pushes negation inward through quantifiers/connectives
`ring`: Solves polynomial ring equations  
`linarith`: Linear arithmetic solver  
`norm_num`: Evaluates numeric expressions  
`positivity`: Proves positivity/nonnegativity goals  
`field_simp`: Simplifies field expressions (clears denominators)
`have h : P := proof`: Introduces intermediate result  
`suffices h : P by proof`: Reduces goal to proving `P`  
`show P`: Changes goal to definitionally equal `P`  
`calc`: Chain of equations/inequalities with justifications  
`conv => ...`: Enter conv mode for targeted rewriting
`induction x`: Structural induction on `x`  
`induction x using ind_principle`: Custom induction principle  
`induction' x with ...`: More flexible case naming  
`cases x`: Case split without induction hypothesis
`classical`: Enter classical mode locally  
`by_cases h : P`: Case split on decidability of `P`  
`use x`: Provide witness for existential goal  
`choose f hf using h`: Extract choice function from proof
`·`: Focus on next goal  
`focus`: Focus on first goal  
`all_goals`: Apply tactic to all goals  
`any_goals`: Apply tactic to any matching goal  
`swap`: Swap first two goals  
`omega`: Integer linear arithmetic  
`decide`: Decision procedure for decidable propositions  
`tauto`: Propositional tautology checker  
`simp_all only [eq_self_iff_true]`: Common finishing pattern  
`repeat`: Apply tactic repeatedly until failure

Rules:
1. Same proof level = same indentation: All tactics at the same logical level must use identical indentation
2. Consistent characters: Use either tabs OR spaces consistently (don't mix)
3. Proper nesting: Indent sub-proofs one level deeper than their parent
4. Do NOT include any imports or open statements.
5. Use proper Lean 4 syntax and conventions. Ensure the proof sketch is enclosed in triple backticks ```lean```.
6. CRITICAL: You MUST output the COMPLETE theorem statement (starting with `theorem` keyword) followed by the proof. Do NOT output only the proof part (starting from `by`). The output must include the full theorem declaration.
7. Only include a single Lean 4 code block, corresponding to the COMPLETE theorem statement and its proof.
8. When dealing with large numerical quantities, avoid explicit computation as much as possible. Use tactics like `rw` to perform symbolic manipulation rather than numerical computation.
9. Do NOT use sorry.
10. Do NOT change anything in the original theorem statement.

If there is an error, fix it precisely based on:
error_message: {error_message}
previous_proof: {previous_proof}
""".strip()
        messages = [{"role": "user", "content": prompt}]

        try:
            start_time = time.time()
            response = self.llm.generate(messages)
            generated_text = response.content

            logger.debug(f"Prover API generation time: {time.time() - start_time:.2f}s")
            # logger.info(f"Prover API generated text: {generated_text}")

            # 提取并规范化 Lean 代码
            return self._extract_lean_code(generated_text)

        except Exception as e:
            logger.error(f"Error in prove_subgoal (API mode): {e}")
            return ""

    def _prove_subgoal_local(self, subgoal: str, header: str = "", error_message: str = "") -> str:
        """使用本地 Goedel-LM 模型证明子目标"""
        # 构建完整的代码
        full_code = header + "\n" + subgoal if header else subgoal

        # 构建 prompt
        prompt = f"""
You are a Lean 4 prover.
Complete the following Lean 4 code so that it compiles.

```lean
{full_code}
```
""".strip()

        chat = [{"role": "user", "content": prompt}]

        try:
            # 编码输入
            encoded = self._tokenizer.apply_chat_template(
                chat,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt",
            )

            # 获取输入长度（用于后续移除 prompt）
            input_length = encoded.shape[1]

            # 生成证明
            start_time = time.time()
            outputs = self._model.generate(
                encoded.to(self._model.device),
                max_new_tokens=self.max_new_tokens,
                pad_token_id=self._tokenizer.pad_token_id,
            )

            # 只解码新生成的部分（移除输入 prompt）
            generated_ids = outputs[0][input_length:]
            generated_text = self._tokenizer.decode(generated_ids, skip_special_tokens=True)

            logger.debug(f"Prover local generation time: {time.time() - start_time:.2f}s")
            logger.info(f"Prover local generated text (without prompt): {generated_text}")

            # 提取并规范化 Lean 代码
            return self._extract_lean_code(generated_text)

        except Exception as e:
            logger.error(f"Error in prove_subgoal (local mode): {e}")
            return ""


TEXT = """
Rules:
1. Output ONLY a single Lean code block (```lean ... ```).
2. Do NOT include any explanation, proof plan, or comments.
3. Do NOT include imports or open statements unless they already appear in the given code.
4. Do NOT use `sorry`.
5. Do NOT change the theorem/lemma statement (name, arguments, types, statement). Only fill in the proof.
6. Keep the result self-contained and compilable."""
