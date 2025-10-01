# Renew_X_Auto_Pardon

利用 Python + Playwright 实现 Microsoft365 E5 Renew X 自动特赦，解除自动特赦时间大于 30 天的限制。

---

## 使用方法

### 方法 1: GitHub Actions 自动特赦

1. Fork 仓库  
   进入仓库页面并点击 Fork：https://github.com/OnlineMo/Renew_X_Auto_Pardon

2. 配置 GitHub Secrets  
   在你的 fork 仓库页面，点击 Settings → Secrets → New repository secret，添加以下 Secrets：
   - RENEW_URL：Microsoft365 E5 Renew X 的公网访问链接（去掉结尾的 /）
   - PASSWORD：Microsoft365 E5 Renew X 登录密码

   示例：
   ```
   RENEW_URL=https://www.example.com
   PASSWORD=1234567890
   ```

3. 启用 GitHub Actions  
   - 进入 Actions 页面。如未自动启用，点击 Enable GitHub Actions。  
   - 工作流会运行 [allow.py](allow.py:1)（headless 模式，无需 Xvfb）。  
   - 可在 [.github/workflows/allow.yml](.github/workflows/allow.yml:1) 内调整定时策略（如启用 schedule）。

---

### 方法 2: 本地启动（Playwright）

1. 安装 Python（建议 3.11+）

2. 安装依赖
   ```bash
   python -m pip install --upgrade pip
   pip install playwright
   python -m playwright install chromium
   ```

3. 设置环境变量并运行
   - Linux/macOS:
     ```bash
     export RENEW_URL="https://你的地址"
     export PASSWORD="你的密码"
     python allow.py
     ```
   - Windows PowerShell:
     ```powershell
     $env:RENEW_URL="https://你的地址"
     $env:PASSWORD="你的密码"
     python allow.py
     ```

---

### 方法 3: Docker 运行

无需 Xvfb，容器内 headless 运行。

- 使用官方镜像（Docker Hub）
  ```bash
  docker run --rm \
    -e RENEW_URL="https://你的地址" \
    -e PASSWORD="你的密码" \
    onlinemo/renew_x_auto_pardon
  ```

- 使用本仓库提供的最小镜像（本地构建）
  ```bash
  docker build -t renew_x_auto_pardon .
  docker run --rm \
    -e RENEW_URL="https://你的地址" \
    -e PASSWORD="你的密码" \
    renew_x_auto_pardon
  ```

- 定时运行（通过环境变量 CRON_EXPR）
  ```bash
  docker run -d --name renew_x_auto_pardon \
    -e RENEW_URL="https://你的地址" \
    -e PASSWORD="你的密码" \
    -e CRON_EXPR="0 8 * * *" \
    renew_x_auto_pardon
  ```

---

### 方法 4: Docker Compose 定时运行

使用仓库内的 [docker-compose.yml](docker-compose.yml:1)（服务名 renew_x_auto_pardon，内置 ENTRYPOINT 支持 CRON）。

```yaml
version: "3.9"

services:
  renew_x_auto_pardon:
    build: .
    container_name: renew_x_auto_pardon
    environment:
      RENEW_URL: ${RENEW_URL}
      PASSWORD: ${PASSWORD}
      CRON_EXPR: "0 8 * * *"  # 每天早上 8 点执行一次
    restart: unless-stopped
```

- 建议在 compose 文件中以映射方式设置 CRON_EXPR（如上所示），避免在 .env 中因空格导致解析问题。  
- 一次性执行：删除或留空 CRON_EXPR 即可。

---

## 文件说明

- 主执行脚本：[allow.py](allow.py:1)
- Docker 构建文件：[Dockerfile](Dockerfile:1)
- Compose 模板：[docker-compose.yml](docker-compose.yml:1)
- GitHub Actions 工作流：[.github/workflows/allow.yml](.github/workflows/allow.yml:1)
- 示例环境变量：[.env.example](.env.example:1)（不建议在 .env 中写入 CRON_EXPR，建议在 compose 中设置）

---

## Star

![Stargazers over time](https://starchart.cc/OnlineMo/Renew_X_Auto_Pardon.svg?variant=adaptive)
