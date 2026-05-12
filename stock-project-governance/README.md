# 存量代码治理 Skills

> 本目录聚焦存量代码治理，当前提供 2 个可直接使用的 skill：**独立 / 链路模块重构** 与 **存量模块新增功能**。

## Skills 列表

| Skill | 适用场景 | 核心约束 | 产出物 |
|---|---|---|---|
| `refactor-module` | 独立模块重构、链路模块重构、legacy 模块治理 | 行为等价、禁止原地重写、v1/vn 并存、三件套确认前禁止写代码 | 现状与风险、调用关系图、技术方案、重构计划、测试用例、重构报告 |
| `refactor-feature-addition` | 在存量模块基础上增加新功能 | 最小改动、禁止顺手改无关代码、先分析影响范围、确认前禁止写代码 | 技术方案、测试用例、必要时补充影响范围说明 |

## 目录结构

```text
stock-project-governance/
├── README.md
├── 模块重构规则.md
├── refactor-module/
│   ├── SKILL.md
│   └── references/
│       ├── 现状与风险模板.md
│       ├── 调用关系图模板.md
│       ├── 技术方案模板.md
│       ├── 重构计划模板.md
│       ├── 测试用例模板.md
│       └── 重构报告模板.md
└── refactor-feature-addition/
    ├── SKILL.md
    └── references/
        ├── 技术方案模板.md
        ├── 测试用例模板.md
        └── 影响范围模板.md
```

## Skill 1：`refactor-module`

### 适用场景
- 独立模块重构
- 链路模块重构
- legacy 模块治理
- 需要快速回滚的 vn 重构

### 核心流程
1. 先调用 `understand-anything` / `/understand` 完成代码理解
2. 确认模块名、版本号 `vn`、重构类型
3. 先产出重构前三件套与 references：
   - `refactor/{模块名}/{vn}/references/现状与风险.md`
   - `refactor/{模块名}/{vn}/references/调用关系图.md`
   - `refactor/{模块名}/{vn}/技术方案.md`
   - `refactor/{模块名}/{vn}/重构计划.md`
   - `refactor/{模块名}/{vn}/测试用例.md`
4. 等待用户确认后再开始写代码
5. 实施 `v1/vn` 并存重构，保留快速回滚能力
6. 全量测试通过后输出 `refactor/{模块名}/{vn}/重构报告.md`

### 核心约束
- 不改变对外可观测行为、错误语义、时序与并发承诺
- 禁止在原业务路径上原地重写
- 禁止顺手优化无关代码
- 新增或实质修改的 API、类、函数必须补充**中文注释**
- 文档与终版实现必须一致，若漂移先修文档并记录原因

### references 模板
- `refactor-module/references/现状与风险模板.md`
- `refactor-module/references/调用关系图模板.md`
- `refactor-module/references/技术方案模板.md`
- `refactor-module/references/重构计划模板.md`
- `refactor-module/references/测试用例模板.md`
- `refactor-module/references/重构报告模板.md`

## Skill 2：`refactor-feature-addition`

### 适用场景
- 在老模块上新增功能
- 在现有模块中扩展能力
- legacy 模块新增需求

### 核心流程
1. 先调用 `understand-anything` / `/understand`
2. 用一段话复述原模块职责、不变量、对外契约
3. 先做上下游调用链与影响范围分析
4. 先产出双文档：
   - `feature/{模块名}/技术方案.md`
   - `feature/{模块名}/测试用例.md`
5. 等待用户确认后再写代码
6. 以最小改动实现新增功能，并补中文注释与单元测试
7. 完成回归并校对代码、技术方案、测试用例三方一致

### 核心约束
- 新增功能必须遵循最小改动原则
- 禁止顺手修改与需求无关的文件
- 优先通过扩展点实现，避免无必要侵入既有逻辑
- 新增或修改的 API、类、函数必须补充**中文注释**
- 单元测试必须全量通过

### references 模板
- `refactor-feature-addition/references/技术方案模板.md`
- `refactor-feature-addition/references/测试用例模板.md`
- `refactor-feature-addition/references/影响范围模板.md`

## 通用治理原则

两个 skill 共用以下治理原则：
- 任何场景下，先理解原模块职责、契约、影响范围，再动手
- 先文档、后代码
- 禁止顺手优化与本次任务无关的代码
- 遵循 SOLID，保持高内聚、低耦合
- 测试通过后再归档、再推进后续流程

## 如何使用

如果要在 Claude Code 中使用，可将本目录下 skill 安装到 `~/.claude/skills/`，或直接复制对应 skill 目录使用。

典型触发语句示例：
- `重构 settlement 模块，保持行为等价，输出方案和计划后再写代码`
- `把订单履约链路做 vn 重构，要求支持快速回滚`
- `给现有库存模块加预占库存功能，要求最小改动，不要顺手重构`
- `在 legacy 支付模块里新增超时取消能力，先分析上下游影响`
