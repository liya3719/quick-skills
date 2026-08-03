# 执行计划（写代码前）

## 何时加载

步骤 4 落盘**执行计划**时**必读**；**未获完整 block 落点前禁止写业务代码**。

## 输入

- `docs/prd/` 需求拆解（REQ-xxx；含研发确认记录）
- `docs/design/` 技术方案（设计分块 / 模块 / 接口；含研发确认记录）
- `design/` 设计数据（Figma / MasterGo / token JSON；含 manifest 确认）
- 项目规则（`AGENTS.md` / `AGENT.md` / `CLAUDE.md`）

## Block 最低字段 ⛔

方案中每个**设计分块**（或子方案模块）须对应一行 block；**任缺一项 → 该 block 状态 `blocked`，不得编码**：

| 字段 | 说明 |
|------|------|
| **block id** | 与方案章节/分块 id 一致 |
| **追溯 REQ** | REQ-xxx |
| **目标文件** | 将创建/修改的路径 |
| **目标组件** | 组件/模块/符号名 |
| **数据字段** | props/state/API 字段与类型来源（方案锚点） |
| **交互** | 事件、跳转、校验、态切换；**须** `docs/prd/` REQ + JSON 节点 id 锚点 |
| **证据** | 方案 § / JSON 节点 id / `design/*.png` 文件名 / token 名 |

## 落盘路径

默认：`docs/ai/codegen/{需求名}-执行计划-v{x.y}.md`（团队另有约定则在步骤 1 注明）。

## 模板

```markdown
# 执行计划 — {需求名} v{x.y}

## 元数据
- 拆解：`docs/prd/{需求名}-v{x.y}.md`（研发确认：…）
- 总方案：`docs/design/{需求名}-tech-solution-v{x.y}.md`（研发确认：…）
- 设计数据：`design/{需求名}/…`（研发确认：…）
- 项目规则：AGENTS.md | CLAUDE.md

## Block 表
| block id | REQ | 目标文件 | 目标组件 | 结构 JSON | 视觉 PNG | 数据字段 | 交互 | 证据 | 状态 |
|----------|-----|----------|----------|-----------|----------|----------|------|------|------|
| B-01 | REQ-001 | src/... | FooCard | design/home.json#node/12 | design/home.png | name, status | click→详情 REQ-003 | 方案§4.2; node/12 | ready |
| B-02 | REQ-002 | … | … | … | … | … | … | … | blocked（缺 PNG） |

## 实现层顺序（全 block 共享）
types → api → state → leaf → page → route → tracking

## blocked 汇总
- B-02：…
```

## 确认门

- 存在 `blocked` block 且用户未确认「仅实现 ready 子集」→ **停止**，不进入步骤 6 编码
- 用户确认缩小范围时，须在计划与后续对齐报告中列出**刻意跳过的 REQ/block**

## 禁止

- 无 block 表直接改文件
- 证据列填「待定」「TBD」却标 `ready`
- 一个 block 对应多个无关联 REQ 却不拆分
