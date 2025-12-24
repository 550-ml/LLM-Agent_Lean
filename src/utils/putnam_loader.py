"""
PutnamBench 数据加载器
用于加载和处理 PutnamBench 数据集的 .lean 文件
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class PutnamProblem:
    file_path: str
    file_name: str
    total_content: str
    header: str
    problem: str
    docstring: str  # 问题描述，中文


class PutnamLoader:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load_lean_files(self):
        """加载所有 .lean 文件"""
        return [f for f in self.data_path.glob("*.lean")]

    def load_file(self, filename: str) -> PutnamProblem:
        if os.path.isabs(filename) or os.path.dirname(filename):
            file_path = filename

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return self._parse_lean_file(content, file_path)

    def _parse_lean_file(self, content: str, file_path: str) -> PutnamProblem:
        """解析 Lean4 文件（简化版）"""
        # 提取 docstring
        docstring_match = re.search(r"/--(.*?)-/", content, re.DOTALL)
        docstring = docstring_match.group(1).strip() if docstring_match else ""

        # 提取 header：从文件开头到 /-- 之前的所有内容
        if docstring_match:
            # 如果找到 docstring，提取从开头到 /-- 之前的内容
            header = content[: docstring_match.start()].strip()
        else:
            # 如果没找到 docstring，提取从开头到第一个 theorem/def/abbrev 之前的内容
            theorem_match = re.search(r"(?:theorem|def|abbrev)\s+\w+", content)
            if theorem_match:
                header = content[: theorem_match.start()].strip()
            else:
                # 如果都没找到，使用原来的逻辑（只提取 import 和 open）
                imports = "\n".join(re.findall(r"^import\s+.*$", content, re.MULTILINE))
                opens = "\n".join(re.findall(r"^open\s+.*$", content, re.MULTILINE))
                header = f"{imports}\n{opens}".strip()

        # 提取 theorem 语句（优先从 theorem 或 def 开始，如果找不到再考虑 abbrev）
        # 先尝试匹配 theorem 或 def
        theorem_match = re.search(r"(?:theorem|def)\s+\w+", content)
        if not theorem_match:
            # 如果找不到 theorem 或 def，再尝试匹配 abbrev
            theorem_match = re.search(r"abbrev\s+\w+", content)
        if not theorem_match:
            raise ValueError(f"无法找到定理: {file_path}")

        problem = content[theorem_match.start() :].strip()
        pro = PutnamProblem(
            file_path=file_path,
            file_name=Path(file_path).name,
            total_content=content,
            header=header,
            problem=problem,
            docstring=docstring,
        )
        print(pro)
        return pro

    def list_all_problems(self) -> List[str]:
        """
        列出所有问题文件

        Returns:
            List[str]: 文件名列表
        """
        if not os.path.exists(self.src_dir):
            return []

        files = [f for f in os.listdir(self.src_dir) if f.endswith(".lean")]
        return sorted(files)
