import logging

from ..verifier import lean4_runner

logger = logging.getLogger(__name__)


class VerificationAgent:
    """
    验证智能体
    """

    def __init__(self, lean_runner: lean4_runner):
        self.lean_runner = lean_runner

    def execute(
        self,
        full_proof: str,
    ):
        """执行 Lean4 验证"""
        full_proof = self._check_head(full_proof)
        result = self.lean_runner.execute(full_proof)
        success = getattr(result, "success", False)
        output = getattr(result, "output", "")
        return success, output

    def _check_head(self, proof):
        """检查proof是否有head"""
        if proof.startswith("import "):
            return proof
        else:
            proof = "import Mathlib\n" + proof
            return proof
