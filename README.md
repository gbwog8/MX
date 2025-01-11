# Microsoft365_E5_Renew_X_-
Microsoft365 E5 Renew X 自动特赦

## 使用方法1（Action自动特赦）
#### 1.**配置 GitHub Secrets**
```
    - 转到你 fork 的仓库页面。
    - 点击 `Settings`，然后在左侧菜单中选择 `Secrets`。
    - 添加以下 Secrets：
        - `RENEW_URL`: 包含Microsoft365_E5_Renew_X的公网访问链接。
        - `PASSWORD`: 你的Microsoft365_E5_Renew_X登录密码。
        
#### 2.**启动 GitHub Actions**
1. **配置 GitHub Actions**
    - 在你的 fork 仓库中，进入 `Actions` 页面。
    - 如果 Actions 没有自动启用，点击 `Enable GitHub Actions` 按钮以激活它。

2. **运行工作流**
    - GitHub Actions 将会根据你设置的定时任务（例如每三天一次）自动运行脚本。
    - 如果需要手动触发，可以在 Actions 页面手动运行工作流。

#### 示例 Secrets

- **RENEW_URL**
    - 示例值: `https://www.example.com`
    - 请注意，后面不带/

- **PASSWORD**
    - 示例值: `1234567890`

## 使用方法2（本地启动）
#### 准备工作
1. **安装python**
2. **安装对应的库**
   - 运行以下命令
   ```bash
    python -m pip install --upgrade pip
    pip install selenium
   ```
3. **下载脚本**
  - 链接：`https://raw.githubusercontent.com/OnlineMo/Microsoft365_E5_Renew_X_-/refs/heads/main/.github/workflows/auth_allow.py`
4. **修改脚本**
   - 将脚本内初始化的变量设为对应值
5. **运行脚本**
   - `python auth_allow.py`
   - auth_allow.py替换为脚本路径

可以添加进Windows自动任务
