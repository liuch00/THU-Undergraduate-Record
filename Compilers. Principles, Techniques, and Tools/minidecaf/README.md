# MiniDecaf Python 框架

## 依赖

- **Python >= 3.9**
- requirements.txt 里的 python 库，包括 ply 和 argparse。
- RISC-V 运行环境（参见实验指导书）

## 运行

```
python3 main.py --input <testcase.c> [--riscv/--tac/--parse]
```

各参数意义如下：

| 参数 | 含义 |
| --- | --- |
| `input` | 输入的 Minidecaf 代码位置 |
| `riscv` | 输出 RISC-V 汇编 |
| `tac` | 输出三地址码 |
| `parse` | 输出抽象语法树 |

## 代码结构

```
minidecaf/
    frontend/       前端（与中端）
        ast/        语法树定义
        lexer/      词法分析
        parser/     语法分析
        type/       类型定义
        symbol/     符号定义
        scope/      作用域定义
        typecheck/  语义分析（符号表构建、类型检查）
        tacgen/     中间代码 TAC 生成
    backend/        后端
        dataflow/   数据流分析
        reg/        寄存器分配
        riscv/      RISC-V 平台相关
    utils/          底层类
        label/      标签定义
        tac/        TAC 定义和基本类
```
