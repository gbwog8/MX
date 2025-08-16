# 使用 Python 3.11 精简版基础镜像
FROM python:3.11-slim

# 设置时区（可按需修改，比如 Asia/Shanghai）
ENV TZ=Asia/Shanghai

# 安装系统依赖和 supercronic（轻量定时器）
RUN apt-get update && apt-get install -y \
    wget unzip xvfb libxi6 libdbus-glib-1-2 ca-certificates tzdata \
 && wget -O /usr/local/bin/supercronic https://github.com/aptible/supercronic/releases/latest/download/supercronic-linux-amd64 \
 && chmod +x /usr/local/bin/supercronic \
 && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip playwright \
 && python -m playwright install

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 默认入口：让 docker-compose 决定执行内容
ENTRYPOINT [ "sh", "-c" ]
