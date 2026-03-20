# AGENTS.md - AI 监控 Demo 项目

## 项目概述

这是一个 Prometheus + Grafana 监控 Demo，通过模拟第三方 API 调用来暴露 Prometheus 指标。

## 技术栈

- **Python 3.11**: 主应用 (`app.py`)
- **Prometheus v2.40.0**: 时序数据库
- **Grafana 7.5.17**: 可视化仪表盘
- **Docker Compose**: 容器编排

## 命令

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行 Python 应用
python app.py

# 验证指标端点
curl http://localhost:8000/metrics
```

### Docker 命令

```bash
# 构建并启动所有服务
docker-compose up -d

# 代码修改后重新构建应用
docker-compose build --no-cache app && docker-compose up -d

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down -v
```

### 服务地址

| 服务 | 地址 | 凭据 |
|------|------|------|
| 应用 (指标) | http://localhost:8000/metrics | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / admin |

## 代码风格指南

### Python (app.py)

- **Shebang**: 可执行文件顶部使用 `#!/usr/bin/env python3`
- **文档字符串**: 使用三引号包裹模块和公共函数的文档
- **导入**: 标准库在前，第三方库在后，每组用空行分隔
  ```python
  import time
  import random
  import threading
  from http.server import HTTPServer, BaseHTTPRequestHandler
  from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
  ```
- **常量**: UPPER_SNAKE_CASE 命名（如 `THIRD_PARTY_APIS`，`API_CALLS_total`）
- **函数**: snake_case 命名，参数和返回值使用类型提示
- **注释**: 业务逻辑用中文注释，技术术语用英文
- **行长度**: 最多 120 字符

### Prometheus 指标命名

- Counter 指标: 使用 `_total` 后缀（如 `invoke_im_total`，不是 `invoke_im`）
- Histogram buckets: 使用标准延迟 buckets `(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)`
- 标签名: 使用 snake_case（如 `api_name`，不是 `apiName`）

### Grafana 仪表盘 (api-monitor.json)

- **数据源**: 使用字符串格式 `"datasource": "prometheus"`（不是对象格式），保证 Grafana 7.x 兼容性
- **聚合**: 多 Pod 场景下使用 `sum without (instance)` 正确聚合指标
- **面板 ID**: 必须使用唯一整数
- **YAML 配置**: 使用正确的 YAML 语法，不是 JSON（如 `datasources.yml`）

### Docker/Compose

- 镜像标签指定精确版本（如 `grafana/grafana:7.5.17`，不是 `grafana/grafana:latest`）
- 使用 `unless-stopped` 作为重启策略
- 使用有描述性的容器名称

## Git 规范

- 提交信息格式: `<type>: <description>`
  - 类型: `feat`, `fix`, `chore`, `docs`, `refactor`
- 示例: `feat: 添加 invokeHis histogram 指标用于服务接口监控`

## 添加新指标

1. 在 `app.py` 中使用 Counter 或 Histogram 定义指标
2. 在 `background_simulator()` 中添加模拟逻辑
3. 在 `api-monitor.json` 中添加对应的 Grafana 面板
4. 使用 `sum without (instance)` 进行聚合查询

## 文件结构

```
├── app.py                    # Python 指标导出器
├── Dockerfile.app            # 应用容器定义
├── docker-compose.yml        # 服务编排
├── prometheus.yml            # Prometheus 抓取配置
├── requirements.txt          # Python 依赖
├── README.md                # 项目文档
└── grafana/
    └── provisioning/
        ├── dashboards/
        │   └── dashboards/
        │       └── api-monitor.json  # Grafana 仪表盘
        └── datasources/
            └── datasources.yml      # Prometheus 数据源
```
