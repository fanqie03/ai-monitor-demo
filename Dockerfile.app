FROM python:3.11-slim

WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir prometheus-client

# 复制应用代码
COPY app.py .

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["python", "app.py"]
