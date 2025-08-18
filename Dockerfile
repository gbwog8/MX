# 使用 Python 3.11 的精简版本作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（包含 xvfb、supercronic 以及 Chromium 运行所需库）
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libdbus-glib-1-2 \
    libnspr4 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libasound2 \
    curl \
 && rm -rf /var/lib/apt/lists/*

# 安装 supercronic
RUN curl -L https://github.com/aptible/supercronic/releases/download/v0.1.7/supercronic-linux-amd64 \
    -o /usr/local/bin/supercronic \
 && chmod +x /usr/local/bin/supercronic

# 升级 pip 并安装 Python 依赖
RUN pip install --upgrade pip
RUN pip install playwright

# 安装 Playwright 浏览器及其运行依赖
RUN python -m playwright install-deps && \
    python -m playwright install chromium

# 复制项目文件
COPY . /app

# 默认启动逻辑：
# 如果有 CRON_EXPR，则用 supercronic 定时执行
# 如果没设置 CRON_EXPR，则直接运行一次并退出
CMD ["sh", "-c", "\
  if [ -n \"$CRON_EXPR\" ]; then \
    echo \"$CRON_EXPR xvfb-run --auto-servernum --server-args='-screen 0 1024x768x24' python /app/allow.py\" | supercronic /dev/stdin; \
  else \
    xvfb-run --auto-servernum --server-args='-screen 0 1024x768x24' python /app/allow.py; \
  fi \
"]
