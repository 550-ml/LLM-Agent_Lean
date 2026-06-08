# LLM-Agent Lean

一个面向 Lean 4 形式化证明的多智能体自动求证项目。项目参考
**HILBERT: Recursively Building Formal Proofs with Informal Reasoning** 的思路，
尝试把通用大模型的数学推理能力、Lean 专用证明模型、语义定理检索与
Lean4 编译验证组合成一个递归证明系统。

核心目标很直接：给定 PutnamBench 风格的 Lean 题目模板，让 Agent 先理解数学问题，
再生成 proof sketch，拆出子目标，调用 Prover 补全 Lean 证明，最后交给 Lean4
严格验证并根据错误反馈继续修复。

## 项目亮点

- **五组件 Agent 架构**：Coordinator 统一调度 Reasoner、Retriever、Prover、Verifier。
- **非形式推理到形式证明**：先生成自然语言证明和 Lean proof sketch，再逐步填补 `sorry`。
- **Lean4 编译闭环**：通过 `lake lean` 对生成代码做真实验证，并解析错误位置、错误类型和未完成目标。
- **语义定理检索**：使用 FAISS 与 sentence-transformers 从 mathlib 相关语料中召回候选定理。
- **PutnamBench 数据适配**：仓库内包含 Lean4 benchmark、测试样例和数据加载逻辑。
- **双 Prover 模式**：支持 API LLM，也预留本地 Goedel-LM / Goedel-Prover 路径。

## 系统架构

```text
Lean 题目模板
     │
     ▼
HilbertCoordinator
     │
     ├── RetrieverAgent      # 生成检索查询，召回相关 theorem / lemma
     ├── ReasonerAgent       # 数学理解、非形式证明、proof sketch、错误修复
     ├── ProverAgent         # 证明单个子目标，支持 API / 本地模型
     └── VerificationAgent   # 调用 Lean4Runner 做编译验证
             │
             ▼
        Lean4 / Lake
```

## 目录结构

```text
.
├── main.py                         # 主入口：加载配置、数据、Agent 并运行证明流程
├── run.sh                          # 示例启动脚本
├── requirements.txt                # Python 依赖
├── config
│   └── default.yaml                # 数据、LLM、Retriever、Verifier、Logger 配置
├── src
│   ├── agent                       # Reasoner / Prover / Retriever / Verifier / Coordinator
│   ├── llm                         # OpenAI / vLLM 客户端与模型工厂
│   ├── verifier                    # Lean4Runner，负责调用 lake lean
│   ├── utils                       # 配置、prompt、Putnam 数据加载与向量库构建工具
│   └── logger                      # 日志与可视化工具
├── data
│   ├── prompts                     # 中文与 user prompt 模板
│   └── benchmarks/lean4            # PutnamBench Lean4 项目与样例
├── docs
│   ├── HILBERT_REPRODUCTION_GUIDE.md
│   └── 开发文档.md
└── test_*.py                       # 模块测试与验证脚本
```

## 环境准备

### 1. 克隆项目

```bash
git clone https://github.com/550-ml/LLM-Agent_Lean.git
cd LLM-Agent_Lean
```

### 2. 安装 Python 依赖

建议使用 Python 3.10+：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` 中包含 `faiss-gpu`，如果本机没有 CUDA/GPU 环境，可以按自己的平台改用
`faiss-cpu`。

### 3. 准备 Lean 4

项目通过 `lake lean` 验证 Lean 代码，因此需要先安装 Lean 4 / Lake，并确保命令可用：

```bash
lake --version
```

Lean benchmark 位于：

```text
data/benchmarks/lean4
```

第一次使用时，可以进入该目录让 Lake 拉取依赖：

```bash
cd data/benchmarks/lean4
lake update
cd ../../..
```

### 4. 配置 API Key

主程序会读取：

```text
config/api_key.env
```

可以创建该文件并写入自己的模型服务密钥，例如：

```bash
OPENAI_API_KEY=your_api_key_here
```

模型名称、base URL、超时时间等配置在 `config/default.yaml` 中维护。

## 快速运行

使用默认配置处理 `data/benchmarks/lean4/test` 下的 Lean 文件：

```bash
python main.py --dir data/benchmarks/lean4/test --config config/default.yaml
```

也可以直接运行脚本：

```bash
bash run.sh
```

当前 `main.py` 会加载测试目录中的 Lean 文件，初始化 Reasoner、Retriever、Verifier、
Prover 和 Coordinator，然后对第一个样例执行一次证明生成流程。

## 核心流程

1. **加载题目**：`PutnamLoader` 读取 Lean 文件中的 header、problem、docstring。
2. **召回定理**：`RetrieverAgent` 根据 Reasoner 生成的 query 检索候选 theorem。
3. **生成思路**：`ReasonerAgent` 生成非形式证明和 Lean proof sketch。
4. **验证草稿**：`VerificationAgent` 调用 Lean4Runner 检查 sketch 语法和上下文。
5. **拆分子目标**：Coordinator 从 sketch 中提取 `have ... := by sorry` 子问题。
6. **证明子目标**：`ProverAgent` 用 API 或本地模型补全具体 Lean 证明。
7. **组装验证**：Coordinator 回填子证明，最终再次调用 Lean4 验证完整证明。

## 配置说明

常用配置集中在 `config/default.yaml`：

- `data.project_dir`：Lean4 benchmark 项目路径。
- `data.data_dir`：待处理 Lean 文件目录。
- `llm.reasoner`：Reasoner 使用的模型、温度、token 上限、base URL。
- `agent.retriever`：FAISS index 目录与 sentence-transformers 模型名。
- `verifier.project_path`：Lean4Runner 执行 `lake lean` 的项目路径。
- `prover.model`：`api` 或 `local`，决定 Prover 使用 API LLM 还是本地证明模型。
- `logger.save_dir`：运行日志输出目录。

注意：默认配置里有本机绝对路径，换机器运行时需要先改成自己的仓库路径。

## 文档

- [HILBERT 论文复现指导](docs/HILBERT_REPRODUCTION_GUIDE.md)
- [开发文档](docs/开发文档.md)
- [LLM 模块说明](src/llm/README.md)
- [Lean4 benchmark 说明](data/benchmarks/lean4/README.md)

## 当前状态

项目已经具备端到端框架：数据加载、LLM 调用、定理检索、proof sketch 生成、
Lean4 验证、子目标拆分和多轮修复逻辑都已有实现。后续仍适合继续完善：

- 更稳定的 theorem retriever 构建与加载流程。
- 更细粒度的错误分类和自动修复策略。
- 更系统的端到端 benchmark 评测。
- CMake/Makefile 类似的环境初始化脚本，降低 Lean 与向量库配置成本。
- 对本地 Prover 模型推理、批处理和日志可视化做进一步工程化。

## 致谢

本项目参考 HILBERT 论文提出的递归形式化证明思路，并使用 PutnamBench /
mathlib 相关 Lean4 数据作为实验基础。

