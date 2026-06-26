# 稳定实现层顺序

## 何时加载

步骤 6 编码前**必读**；**不得跳层**（除非执行计划显式标 `layer-skip` + OPEN 理由）。

## 顺序 ⛔

对每个 **ready** block，按下列层级依次提交（同一层内可多文件，但须在本层完成后再进下一层）：

| 层 | 典型产物 | 说明 |
|----|----------|------|
| 1 **types** | `types.ts`、接口/枚举/DTO | 与方案契约一致；REQ 注释或映射 |
| 2 **api** | `api.ts`、请求封装、错误码映射 | 负载形状与方案一致 |
| 3 **state** | hooks、store、state 模块 | 数据流与方案状态机一致 |
| 4 **leaf** | 子组件、纯展示/交互单元 | 消费 token/metadata；禁截图臆造 |
| 5 **page** | 页面容器、布局编排 | 组装 leaf + state |
| 6 **route** | 路由表、Web 注册、深链 | 与方案路由/平台一致 |
| 7 **tracking** | 埋点、日志、可观测 | 与方案埋点关键词一致 |

## 与执行计划的关系

- 执行计划 block 的「目标文件」应标注所属层（1–7）
- 下层未 `ready` 时，上层不得引用其未定义契约

## 禁止

- 先写 page 再补 types/api
- 在 leaf/page 层硬编码 API 形状（应已在 types/api 层定义）
- 跳过 tracking 层却宣称 REQ 含埋点/NFR 已交付

## 栈差异

- **Vue / React**：leaf = SFC/TSX 子组件；page = 路由级视图
- **ZRN / 跨端**：route 层含原生/Web 双端注册；样式对齐报告单独列 **ZRN UI 与 token**

细节栈实践仍按 SKILL「渐进加载表」加载对应 reference。
