# 死代码与「染色」标注规范

> 在 Step 6 中严格遵循。与 Iron Law 一致。

## 定义

- **死代码（疑似）**：经静态分析/检索后，无引用、无入口、无构建产物的符号或分支；**未经研发确认前一律视为「疑似」**。

## 禁止

- 禁止在仓库中**直接删除**疑似死代码。
- 禁止在未经用户/研发**书面或对话明确**确认前，提交「只删线」的变更。

## 推荐标注（染色）形式

在审查报告中列出；若用户允许在代码中临时标注，**统一**使用以下**注释块**（便于 `grep` 与回滚）：

**单行适用：**
```
// [DEAD-CODE-CANDIDATE] reason=unused-export | confirmed-by=unconfirmed | ticket=TBD
```

**多行块：**
```
/* [DEAD-CODE-CANDIDATE] start
 * reason=无引用(见 2025-xx-xx 代码审查)
 * 删除前须: 研发确认 + 单测/回归项
 * [DEAD-CODE-CANDIDATE] end */
```

- `reason`：简要原因（如 `unreachable-after-return`、`unused-export`）。
- 语言无关：Python 用 `#`，SQL 用 `--`，在注释允许的语言中共用标签文本 `[DEAD-CODE-CANDIDATE]`。

## 研发确认后删除

- 由**研发**在确认后**自行**删除或发起 PR，或在本对话中**再次**明确「可以删除已标注块」后，执行删除。
