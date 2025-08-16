# Renew_X_Auto_Pardon

利用 Python 实现 Microsoft365 E5 Renew X 自动特赦  
可解除自动特赦时间要大于 30 的限制

---

## 使用方法1（Action 自动特赦）

#### 1. Fork 仓库
#### 2. 配置 GitHub Secrets
- 转到你 fork 的仓库页面  
- 点击 `Settings` → 左侧菜单中选择 `Secrets`  
- 添加以下 Secrets：
  - `RENEW_URL` : 包含 Microsoft365_E5_Renew_X 的公网访问链接（后面不带 `/`）
  - `PASSWORD` : 你的 Microsoft365_E5_Renew_X 登录密码  

#### 3. 启动 GitHub Actions
1. 在你的 fork 仓库中，进入 `Actions` 页面  
2. 如果 Actions 没有自动启用，点击 `Enable GitHub Actions` 激活它  
3. GitHub Actions 会按照你设置的定时任务（如每三天一次）自动运行脚本  
4. 需要手动触发时，可在 Actions 页面直接运行  

**示例 Secrets**：
```
RENEW_URL=https://www.example.com
PASSWORD=1234567890
```

---

## 使用方法2（本地启动）

#### 准备工作
1. 安装 Python  
2. 安装依赖：
```bash
python -m pip install --upgrade pip
pip install selenium
```
3. 下载脚本  
   链接：[auth_allow.py](https://raw.githubusercontent.com/OnlineMo/Microsoft365_E5_Renew_X_-/refs/heads/main/auth_allow.py)  
4. 修改脚本内初始化变量为对应值  
5. 运行脚本：
```bash
python auth_allow.py
```
也可加入 Windows 计划任务定时运行  

**playwright 版本**  
[auth_allow_playwright.py](https://github.com/OnlineMo/Microsoft365_E5_Renew_X_-/raw/refs/heads/main/auth_allow_playwright.py)（需自行研究）

---

## 使用方法3（Docker Hub 部署）

无需构建镜像，直接使用官方发布的 Docker 镜像：[onlinemo/renew_x_auto_pardon](https://hub.docker.com/r/onlinemo/renew_x_auto_pardon)

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
      - CRON_EXPR=0 8 * * *  # 每天早上 8 点运行一次
    command: >
      sh -c "echo \"$CRON_EXPR xvfb-run --auto-servernum --server-args='-screen 0 1024x768x24' python /app/allow.py\" | supercronic /dev/stdin"
    restart: unless-stopped
```

---

## 使用方法4（Docker 本地构建部署）

#### 1. 准备环境
- 安装 [Docker](https://docs.docker.com/get-docker/)  
- （可选）安装 [Docker Compose](https://docs.docker.com/compose/install/)

#### 2. 克隆项目
```bash
git clone https://github.com/OnlineMo/Renew_X_Auto_Pardon.git
cd Renew_X_Auto_Pardon
```

#### 3. 配置 `.env`
在项目根目录新建 `.env`：
```env
RENEW_URL=https://你的地址
PASSWORD=你的密码
CRON_EXPR=0 8 * * *   # 每天早上 8 点运行一次
```

---

#### 4. 构建并运行
```bash
docker build -t renew_x_auto_pardon .
docker run --rm \
    -e RENEW_URL="https://你的地址" \
    -e PASSWORD="你的密码" \
    renew_x_auto_pardon
```


#### 5. 使用 Docker Compose 定时运行
参考方法3中的 `docker-compose.yml` 示例


## Star
![Stargazers over time](https://starchart.cc/OnlineMo/Renew_X_Auto_Pardon.svg?variant=adaptive)

---
