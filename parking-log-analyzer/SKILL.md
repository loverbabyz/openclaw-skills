---
name: parking-log-analyzer
description: 泊车日志分析与问题定位。当用户提到泊车日志、RPA状态机、泊入泊出流程、QUIT码、BLE连接问题、车辆状态条件、或需要分析com.ics.secureKeyKit.log时触发。
---

# 泊车日志分析 Skill

分析 ICSCarKey 泊车日志，定位 BLE 连接问题、RPA 状态异常和车辆状态条件。

## 工作流：分析泊车日志

1. **收集日志文件** — 确认日志文件路径（通常是 `com.ics.secureKeyKit.log`）
2. **识别泊车会话** — 从日志中提取所有泊车会话（通过 `setParkType`、`setParkInStep`、`setParkOutStep`）
3. **解析状态机** — 按时间顺序还原每个会话的泊入/泊出状态流转
4. **关联错误上下文** — 收集 BLE 事件（`didUpdateConnection`）、RPA 错误（`💔[ERROR]`）、退出指示码（PAA_Quit_Indication）
5. **生成分析报告** — 判断完成/取消/异常，给出根因推断

## 关键日志标签

| 标签 | 含义 |
|------|------|
| `set park type:` | 泊车类型设置（1=泊入, 2=泊出, 3=离车泊入, 4=下电） |
| `set park in step:` | 泊入状态机步骤 |
| `set park out step:` | 泊出状态机步骤 |
| `didUpdateConnection` | BLE 连接状态变更 |
| `💔[ERROR]` + `[Rpa]` | RPA 层错误 |
| `PAA_Quit_Indication:` | 泊车退出原因码 |
| `condition:` + `[VC]` | 车辆状态条件（58字节 hex） |
| `didReceivePilotedParkingData` | 收到泊车数据回调 |

## 泊车类型

| 值 | 类型 |
|----|------|
| 0 | 未知 |
| 1 | 泊入 (ParkIn) |
| 2 | 泊出 (ParkOut) |
| 3 | 离车泊入 (InGuidance) |
| 4 | 下电 (PowerOff/T68) |

> [!tip]
> 查看完整状态机定义、退出码详解、车辆状态 hex 解析，见 [references/STATE_MACHINE.md](references/STATE_MACHINE.md) 和 [references/QUIT_CODES.md](references/QUIT_CODES.md)

## 常见问题快速定位

### BLE 连接断开导致泊车取消
- 日志特征：`didUpdateConnection` isConnected:0 出现在泊车过程中
- 常见原因：手机与车辆距离过远、蓝牙干扰、车机下电

### 状态机卡在"自检中"
- 日志特征：`set park in step: 10` 之后无后续步骤
- 常见原因：车辆条件不满足（见 `condition:` hex 数据）

### 泊车被取消（Cancel）
- 日志特征：`PAA_Quit_Indication` 出现非 0 值
- 处理方式：根据退出码查询原因（见 QUIT_CODES.md）

## 日志解析工具

泊车目录下有现成的解析脚本：

```bash
python3 泊车日志解析工具.py <日志文件路径> [输出HTML路径]
```

输出 HTML 报告包含：会话列表、状态机时间线、错误分类、BLE 事件、退出码汇总。

## 分析示例

给定一个泊车日志文件，分析步骤：

1. 运行解析工具生成 HTML 报告
2. 查看有多少泊车会话，成功/失败比例
3. 点击异常会话，查看状态机流转是否完整
4. 检查 quit_indications 确定取消原因
5. 对比 BLE 事件时间点和状态变更时间点

## 车辆状态条件 (condition) 格式

58 字节 hex 数据，各位定义见 [references/VEHICLE_CONDITION.md](references/VEHICLE_CONDITION.md)。关键字段：

- EPB 状态（字节 16-17）
- 挡位（字节 20-21）
- APA 状态（字节 28-29）
- PAA 退出指示码（字节 44-45）

## References

- [ICSCarKey泊车业务设计文档](../泊车/ICSCarKey泊车业务设计文档.md)
- [泊车日志解析工具](../泊车日志解析工具.py)
