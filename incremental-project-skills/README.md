# 新项目

> 本目录收录新项目从立项到上线全流程的 AI Skill，覆盖需求拆解 → 技术方案 → 代码实现 → 测试用例 → 代码审查五个核心阶段。

---

## Skill 全景

| 阶段 | 目录 | Skill 名称 | 核心能力 |
|------|------|-----------|---------|
| 📋 需求 | [`quick-requirement-decomposition`](./quick-requirement-decomposition/SKILL.md) | 产品需求拆解 | 将 PRD 拆解为带 REQ-xxx 编号的原子需求，输出大模型 / 研发 / QA 三视图与追溯矩阵 |
| 📐 设计 | [`quick-tech-solution`](./quick-tech-solution/SKILL.md) | 研发技术方案 | 基于拆解稿输出可实施、可回溯的技术方案；支持子方案拆分、版本管理与附录追溯 |
| 💻 实现 | [`quick-req-driven-codegen`](./quick-req-driven-codegen/SKILL.md) | REQ 驱动代码生成 | 以 PRD + 技术方案 + design token JSON 为真源驱动编码，禁止发明产品逻辑 |
| 🧪 测试 | [`quick-requirement-testcase-trace`](./quick-requirement-testcase-trace/SKILL.md) | 需求追溯测试用例 | 生成功能 / 异常 / 边界三层用例，每条 TC 追溯到 REQ-xxx，维护需求—用例矩阵 |
| 🔍 审查 | [`quick-arch-security-code-review`](./quick-arch-security-code-review/SKILL.md) | 架构与安全代码审查 | 覆盖 SOLID、XSS/CORS/SQLi、鉴权越权、死代码、性能热路径的深度 Code Review |

---

## Skill 协作关系

```
PRD / 产品输入
      │
      ▼
quick-requirement-decomposition   ← 输出 REQ-xxx 拆解稿（真源）
      │
      ▼
quick-tech-solution               ← 消费拆解稿，输出总方案 + 子方案（附录 F）
      │
      ├──────────────────────────────────────────┐
      ▼                                          ▼
quick-req-driven-codegen     quick-requirement-testcase-trace
（按方案 + token 驱动实现）    （按 REQ 生成三层测试用例）
      │
      ▼
quick-arch-security-code-review   ← PR / 合并前，对产出代码做架构与安全审查
```

> **关键约定**：每个 Skill 消费上游产物作为**唯一真源**，禁止跨 Skill 发明业务规则或接口字段。

---

## IRON LAW（跨 Skill 通用）

1. **禁止发明** — 每条实现承诺、接口字段、错误码必须能对应到 REQ-xxx 或标注「工程补充」
2. **禁止覆盖** — PRD 变更或方案升版时，须新建版本文件，旧版保留可查
3. **禁止静默删除** — 未经用户明确确认，不得删除代码或旧文件
4. **追溯优先** — 需求 → 方案 → 代码 → 用例，全链路可回溯

---

## 如何新增 Skill

1. 在本目录下新建子目录，命名以 `quick-` 开头，使用 `kebab-case`，力求见名知意
2. 子目录内包含 `SKILL.md`（主 Skill 文件）及可选的 `references/` 参考资料目录
3. 在本文件的「Skill 全景」表格与「Skill 协作关系」图中补充对应条目
