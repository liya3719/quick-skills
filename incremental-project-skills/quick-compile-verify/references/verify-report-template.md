# 编译验证报告模板

## 何时加载

步骤 5 落盘时。

## 默认路径

`docs/ai/compile-verify/{需求名}-编译验证报告-v{x.y}.md`

## 模板

```markdown
# 编译验证报告 — {需求名} v{x.y}

## 1. 元数据
- 对齐报告：{path}（关键项：pass / missing / 用户跳过）
- 执行计划：{path}
- 验证范围：web | native | all
- git 基线 / HEAD：
- fix-rounds：已用 n / 上限 N

## 2. 验证命令表
| 阶段 | 命令 | cwd | 结果 | 耗时 |
|------|------|-----|------|------|
| lint | | | pass/fail/N/A | |
| typecheck | | | | |
| web build | | | | |
| iOS bundle | | | N/A | |
| Android bundle | | | | |
| Harmony bundle | | | | |

## 3. 修复记录（若有）
| 轮次 | 步骤 | 根因 | 修改文件 | 重跑 |
|------|------|------|----------|------|

## 4. OPEN 项
（env-blocked / decision-blocked；无则写「无」）

## 5. 待验证项
（warning、仅 CI 可验项、需真机项）

## 6. 门禁结论
- **pass** / **fixed-pass** / **blocked**
- 可否进入代码审查 / 合入：是 / 否 + 原因
```

## 禁止

- 结论 pass 但命令表存在 fail 行
- 无修复记录却标 fixed-pass
