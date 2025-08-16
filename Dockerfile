# 使用 Python 3.11 的精简版本作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖，包括 xvfb 和 supercronic
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libdbus-glib-1-2 \
    curl \
    && rm -rf /var/lib/apt/lists/*  # 清理缓存减少镜像大小

# 安装 supercronic
RUN curl -L https://github.com/aptible/supercronic/releases/download/v0.1.7/supercronic-linux-amd64 -o /usr/local/bin/supercronic \
    && chmod +x /usr/local/bin/supercronic

# 安装 Python 依赖
RUN pip install --upgrade pip
RUN pip install playwright

# 安装 Playwright 依赖
RUN python -m playwright install

# 复制项目文件到容器中
COPY . /app

# 设置容器的入口命令，使用 supercronic 执行定时任务
CMD ["sh", "-c", "echo \"$CRON_EXPR xvfb-run --auto-servernum --server-args='-screen 0 1024x768x24' python /app/allow.py\" | supercronic /dev/stdin"]
