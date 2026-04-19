---
name: homekit-homebridge
description: Bridge HomeKit devices to Hermes Agent using Homebridge — control existing HomeKit accessories without resetting pairings or affecting iPhone/HomePod control.
trigger: 使用 HomeKit 控制智能家居设备时触发
---

# Homebridge + Hermes HomeKit 接入指南

## 架构说明

```
iPhone（家庭App）←→ Apple TV（家庭中枢）←→ HomeKit 设备
                                       ↑
                               Homebridge（第二控制器）
                                       ↑
                                   Hermes Agent
```

Homebridge 以「额外控制器」身份加入 HomeKit 网络，**不破坏现有配对**，iPhone 和 HomePod/Apple TV 照常使用。

---

## 自动安装（按顺序执行）

### 步骤 1/4：安装 Homebridge

```bash
npm install -g homebridge
```
验证：`homebridge --version`

---

### 步骤 2/4：安装 HomeKit Controller 插件

```bash
npm install -g homebridge-platform-homekit-controller
```

---

### 步骤 3/4：创建配置文件

Homebridge 配置路径：`~/.homebridge/config.json`

```json
{
  "bridge": {
    "name": "Hermes-Homebridge",
    "username": "AA:BB:CC:DD:EE:FF",
    "port": 51826,
    "pin": "031-45-154"
  },
  "platforms": [
    {
      "platform": "HomeKit-Controller",
      "name": "HomeKit Controller",
      "searchInterval": 3000,
      "discoverTime": 60
    }
  ],
  "accessories": []
}
```

---

### 步骤 4/4：启动 Homebridge

```bash
homebridge -D
```

启动后，日志中找：
- **PIN码**（格式 `XXX-YY-ZZZ`）
- **控制台地址**（通常是 `http://localhost:8581`）

---

## Hermes 连接 Homebridge

### 发现 Homebridge

```
homekit_discover(max_seconds=15)
```

Homebridge 的 Bonjour name 通常是 `Hermes-Homebridge._hap._tcp.local.`

### 配对

```
homekit_pair(alias="homebridge", device_id="<发现的device_id>", pin="<日志中的PIN>")
```

### 查看并控制设备

```
homekit_list_accessories(alias="homebridge")
homekit_put_characteristic(alias="homebridge", characteristic="1.8", value=true)
```

---

## 验证连通性（可选）

```bash
dns-sd -B _hap._tcp local.
```

---

## 故障排除

| 问题 | 解决方法 |
|------|---------|
| `homekit_discover` 找不到 | 确保防火墙允许 mDNS（5353/UDP） |
| 配对失败 | 检查 Homebridge 日志中是否开启「允许加入新设备」|
| Apple TV 不允许额外控制器 | 在 Apple TV 设置中检查「家庭中枢」权限 |
| 设备重启后消失 | 确认 `config.json` 中 `username`（MAC）不变 |

---

## 执行步骤

按顺序执行：

1. 安装 Homebridge → `npm install -g homebridge`
2. 安装 HomeKit Controller 插件 → `npm install -g homebridge-platform-homekit-controller`
3. 创建/更新 `~/.homebridge/config.json` 配置文件
4. 启动 Homebridge → `homebridge -D`
5. 找到日志中的 PIN，告诉我
6. 执行 `homekit_discover` 发现 Homebridge
7. 执行 `homekit_pair` 配对
8. 执行 `homekit_list_accessories` 查看设备
9. 开始控制 HomeKit 设备
