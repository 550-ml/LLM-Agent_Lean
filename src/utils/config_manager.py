"""
配置管理器：统一管理所有配置
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict

import yaml

from src.logger import setup_logging


class ConfigManager:
    """配置管理器：统一加载和管理所有配置"""

    def __init__(self, config_file: str = "config/default.yaml"):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

        with open(self.config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        return config or {}

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置值（支持点号路径，如 "llm.planning.model"）

        Args:
            key_path: 配置键路径（如 "llm.planning.model"）
            default: 默认值

        Returns:
            配置值
        """
        keys = key_path.split(".")
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_data_config(self) -> Dict[str, Any]:
        """获取数据配置"""
        return self.config.get("data", {})

    def get_prompt_loader_config(self) -> Dict[str, Any]:
        """获取 prompt 加载器配置"""
        return self.config.get("prompt_loader", {})

    def get_retriever_config(self) -> Dict[str, Any]:
        """获取 retriever 配置"""
        return self.config.get("retriever", {})

    def get_llm_config(self, agent_type: str = "planning") -> Dict[str, Any]:
        """
        获取 LLM 配置

        Args:
            agent_type: 智能体类型（"planning" 或 "generation"）

        Returns:
            LLM 配置字典
        """
        return self.config.get("llm", {}).get(agent_type, {})

    def get_agent_config(self) -> Dict[str, Any]:
        """获取 Agent 配置"""
        return self.config.get("agent", {})

    def get_verifier_config(self) -> Dict[str, Any]:
        """获取验证器配置"""
        return self.config.get("verifier", {})

    def get_prover_config(self) -> Dict[str, Any]:
        """获取 Prover 配置"""
        return self.config.get("prover", {})

    def get_project_dir(self) -> str:
        """获取基准数据目录"""
        return self.get_data_config().get("project_dir", "data/benchmarks/lean4")

    def get_data_dir(self) -> str:
        """获取数据目录"""
        return self.get_data_config().get("data_dir", "data/benchmarks/lean4/test")

    def get_max_retries(self) -> int:
        """获取最大重试次数"""
        return self.get_agent_config().get("max_retries", 5)

    def init_logger(self, problem_name: str = None):
        """
        初始化日志系统

        Args:
            problem_name: 题目名称（如 "putnam_2001_a1"），如果提供则按题目创建文件夹，
                         否则按时间创建文件夹

        Returns:
            logging.Logger: 日志记录器
        """
        log_dir = self.get("logger.save_dir")
        log_config = self.get("logger.log_config")

        if problem_name:
            # 根据题目名称创建文件夹（清理文件名中的特殊字符）
            safe_name = problem_name.replace("/", "_").replace("\\", "_").replace(".lean", "")
            save_dir = f"{log_dir}/{safe_name}"
        else:
            # 如果没有提供题目名称，使用时间戳
            save_dir = datetime.now().strftime(f"{log_dir}/%Y%m%d_%H%M%S")

        os.makedirs(save_dir, exist_ok=True)

        # 查找下一个可用的日志文件名（info.log, info2.log, info3.log, ...）
        log_filename = self._get_next_log_filename(save_dir)

        # 清除现有的 handlers，避免重复添加
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            # 关闭文件 handler 以释放文件句柄
            if hasattr(handler, "close"):
                handler.close()
            root_logger.removeHandler(handler)

        # 使用新的日志文件名设置 logger
        setup_logging(sva_dir=save_dir, log_config=log_config, log_filename=log_filename)

        logger = logging.getLogger(__name__)
        return logger

    def _get_next_log_filename(self, save_dir: str) -> str:
        """
        获取下一个可用的日志文件名

        Args:
            save_dir: 日志保存目录

        Returns:
            str: 日志文件名（如 "info.log", "info2.log", "info3.log"）
        """
        import glob

        # 查找所有 info*.log 文件
        pattern = os.path.join(save_dir, "info*.log")
        existing_files = glob.glob(pattern)

        if not existing_files:
            # 如果没有现有文件，使用 info.log
            return "info.log"

        # 提取所有编号
        numbers = []
        for file in existing_files:
            basename = os.path.basename(file)
            if basename == "info.log":
                numbers.append(0)  # info.log 对应编号 0
            else:
                # 提取 info 后面的数字（如 info2.log -> 2）
                import re

                match = re.match(r"info(\d+)\.log", basename)
                if match:
                    numbers.append(int(match.group(1)))

        # 找到最大编号，下一个编号就是 max_number + 1
        if numbers:
            max_number = max(numbers)
            next_number = max_number + 1
        else:
            next_number = 1

        # 生成新的文件名
        if next_number == 0:
            return "info.log"
        else:
            return f"info{next_number}.log"
