# 选择 Python 3.11 基础镜像
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget unzip xvfb libxi6 libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip playwright \
    && python -m playwright install

# 创建工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . /app

# 设置环境变量（可在运行时覆盖）
ENV RENEW_URL=""
ENV PASSWORD=""

# 启动命令
CMD xvfb-run --auto-servernum --server-args="-screen 0 1024x768x24" python allow.py
