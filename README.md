# 萤石云无感睡眠伴侣 Home Assistant 集成

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

这是一个用于 Home Assistant 的自定义集成，可以将萤石云无感睡眠伴侣设备接入 Home Assistant。

## 功能特性

- ✅ 实时监测心率
- ✅ 实时监测呼吸率
- ✅ 睡眠状态监测（离床/清醒/浅睡/深睡/REM睡眠）
- ✅ 体动监测
- ✅ 睡眠评分
- ✅ 睡眠时长统计（深睡/浅睡/清醒）
- ✅ 支持多设备

## 安装方法

### 通过 HACS 安装（推荐）

1. 确保已安装 [HACS](https://hacs.xyz/)
2. 在 HACS 中点击右上角的三个点，选择"自定义存储库"
3. 添加此仓库的 URL，类别选择"Integration"
4. 在 HACS 中搜索"萤石云无感睡眠伴侣"并安装
5. 重启 Home Assistant

### 手动安装

1. 下载此仓库
2. 将 `custom_components/ezviz_sleep` 文件夹复制到你的 Home Assistant 配置目录下的 `custom_components` 文件夹中
3. 重启 Home Assistant

## 配置

1. 在 Home Assistant 中，进入"配置" -> "集成"
2. 点击右下角的"+ 添加集成"
3. 搜索"萤石云无感睡眠伴侣"
4. 输入萤石开放平台的 AppKey 和 AppSecret

### 获取 AppKey 和 AppSecret

如果你需要使用开放平台的 API：

1. 访问 [萤石开放平台](https://open.ys7.com/)
2. 注册并登录
3. 创建应用获取 AppKey 和 AppSecret

注意：此集成通过萤石开放平台 API 获取数据，必须提供 AppKey 和 AppSecret。

## 传感器说明

集成会为每个睡眠伴侣设备创建以下传感器：

| 传感器 | 说明 | 单位 |
|--------|------|------|
| 心率 | 实时心率 | bpm |
| 呼吸率 | 实时呼吸率 | 次/分 |
| 睡眠状态 | 当前睡眠状态 | - |
| 体动 | 体动情况 | - |
| 睡眠评分 | 睡眠质量评分 | - |
| 深睡时长 | 深度睡眠时长 | 分钟 |
| 浅睡时长 | 浅度睡眠时长 | 分钟 |
| 清醒时长 | 清醒时长 | 分钟 |

## 使用示例

### 在仪表板中显示睡眠数据

```yaml
type: entities
title: 睡眠监测
entities:
  - entity: sensor.睡眠伴侣_心率
  - entity: sensor.睡眠伴侣_呼吸率
  - entity: sensor.睡眠伴侣_睡眠状态
  - entity: sensor.睡眠伴侣_睡眠评分
```

### 创建自动化

```yaml
automation:
  - alias: "睡眠状态通知"
    trigger:
      - platform: state
        entity_id: sensor.睡眠伴侣_睡眠状态
        to: "深睡"
    action:
      - service: notify.mobile_app
        data:
          message: "已进入深度睡眠"
```

## 注意事项

1. 此集成通过萤石云 API 获取数据，需要网络连接
2. 数据更新间隔为 5 分钟
3. 请确保你的萤石云账号已绑定睡眠伴侣设备
4. API 接口可能会有变化，如遇问题请提交 Issue

## 常见问题

### Q: 无法登录萤石云
A: 请检查账号密码是否正确，确保账号已在萤石云 APP 中正常使用

### Q: 找不到设备
A: 请确保设备已在萤石云 APP 中正常添加和使用

### Q: 数据不更新
A: 检查网络连接，查看 Home Assistant 日志是否有错误信息

## 支持

如果你遇到问题或有建议，请在 [GitHub Issues](https://github.com/yourusername/ezviz_sleep/issues) 中提交。

## 许可证

MIT License

## 免责声明

此项目为非官方集成，与萤石云官方无关。使用此集成产生的任何问题由用户自行承担。
