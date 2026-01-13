# 集成 Logo 说明

## 需要添加的图标文件

为了让集成在 HACS 和 Home Assistant 中显示图标，需要添加以下文件：

### 1. 品牌图标（必需）
在 `custom_components/ezviz_sleep/` 目录下添加：

- **icon.png** - 256x256 像素的 PNG 图标
- **icon@2x.png** - 512x512 像素的高清 PNG 图标（可选）

### 2. 图标设计建议

图标应该：
- 使用萤石云的品牌色（蓝色系）
- 包含睡眠相关的元素（如月亮、床、心率波形等）
- 背景透明
- 简洁清晰，在小尺寸下也能识别

### 3. 图标来源

你可以：
1. **使用萤石云官方图标** - 从萤石云 APP 或官网获取
2. **自己设计** - 使用 Figma、Photoshop 等工具设计
3. **使用在线工具** - 如 Canva、Flaticon 等

### 4. 添加图标的步骤

1. 准备好 256x256 的 PNG 图标
2. 命名为 `icon.png`
3. 放到 `custom_components/ezviz_sleep/` 目录
4. （可选）准备 512x512 的图标，命名为 `icon@2x.png`

### 5. 临时方案

如果暂时没有图标，Home Assistant 会使用默认图标。你可以稍后再添加。

### 6. 图标示例

建议的图标元素组合：
- 🌙 月亮 + 💤 睡眠符号
- 💓 心率图 + 🛏️ 床
- 萤石云 Logo + 睡眠元素

## 更新 manifest.json

图标文件添加后，不需要修改 manifest.json，Home Assistant 会自动识别 `icon.png` 文件。
