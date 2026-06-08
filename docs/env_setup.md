# Linux 环境配置

你现在是 Windows 电脑，已经装了 Linux 虚拟机。建议把这个项目复制到 Linux 虚拟机里练。

## 推荐环境

零基础优先：

```text
Ubuntu 22.04 / Ubuntu 24.04
```

更接近部分企业服务器：

```text
Rocky Linux 8/9
```

## Ubuntu 安装工具

```bash
sudo apt update
sudo apt install -y git make tcl python3 python3-venv
```

## Rocky Linux 安装工具

```bash
sudo dnf install -y git make tcl python3
```

## 配置项目环境

进入项目目录后：

```bash
source config/env.sh
flowctl doctor
```

`source config/env.sh` 做了两件事：

1. 设置 `FLOWOPS_ROOT`
2. 把 `bin/` 加入 `PATH`

所以之后可以直接输入：

```bash
flowctl run --design alu --flow ref
```

## 真实公司环境通常是什么样

你可能不会在自己的 VMware 里跑真实项目。更常见的是：

- Windows 办公机
- SSH 登录 Linux 服务器
- EDA 工具安装在共享目录
- 项目数据在公司内网磁盘
- license 由服务器统一管理

本项目先让你在虚拟机里学会基本动作，之后迁移到公司环境时主要是改工具路径和配置。

