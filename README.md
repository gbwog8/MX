# Renew\_X\_Auto\_Pardon

利用 Python 实现 **Microsoft365 E5 Renew X 自动特赦**
解除自动特赦时间大于 30 天的限制。

---

## 使用方法

### 方法 1: GitHub Actions 自动特赦

1. **Fork 仓库**
   进入 [仓库页面](https://github.com/OnlineMo/Renew_X_Auto_Pardon) 并点击 `Fork`，将仓库复制到你的 GitHub 账户。

2. **配置 GitHub Secrets**
   在你的 fork 仓库页面，点击 `Settings` → `Secrets` → `New repository secret`，添加以下 Secrets：

   * `RENEW_URL`：Microsoft365 E5 Renew X 的公网访问链接（去掉结尾的 `/`）
   * `PASSWORD`：Microsoft365 E5 Renew X 登录密码

   **示例 Secrets 配置**：

   ```
   RENEW_URL=https://www.example.com
   PASSWORD=1234567890
   ```

3. **启用 GitHub Actions**

   * 进入 `Actions` 页面。
   * 如果 Actions 没有自动启用，点击 `Enable GitHub Actions` 激活它。
   * GitHub Actions 会按照你设置的定时任务（如每三天一次）自动运行脚本。
   * 需要手动触发时，可直接在 `Actions` 页面运行。

---

### 方法 2: 本地启动

1. **安装 Python**
   确保你的计算机上已安装 Python 3.x，安装方式可参考 [Python 官方文档](https://www.python.org/downloads/)。

2. **安装依赖**
   执行以下命令来安装 Python 依赖：

   ```bash
   python -m pip install --upgrade pip
   pip install selenium
   ```

3. **下载脚本**
   下载并修改初始化变量，脚本链接：[auth\_allow.py](https://raw.githubusercontent.com/OnlineMo/Microsoft365_E5_Renew_X_-/refs/heads/main/auth_allow.py)

4. **运行脚本**
   在终端运行以下命令启动脚本：

   ```bash
   python auth_allow.py
   ```

5. **定时运行（Windows 计划任务）**
   可以在 Windows 中设置计划任务定期运行脚本。

**playwright 版本**
[auth\_allow\_playwright.py](https://github.com/OnlineMo/Microsoft365_E5_Renew_X_-/raw/refs/heads/main/auth_allow_playwright.py)（需自行研究）

---

### 方法 3: Docker Hub 部署

无需构建镜像，直接使用官方发布的 Docker 镜像：[onlinemo/renew\_x\_auto\_pardon](https://hub.docker.com/r/onlinemo/renew_x_auto_pardon)

#### 快速运行（立即执行一次）

```bash
docker run --rm \
  -e RENEW_URL="https://你的地址" \
  -e PASSWORD="你的密码" \
  onlinemo/renew_x_auto_pardon
```

#### Docker Compose 示例（定时运行）

```yaml
version: "3.9"

services:
  renew_x_auto_pardon:
    image: onlinemo/renew_x_auto_pardon
    container_name: renew_x_auto_pardon
    environment:
      - RENEW_URL=https://你的地址
      - PASSWORD=你的密码
      - CRON_EXPR="0 8 * * *"  # 每天早上 8 点运行一次
    volumes:
      - ./app:/app  # 挂载本地项目文件
    command: >
      sh -c "echo \"$CRON_EXPR xvfb-run --auto-servernum --server-args='-screen 0 1024x768x24' python /app/allow.py\" | supercronic /dev/stdin"
    restart: unless-stopped
```

---

### 方法 4: 本地构建 Docker 镜像

#### 1. 准备环境

* 安装 [Docker](https://docs.docker.com/get-docker/)
* （可选）安装 [Docker Compose](https://docs.docker.com/compose/install/)

#### 2. 克隆项目

```bash
git clone https://github.com/OnlineMo/Renew_X_Auto_Pardon.git
cd Renew_X_Auto_Pardon
```

#### 3. 配置 `.env`

在项目根目录新建 `.env` 文件，配置你的环境变量：

```env
RENEW_URL=https://你的地址
PASSWORD=你的密码
CRON_EXPR="0 8 * * *"  # 每天早上 8 点运行一次
```

#### 4. 构建并运行 Docker 镜像

```bash
docker build -t renew_x_auto_pardon .
docker run --rm \
    -e RENEW_URL="https://你的地址" \
    -e PASSWORD="你的密码" \
    renew_x_auto_pardon
```

#### 5. 使用 Docker Compose 定时运行

参考方法 3 中的 `docker-compose.yml` 示例，配置定时任务。

---

## Star

![Stargazers over time](https://starchart.cc/OnlineMo/Renew_X_Auto_Pardon.svg?variant=adaptive)

这个修改后的 **README** 已经更加清晰，涵盖了 GitHub Actions、Docker 部署和本地启动的所有常见方法，同时注重了简洁性和易用性。
