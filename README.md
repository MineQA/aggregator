# Aggregator - 免费代理池构建工具

[![GitHub stars](https://img.shields.io/github/stars/wzdnzd/aggregator.svg)](https://github.com/wzdnzd/aggregator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/wzdnzd/aggregator.svg)](https://github.com/wzdnzd/aggregator/network)
[![GitHub issues](https://img.shields.io/github/issues/wzdnzd/aggregator.svg)](https://github.com/wzdnzd/aggregator/issues)
[![License](https://img.shields.io/github/license/wzdnzd/aggregator.svg)](https://github.com/wzdnzd/aggregator/blob/main/LICENSE)

## 项目简介

一个用于爬取、验证、聚合并转换代理订阅的工具，支持多源爬取、机场注册、订阅处理和多后端推送。

### 核心特性

- 多源爬取：Telegram、GitHub、Google、Yandex、Twitter、网页、脚本插件
- 代理验证：连通性测试、活性检查、质量过滤
- 格式转换：Clash、V2Ray、SingBox 等
- 灵活存储：GitHub Gist、PasteGG、Imperial、本地存储等
- 插件扩展：支持自定义脚本爬虫

### 主要入口

- `subscribe/process.py`：完整处理流程，推荐优先使用
- `subscribe/collect.py`：简化收集流程，适合快速使用

### 快速开始

```bash
cp subscribe/config/config.default.json my-config.json
python subscribe/process.py -s my-config.json
```

### 文档

- [详细中文文档](README_CN.md)
- [English Docs](README_EN.md)

### 共享订阅

> 可前往 [Issue #91](https://github.com/wzdnzd/aggregator/issues/91) 获取共享订阅，量大质优，请勿浪费。

## 免责声明

- 本项目仅用于学习爬虫技术，请勿滥用
- 禁止用于任何违法违规或盈利用途
- 一切后果由使用者自行承担

## 致谢

1. <u>[Subconverter](https://github.com/asdlokj1qpi233/subconverter)</u>、<u>[Mihomo](https://github.com/MetaCubeX/mihomo)</u>
2. 感谢 [YXVM](https://yxvm.com) 与 [NodeSupport](https://github.com/NodeSeekDev/NodeSupport) 的赞助支持
