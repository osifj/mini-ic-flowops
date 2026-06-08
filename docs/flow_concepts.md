# IC Flow 概念

这个项目模拟的是一个非常简化的数字 IC 流程：

```text
precheck -> synth -> floorplan -> place -> route -> signoff
```

## precheck

检查输入数据是否完整，例如：

- 有没有 RTL
- 有没有 SDC 约束
- 有没有 README
- 有没有 IP 元数据

## synth

综合。真实工具会把 RTL 转成门级网表。

本项目里它只生成模拟指标：

- cell_count
- area_um2
- wns_ns

## floorplan

规划芯片面积、核心区域、宏单元位置。

## place

摆放标准单元。

## route

布线，连接各个单元。

## signoff

签核检查，常见内容：

- timing
- DRC
- LVS
- power

## Reference Flow 和 Testchip Flow

Reference Flow 是标准参考流程，重点是可复用。

Testchip Flow 会更完整，可能还包括：

- IP QA
- 测试数据收集
- 测试结果分析
- 汇总报告

