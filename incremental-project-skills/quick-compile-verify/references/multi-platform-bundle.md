# 多平台 Bundle 验证

## 何时加载

步骤 3；scope 为 `native` 或 `all`，或对齐报告 §5 含 Native/ZRN/Harmony 时。

## 平台判定

| 平台 | 触发条件 | 常见命令来源 |
|------|----------|--------------|
| **iOS** | 方案/RN/ZRN iOS 产物 | `package.json`：`bundle-ios` / `react-native bundle --platform ios` / 原生 `xcodebuild` |
| **Android** | 同上 Android | `bundle-android` / Gradle assemble / RN bundle |
| **Harmony** | HarmonyOS、鸿蒙、ArkTS 模块 | 项目 `hvigorw`、DevEco 构建脚本、内部 harmony 文档 |

先 Read **AGENTS.md** 与 **对齐报告 §5**；无 documented 命令 → OPEN，勿臆造。

## 验证标准

1. 打包命令 **exit 0**
2. **产物存在**且非 0 字节（常见路径示例，以项目为准）：
   - iOS：`*.jsbundle` / `main.jsbundle`、或 IPA 构建日志无 error
   - Android：`index.android.bundle`、`*release*.apk` 构建阶段无 error
   - Harmony：`*.hap` / 模块 `build` 输出目录
3. 日志无 **编译级** error（warning 可记入待验证项）

## 与 Web 关系

- Web build pass **不**替代 native bundle
- 纯 H5 容器内嵌且方案未要求独立 bundle → 标 **N/A** 并说明

## env-blocked（常见）

- Xcode / Android SDK / Harmony SDK 未安装
- 签名证书、provision profile 缺失
- 内网 Maven/npm 源不可达

以上 → **OPEN**，不修改业务代码冒充修复。

## 禁止

- 无 macOS 却声称已完成 iOS 本地 bundle（应 OPEN 或建议 CI）
- 跳过 bundle 仅因「Web 已过」
