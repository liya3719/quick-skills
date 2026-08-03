---
name: quick-arch-security-code-review
description: "面向架构、安全、漏洞扫描、业务逻辑校验与性能的深度代码审查，默认中文输出。覆盖 SOLID 与分层边界、污点追踪式漏洞扫描（OWASP/CWE、SSRF/XXE/命令注入/依赖 CVE）、XSS 与 CORS 与 SQL 注入、身份认证与鉴权与越权、状态机与幂等与补偿逻辑校验、敏感信息与私钥进日志、不安全反序列化、竞态与 TOCTOU、错误处理与边界与空值、算法与 I/O 与热路径性能。死代码以统一可检索标注列出，须经研发明确确认后由本人或研发删除，审查方不擅自删线。触发：代码审查、code review、CR、PR 审查、合并前检查、走查、安全审计、漏洞扫描、逻辑校验、业务逻辑审查、渗透前自查、质量分析、查死代码、性能问题、架构合理性。Actions: review, audit, inspect, scan, 扫描, 检查, 审计, 走读, 评审, 逻辑校验."
argument-hint: "[--focus all|arch|security|vuln|logic|quality|perf|dead-code] [--in-repo-annotate yes|no] 无参则全维度；vuln=漏洞扫描 logic=逻辑校验；annotate 表示是否在代码中加 DEAD 注释，须用户明确同意"
---

# 架构与安全代码审查

IRON LAW：**未**得用户或研发**明确确认**前，**不得**从仓库**删除**任何代码，**不得**将「死代码」物理移除；**不得**擅自向生产分支**推送**安全修复。**漏洞**与**逻辑**结论须**有代码路径或复现条件**支撑；缺业务上下文时标「需确认」，**不得**把推测标成 P0。

Red Flags（出现则回到「确认范围与权限」再往下）：

- 准备用「应删未用」**直接**删 import/函数/文件
- 在无流量与业务上下文时，声称某分支「**绝对**不可达」
- 把**猜测**写成**已证实**的安全漏洞或**逻辑缺陷**
- 漏洞扫描**不**做污点追踪，只复读 OWASP 名词
- 逻辑校验**不**对齐预期行为，只报空指针/边界
- 用户**未**要求时**修改**远程/共享分支

---

## Workflow

```
架构与安全代码审查 进度:

- [ ] Step 0: 确认范围与模式 ⛔ BLOCKING
- [ ] Step 1: 通读范围与数据流
- [ ] Step 2: 架构与 SOLID → references/solid-architecture.md
- [ ] Step 3: 安全风险 → references/security-risks.md
- [ ] Step 4: 漏洞扫描（污点追踪）→ references/vulnerability-scan.md
- [ ] Step 5: 逻辑校验（业务语义）→ references/logic-verification.md
- [ ] Step 6: 代码质量（错误/边界）→ references/code-quality.md
- [ ] Step 7: 性能 → references/performance.md
- [ ] Step 8: 死代码（疑似）与染色 → references/dead-code-marking.md
- [ ] Step 9: 按模板汇总 ⚠️ REQUIRED → references/review-output-template.md
- [ ] Step 10: 用户确认后行动（改代码/不改编译）⚠️ REQUIRED
```

**`$ARGUMENTS` / focus**：`--focus arch|security|vuln|logic|quality|perf|dead-code` 时，**可跳过**非选中维度的长清单，但摘要中须注明「本次未覆盖：…」。`security` 含 Step 3；`vuln` 仅 Step 4；`logic` 仅 Step 5。`all` 或缺省为全维度。

---

## Step 0: 确认范围与模式 ⛔ BLOCKING

在读取代码前，向用户**确认**或从上下文**推断**并**复述**：

- **范围**：单文件、目录、diff、整 PR、或分支对比？
- **技术栈**（影响 XSS/SQL/反序列化/并发模型等检查项的权重）
- **是否在库中打「死代码」注释**（`--in-repo-annotate`）：**默认否**；**仅**在用户明确说「可改仓库加标注」时启用
- 若有「仅出意见/可改代码」偏好，**遵守**

---

## Step 1: 通读范围与数据流

问：**外部**输入从何处进入？**敏感**写操作、**钱/库存/权限**变更在何路径？  
用 3～6 句话概括数据流，再进各专项；避免一上来抠命名。

---

## Step 2: 架构与 SOLID

加载 `references/solid-architecture.md`，按**提问清单**在报告「架构」类下列出发现。  
**禁止**只写「违反 SRP」而无**可改**的拆分建议或**至少一个**具体问题（例如多职责证据）。

---

## Step 3: 安全风险

加载 `references/security-risks.md`。  
对 XSS/CORS/SQLi、鉴权与越权、日志与私钥、反序列化、竞态：**每类**至少**自问**表格中的**对应句**；有代码证据再写进报告，无证据进「需确认」。

---

## Step 4: 漏洞扫描

加载 `references/vulnerability-scan.md`。

- 按 Step 1 数据流**枚举入口**，对每条外部输入做**入口→sink**追踪。
- 对照模式库（SQL/命令/路径/SSRF/XXE/反序列化/加密/JWT 等）；命中则写报告，注明 **CWE/OWASP**（有映射时）与**可利用前提**。
- scope 含依赖清单时检查**已知高危 CVE** 与**密钥进库**；无 lockfile 则建议 SCA，不假装已扫全依赖。
- **禁止**无 sink 路径时标 P0；与 Step 3 重复项**合并**为一条，取更高严重度。

---

## Step 5: 逻辑校验

加载 `references/logic-verification.md`。

- 先写清本 scope **预期业务行为**（来自 PRD/注释/测试；否则标「假设」）。
- 覆盖：分支完备性、状态不变量、权限归属、幂等、时序与金额、补偿回滚、测试与注释一致性。
- 每条逻辑问题：**预期** vs **实际** + **复现条件** + 位置；无业务依据 →「待确认规则」，不标 P0。

---

## Step 6: 代码质量

加载 `references/code-quality.md`，覆盖**错误处理**与**边界**两类；区分「**风格**」与「**会崩/会错**」问题。

---

## Step 7: 性能

加载 `references/performance.md`。先标出**热路径/大数据量**再谈优化；**无**基准或复杂度对比时，严重度**上限 P2** 并标「需 profiling」。

---

## Step 8: 死代码（疑似）与「染色」

加载 `references/dead-code-marking.md`。

- 在报告中**单独**一节列「**疑似**死代码」，每条：**位置、依据、置信度（低/中/高）**。
- **仅**在用户允许 `--in-repo-annotate` 时，在**本地/分支**用文档中的**统一注释**标注；**不得**在未经确认时**删除**。
- 高置信度时仍写「须研发确认后删除」。

---

## Step 9: 汇总

加载 `references/review-output-template.md`，按**严重度**排序，**P0 漏洞/越权/注入**与**P0 逻辑（重复扣款、库存可负等）**最前。每条含：位置、类别、问题、**一条**可执行建议。

---

## Step 10: 用户确认后行动 ⚠️ REQUIRED

- **只读报告**：不修改文件。
- **需改代码**（如加 DEAD 注释、修漏洞）：**复述**将改哪些文件，**等待**用户明确「可以改」或「发 PR 草稿」再动手。
- **删代码**：**仅**在用户**逐条**或整段确认「可删」后执行，且**优先**由用户自行在版本库中删除。

---

## Anti-Patterns

- 以「未使用」为由**直接** `git rm` 或大片删除。
- 把 `eslint` 能报的**当**成深度架构结论。
- 不区分 **Back-end / 前端** 的安全模型，混用 CORS 与「接口鉴权」的叙述。
- 在报告中堆砌术语而无**file:line** 或**符号**位置。
- **自动**为「修复安全」在共享分支**强推**或覆盖他人提交。
- 漏洞扫描只列 checklist **不**写入口→sink 链路。
- 逻辑校验把**空值/类型**问题当**业务逻辑错误**重复报告。

---

## Pre-Delivery Checklist

- [ ] 已说明 scope 与本次 `--focus` 未覆盖的维度
- [ ] 每条**实质**问题含**位置**（`path:line` 或符号）
- [ ] 安全/漏洞项区分「**已**从代码**证实**」与「**需**业务/运行确认」；漏洞含**入口→sink**（若有）
- [ ] 逻辑项含**预期 vs 实际**与**复现条件**（或标「待确认规则」）
- [ ] 无「建议重构」**单独**成条而无具体问题
- [ ] 死代码**未**在未经授权时删除；若打了注释，**未**用非统一标签
- [ ] 无占位 `TODO`/`FIXME` 在交付报告主体中冒充结论
- [ ] IRON LAW：无擅自删线与未授权的自动修复
- [ ] **观测可扫描**：未关闭 P0/高危项在报告中可检索（含 P0 + 未关闭/open），供 `quick-pipeline-observability` 统计
