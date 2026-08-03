---
name: quick-compile-verify
description: "代码编译验证与可运行性审计：消费 quick-req-driven-codegen 产出，在架构对齐报告关键项 pass 后执行 lint、TypeScript 编译、Web 构建；多平台场景追加 iOS/Android/Harmony bundle 产物验证。失败时须定位根因并修复（import 路径、类型不匹配、字段变更、依赖误用、lint 规则等），修复后重跑直至通过或达回流上限；仅环境缺失或需人工决策时汇总 OPEN 交研发确认。Actions: 编译验证, build verify, lint, typecheck, tsc, 构建, 打包验证, bundle 验证, 修编译错误, 修 lint, 修类型错误. Objects: 架构对齐报告, 执行计划, package.json, AGENTS.md, ZRN, RN, Harmony. Stacks: Vue3, React, ZRN, TS, Vite, Webpack, Rspack. Triggers: 编译验证, 跑 lint, 类型检查, build 不过, 构建失败, 修编译, 验证可运行, bundle 验证, iOS Android Harmony 打包."
argument-hint: "[--scope web|native|all] [--fix-rounds N] 默认 web+lint+tsc+build；native 含 iOS/Android/Harmony bundle；fix-rounds 默认 3"
---

# 代码编译验证

**语言**：报告、修复说明、OPEN 项默认**中文**；保留错误码、包名、路径、符号名为原样英文。

IRON LAW：**禁止只贴编译/log 报错而不定位根因与修复动作。** **可自动修复的错误（路径、类型、字段、依赖引用、lint 可机械满足项）须在本 skill 内修完并重跑，不得甩给研发。** **仅当错误明确来自环境缺失、凭证/私服、平台 SDK 未安装、或业务/契约需人工拍板时，才汇总 OPEN 列表暂停。** **未通过架构对齐报告门禁（关键项 pass）时，禁止宣称编译验证完成。**

Red Flags（出现则回到步骤 0）：

- 对齐报告缺失或关键项非 pass 却跑 build
- 把 stderr 全文粘贴当交付，无「根因 → 改动 → 重跑结果」
- 未读 `AGENTS.md` / `package.json` 就臆造 npm script
- 环境类失败未区分「本机缺 SDK」与「代码错误」
- 修复时改动范围远超报错文件且无说明
- 达 fix-rounds 上限仍 pass 宣称可合入

## Workflow

```
编译验证进度：

- [ ] 步骤 0：前置门禁 ⛔ BLOCKING
  - [ ] 0.1 《架构对齐报告》已落盘且关键项 pass（或用户明确跳过并承担风险）
  - [ ] 0.1a UI 相关迭代：《视觉偏差清单》pass 或 UI-N/A（来自 `quick-visual-audit`）
  - [ ] 0.2 确认验证范围：web / native / all（`$ARGUMENTS` 或上下文）
  - [ ] 0.3 确认 fix-rounds 上限（默认 3）
- [ ] 步骤 1：发现构建命令 ⛔ BLOCKING
  - [ ] 加载 `references/build-command-discovery.md`
  - [ ] 从 AGENTS.md、package.json、根 README、CI 配置解析 lint / typecheck / build / bundle 命令
  - [ ] 落盘或口头复述《验证命令表》后再执行
- [ ] 步骤 2：Web 管线 ⛔ BLOCKING（scope=web|all）
  - [ ] 加载 `references/verify-pipeline-order.md`
  - [ ] 顺序：lint → typecheck(tsc/vue-tsc) → web build
  - [ ] 每步失败 → 步骤 4 修复循环
- [ ] 步骤 3：多平台 bundle（scope=native|all）⚠️ REQUIRED
  - [ ] 加载 `references/multi-platform-bundle.md`
  - [ ] 按方案/对齐报告平台清单：iOS / Android / Harmony（HarmonyOS）
  - [ ] 验证 bundle 或等价打包产物生成且无编译级错误
- [ ] 步骤 4：错误分流与修复循环 ⛔ BLOCKING
  - [ ] 加载 `references/error-triage-and-fix.md`
  - [ ] 分类：auto-fix / env-blocked / decision-blocked
  - [ ] auto-fix：改代码 → 重跑失败步骤 → 记录轮次
  - [ ] env/decision：写入 OPEN，停止自动修复，交研发确认
- [ ] 步骤 5：落盘报告 ⚠️ REQUIRED
  - [ ] 加载 `references/verify-report-template.md`
  - [ ] 默认路径：`docs/ai/compile-verify/{需求名}-编译验证报告-v{x.y}.md`
- [ ] 步骤 6：与 codegen 衔接
  - [ ] pass → 可进入 CR / 合入前审查（如 quick-arch-security-code-review）
  - [ ] blocked → 回流 codegen 或人工决策，禁止宣称可合入
```

## 步骤 0：前置门禁 ⛔ BLOCKING

自问：

- 《架构对齐报告》路径？关键项是否 **pass**？（来自 `quick-req-driven-codegen` 步骤 8–9）
- 本次迭代涉及哪些平台（仅 Web / 含 RN·ZRN / 含 Harmony）？
- 用户是否授权**直接改仓库**修复编译错误？（默认是；若用户仅要报告则只诊断不改动）

无对齐报告时：可仅做「局部文件编译诊断」，但**不得**标「本需求编译验证 pass」。

## 步骤 1：发现构建命令

加载 `references/build-command-discovery.md`。

**验证命令表**（执行前必填）：

| 阶段 | 命令 | 来源 |
|------|------|------|
| lint | | package.json / AGENTS.md |
| typecheck | | |
| web build | | |
| iOS bundle | | （native 时） |
| Android bundle | | |
| Harmony bundle | | |

命令未知时：Read 根目录与变更包路径的 `package.json`、`AGENTS.md`、`.github/workflows`；仍无法确定 → OPEN「缺标准 build 脚本」，交研发确认。

## 步骤 2：Web 管线

加载 `references/verify-pipeline-order.md`。

**顺序不可乱**：lint 与 typecheck 可并行仅当项目脚本明确支持；默认**串行**，先 lint 再 typecheck 再 build。

单步失败：**不要继续后续步骤**，进入步骤 4；通过后标记该步 pass 并进入下一步。

## 步骤 3：多平台 bundle

加载 `references/multi-platform-bundle.md`。

仅当对齐报告 §5 路由与平台或技术方案声明 **Native / ZRN / RN / Harmony** 时执行；纯 Web 标 **N/A**。

成功标准：对应平台打包命令 exit 0，且产物路径/体积与项目约定一致（见 reference）。

## 步骤 4：错误分流与修复

加载 `references/error-triage-and-fix.md`。

每轮修复须记录：

| 轮次 | 失败步骤 | 根因摘要 | 修改文件 | 重跑结果 |
|------|----------|----------|----------|----------|

**fix-rounds**（默认 3）：仅计 **auto-fix 重跑**轮次；env/decision-blocked 不计入但须 OPEN。

| 分类 | 动作 |
|------|------|
| auto-fix | 定位 → 最小 diff 修复 → 重跑失败步骤 |
| env-blocked | OPEN：缺 Node 版本、SDK、证书、私服、内存等 |
| decision-blocked | OPEN：契约与方案冲突、删改公开 API、lint 规则需团队豁免 |

**常见 auto-fix 域**（非穷举）：错误 import/alias、类型不匹配、字段重命名遗漏、错误依赖或未安装声明、eslint 可自动 fix 项、路径大小写、缺失 export。

## 步骤 5：报告与结论

加载 `references/verify-report-template.md`。

**门禁结论**：

| 结果 | 含义 |
|------|------|
| **pass** | 命令表内必需步骤全部通过 |
| **fixed-pass** | 经 auto-fix 后通过；报告附修复摘要 |
| **blocked** | env/decision OPEN 未解，或 fix-rounds 用尽仍有失败 |

## 确认门 ⚠️ REQUIRED

- 大范围删除/替换公开 API 才能过编译 → 须用户确认
- 修改 `eslint`/TS 配置或根 build 配置才能过 → 须用户确认
- 安装**新**依赖才能过 → 复述包名与用途，确认后安装
- 用户明确「只出报告不修」→ 步骤 4 仅分类不改动

## Anti-Patterns

- 只贴终端输出不修代码
- 跳过 lint 直接 build「看能不能过」
- 用 `@ts-ignore` / `eslint-disable` 整文件掩盖根因（除非 OPEN 已批准）
- 未验证对齐报告就宣称「编译通过可合入」
- 把 CI 未配的 native SDK 问题当成代码 bug 乱改
- fix-rounds 内重复相同失败却不换诊断思路
- 同时改多个无关模块「碰运气」

## Pre-Delivery Checklist

- [ ] 对齐报告门禁状态已记录（pass / 用户跳过说明）
- [ ] 《验证命令表》有来源依据，非臆造 script
- [ ] lint → typecheck → build（+ native 若适用）均已执行或标 N/A
- [ ] 失败项均有「根因 → 修复 → 重跑」或 OPEN 编号
- [ ] 《编译验证报告》已落盘（或用户只要口头结论时已给同等信息）
- [ ] 无未解释的 `@ts-ignore` / 整文件 disable 新增
- [ ] blocked 时未宣称 pass；OPEN 列表可交研发跟进
- [ ] **观测可扫描**：编译验证报告若记录首跑失败类别（lint/tsc/build），可供 `quick-pipeline-observability` 汇总

## 与相邻技能的关系

- **quick-req-driven-codegen**：上游；步骤 10 前须视觉 pass 或 UI-N/A。
- **quick-visual-audit**：UI 验收前置；视觉 pass 或 UI-N/A 后再执行本 skill；本 skill 不处理视觉偏差。
- **quick-arch-security-code-review**：下游；编译 pass 后建议做 CR，但 CR 不替代编译验证。
- **quick-tech-solution**：契约/字段争议以方案为准；decision-blocked 时引用方案章节。
- **quick-pipeline-observability**：下游只读扫描验证报告 → metrics。
