# EZVIZ Sleep Companion for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

将萤石无感睡眠伴侣集成到 Home Assistant 中，实时监控您的睡眠质量。

## 功能

- 实时监测睡眠数据
- 支持多种传感器类型
- 中英文界面
- 可配置的更新间隔

## 安装

### 通过 HACS 安装（推荐）

1. 在 HACS 中，进入 "集成" 页面
2. 点击右下角的 "⋮" 按钮
3. 选择 "自定义存储库"
4. 在 "存储库" 字段中输入：`https://github.com/yourusername/ezviz-sleep-companion-ha`
5. 在 "类别" 下拉菜单中选择 "Integration"
6. 点击 "添加"
7. 在集成列表中找到 "EZVIZ Sleep Companion" 并点击安装

### 手动安装

1. 将 `custom_components/ezviz_sleep_companion` 文件夹复制到您的 Home Assistant 配置目录中的 `custom_components` 文件夹下
2. 重启 Home Assistant
3. 在配置 > 设备与服务 > 添加集成 中搜索 "EZVIZ Sleep Companion"

## 配置

1. 在 Home Assistant 中，进入 **配置** > **集成**
2. 点击 **+ 添加集成**
3. 搜索并选择 **EZVIZ Sleep Companion**
4. 输入以下信息：
   - **App Key**: 您的萤石开放平台 App Key
   - **App Secret**: 您的萤石开放平台 App Secret
   - **设备序列号**: 您的睡眠伴侣设备序列号
   - **设备名称** (可选): 为设备指定一个名称

## 可用传感器

### 传感器

| 名称 | 描述 | 单位 |
|------|-------------|------|
| 睡眠评分 | 睡眠质量评分 | % |
| 心率 | 实时心率 | bpm |
| 呼吸率 | 实时呼吸率 | rpm |
| 睡眠时长 | 总睡眠时间 | 分钟 |
| 深睡时长 | 深睡眠时间 | 分钟 |
| 浅睡时长 | 浅睡眠时间 | 分钟 |
| 睡眠效率 | 睡眠效率 | % |

### 二进制传感器

| 名称 | 描述 |
|------|-------------|
| 在床状态 | 是否在床上 |
| 入睡状态 | 是否已入睡 |

## 故障排除

- **无法连接**: 请检查您的网络连接和 API 凭据
- **数据不更新**: 检查更新间隔设置，或尝试重新加载集成
- **其他问题**: 请查看 Home Assistant 日志文件中的错误信息

## 贡献

欢迎提交问题和拉取请求！

## 许可证

MIT

---

*此集成由社区开发，与 EZVIZ 公司无关。*
