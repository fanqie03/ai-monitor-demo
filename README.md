# 第三方API监控 Demo

使用 Prometheus + Grafana 监控第三方依赖接口的调用次数和耗时。

## 架构

```
┌─────────────┐     metrics      ┌─────────────┐     queries      ┌─────────────┐
│  Python App │ ──────────────► │  Prometheus │ ◄──────────────► │   Grafana   │
│  (模拟服务)  │    /metrics     │   (时序数据库) │                 │  (可视化)    │
└─────────────┘                  └─────────────┘                 └─────────────┘
```

## 快速开始

### 方式一：Docker Compose (推荐)

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 方式二：本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动Python模拟服务
python app.py

# 3. 手动启动Prometheus (配置 prometheus.yml)
# 4. 手动启动Grafana (访问 http://localhost:3000)
```

## 服务地址

| 服务 | 地址 | 说明 |
|------|------|------|
| Python模拟服务 | http://localhost:8000 | 模拟API调用 |
| Prometheus | http://localhost:9090 | 时序数据库 |
| Grafana | http://localhost:3000 | 可视化仪表盘 |

## 登录信息

- **Grafana**: admin / admin
- **Prometheus**: 无需认证

## 暴露的指标

### IM接口指标
调用IM接口时记录

```
# HELP invoke_im_total Total number of IM API calls
# TYPE invoke_im_total counter
invoke_im_total

# HELP invoke_im_cost_total Total IM API call duration in seconds
# TYPE invoke_im_cost_total counter
invoke_im_cost_total
```

### 卡片接口指标
调用卡片接口时记录

```
# HELP invoke_card_total Total number of Card API calls
# TYPE invoke_card_total counter
invoke_card_total

# HELP invoke_card_cost_total Total Card API call duration in seconds
# TYPE invoke_card_cost_total counter
invoke_card_cost_total
```

### api_calls_total
第三方API调用总次数

```
# 标签
- api_name: API名称 (payment-service, user-service, order-service 等)
- status: 调用状态 (success, error, timeout)

# 示例
api_calls_total{api_name="payment-service",status="success"}
```

### api_call_duration_seconds
第三方API调用耗时

```
# 标签
- api_name: API名称

# 直方图 buckets
[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
```

## 模拟的第三方API

- payment-service (支付服务)
- user-service (用户服务)
- order-service (订单服务)
- notification-service (通知服务)
- analytics-service (分析服务)
- sms-service (短信服务)
- email-service (邮件服务)
- storage-service (存储服务)

## Grafana 仪表盘

Dashboard 包含以下面板：

### IM接口监控
1. **IM调用次数 (每秒)** - 展示IM接口的调用频率
2. **IM平均响应时间** - IM接口的平均响应时间

### 卡片接口监控
1. **Card调用次数 (每秒)** - 展示卡片接口的调用频率
2. **Card平均响应时间** - 卡片接口的平均响应时间

### 第三方API监控
1. **API调用次数 (每秒)** - 展示各API的调用频率，按状态分色
2. **API调用耗时 (秒)** - 展示P50/P95/P99耗时曲线
3. **平均响应时间** - 各API的平均响应时间
4. **错误率 (%)** - 各API的错误率百分比
5. **耗时分布直方图** - 调用耗时的分布情况

## 清理

```bash
# 停止并删除容器
docker-compose down -v
```

## 自定义

### 添加新的API

修改 `app.py` 中的 `THIRD_PARTY_APIS` 列表：

```python
THIRD_PARTY_APIS = [
    'payment-service',
    'user-service',
    'order-service',
    # 添加新API
    'new-api-service',
]
```

### 修改Prometheus抓取间隔

编辑 `prometheus.yml`：

```yaml
global:
  scrape_interval: 5s  # 改为其他值
```
