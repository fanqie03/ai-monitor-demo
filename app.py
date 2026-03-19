#!/usr/bin/env python3
"""
模拟第三方API调用服务
暴露Prometheus指标：调用次数、耗时
"""

import time
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# 定义指标
# 第三方API调用次数
API_CALLS_total = Counter(
    'api_calls_total',
    'Total number of API calls',
    ['api_name', 'status']
)

# 第三方API调用耗时（秒）
API_CALL_DURATION_SECONDS = Histogram(
    'api_call_duration_seconds',
    'API call duration in seconds',
    ['api_name'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
)

# 模拟的第三方API列表
THIRD_PARTY_APIS = [
    'payment-service',    # 支付服务
    'user-service',       # 用户服务
    'order-service',      # 订单服务
    'notification-service', # 通知服务
    'analytics-service', # 分析服务
    'sms-service',        # 短信服务
    'email-service',      # 邮件服务
    'storage-service',    # 存储服务
]

# IM接口调用次数
INVOKE_IM = Counter(
    'invoke_im',
    'Total number of IM API calls'
)

# IM接口调用耗时（累计）
INVOKE_IM_COST = Counter(
    'invoke_im_cost',
    'Total IM API call duration in seconds'
)

# 卡片接口调用次数
INVOKE_CARD = Counter(
    'invoke_card',
    'Total number of Card API calls'
)

# 卡片接口调用耗时（累计）
INVOKE_CARD_COST = Counter(
    'invoke_card_cost',
    'Total Card API call duration in seconds'
)

# 服务暴露接口耗时（Histogram）
INVOKE_HIS = Histogram(
    'invokeHis',
    'Service API call duration in seconds',
    ['uri'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
)

# 模拟的服务接口列表
SERVICE_APIS = [
    '/api/user/info',
    '/api/order/list',
    '/api/product/detail',
    '/api/cart/get',
    '/api/payment/create',
]


def simulate_api_call(api_name: str) -> tuple:
    """模拟API调用，返回(状态, 耗时)"""
    # 模拟不同的耗时分布
    if api_name in ['payment-service', 'sms-service', 'email-service']:
        # 外部服务，耗时较长
        duration = random.expovariate(1/0.3)  # 平均300ms
    elif api_name in ['storage-service', 'analytics-service']:
        # I/O密集型，中等耗时
        duration = random.expovariate(1/0.15)  # 平均150ms
    else:
        # 内部服务，速度快
        duration = random.expovariate(1/0.08)  # 平均80ms
    
    duration = min(duration, 10.0)  # 最大10秒
    time.sleep(duration)
    
    # 模拟不同状态的响应
    status = random.choices(
        ['success', 'error', 'timeout'],
        weights=[95, 3, 2]
    )[0]
    
    return status, duration


def background_simulator():
    """后台线程：持续模拟API调用"""
    while True:
        # 随机选择1-3个API同时调用
        num_calls = random.randint(1, 3)
        apis_to_call = random.sample(THIRD_PARTY_APIS, num_calls)
        
        threads = []
        for api in apis_to_call:
            t = threading.Thread(target=call_api, args=(api,))
            t.start()
            threads.append(t)
        
        # 随机调用IM接口 (30%概率)
        if random.random() < 0.3:
            t = threading.Thread(target=call_im_api)
            t.start()
            threads.append(t)
        
        # 随机调用Card接口 (20%概率)
        if random.random() < 0.2:
            t = threading.Thread(target=call_card_api)
            t.start()
            threads.append(t)
        
        # 随机调用服务接口 (40%概率)
        if random.random() < 0.4:
            t = threading.Thread(target=call_service_api)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        # 随机间隔0.5-3秒
        time.sleep(random.uniform(0.5, 3.0))


def call_api(api_name: str):
    """执行API调用并记录指标"""
    status, duration = simulate_api_call(api_name)
    
    # 记录调用次数
    API_CALLS_total.labels(api_name=api_name, status=status).inc()
    
    # 记录耗时
    API_CALL_DURATION_SECONDS.labels(api_name=api_name).observe(duration)


def call_im_api():
    """调用IM接口并记录指标"""
    duration = random.expovariate(1/0.1)  # 平均100ms
    duration = min(duration, 5.0)
    time.sleep(duration)
    
    INVOKE_IM.inc()
    INVOKE_IM_COST.inc(duration)


def call_card_api():
    """调用卡片接口并记录指标"""
    duration = random.expovariate(1/0.2)  # 平均200ms
    duration = min(duration, 5.0)
    time.sleep(duration)
    
    INVOKE_CARD.inc()
    INVOKE_CARD_COST.inc(duration)


def call_service_api():
    """调用服务暴露的接口并记录histogram指标"""
    uri = random.choice(SERVICE_APIS)
    duration = random.expovariate(1/0.15)  # 平均150ms
    duration = min(duration, 5.0)
    time.sleep(duration)
    
    INVOKE_HIS.labels(uri=uri).observe(duration)


class PrometheusHandler(BaseHTTPRequestHandler):
    """处理Prometheus抓取请求"""
    
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(generate_latest())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # 抑制日志输出
        pass


def main():
    port = 8000
    
    # 启动后台模拟线程
    simulator_thread = threading.Thread(target=background_simulator, daemon=True)
    simulator_thread.start()
    
    # 启动HTTP服务器
    server = HTTPServer(('0.0.0.0', port), PrometheusHandler)
    print(f"[OK] Service started!")
    print(f"   - Prometheus metrics: http://localhost:{port}/metrics")
    print(f"   - Health check: http://localhost:{port}/health")
    print(f"   - Simulated APIs: {', '.join(THIRD_PARTY_APIS)}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[BYE] Service stopped")
        server.shutdown()


if __name__ == '__main__':
    main()
