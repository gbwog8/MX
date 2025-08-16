# 使用 Python 3.11 的精简版本作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装 Playwright 所需的系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*  # 清理缓存减少镜像大小

# 安装 Playwright 和其它 Python 依赖
RUN pip install --upgrade pip \
    && pip install playwright

# 安装 Playwright 浏览器
RUN python -m playwright install

# 复制项目文件到容器中
COPY . /app

# 设置容器的入口命令，使用 xvfb 运行脚本
CMD ["xvfb-run", "--auto-servernum", "--server-args='-screen 0 1024x768x24'", "python", "allow.py"]
