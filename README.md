# Docker Mirror Sync

利用 GitHub Actions 的海外网络环境，解决国内服务器 `docker pull` 官方镜像慢或失败的问题。
工作流会自动拉取 `mirror-list.txt` 中指定的镜像，并推送到你的阿里云容器镜像服务 (ACR)。

## 🚀 功能特点

- **高速拉取**：利用 GitHub Actions (Azure US) 网络拉取 Docker Hub 官方镜像。
- **自动推送**：自动打标并推送到指定的阿里云 ACR 仓库。
- **配置简单**：只需修改 `mirror-list.txt` 即可触发同步。
- **安全可靠**：支持 GitHub Secrets 管理敏感信息。

## 🛠️ 使用方法

### 1. 准备工作
你需要拥有一个阿里云账号，并开通容器镜像服务 (ACR)，创建一个命名空间 (Namespace) 和镜像仓库。

### 2. 配置参数
你可以通过以下两种方式之一配置阿里云 ACR 信息：

**方式 A：使用 GitHub Secrets（推荐，更安全）**
在 GitHub 仓库的 `Settings` -> `Secrets and variables` -> `Actions` 中添加以下 Secrets：
- `ALIYUN_REGISTRY`: 你的阿里云 ACR 地址 (例如 `registry.cn-hangzhou.aliyuncs.com`)
- `ALIYUN_NAMESPACE`: 你的阿里云命名空间 (例如 `my-docker-repo`)
- `ALIYUN_USERNAME`: 阿里云账号用户名 (通常是手机号或邮箱)
- `ALIYUN_PASSWORD`: 阿里云 ACR 访问凭证密码 (注意：这是在 ACR 控制台设置的独立密码，非阿里云登录密码)

**方式 B：直接修改 Workflow 文件**
修改 `.github/sync-docker.yaml` 文件中的 `步骤2`，填入你的阿里云信息。

### 3. 添加镜像
修改根目录下的 `mirror-list.txt` 文件，一行一个镜像地址：
```text
ubuntu:22.04
mysql:8.0
redis:alpine
```

### 4. 触发同步
- **自动触发**：提交 `mirror-list.txt` 的修改到 GitHub 仓库。
- **手动触发**：在 GitHub 仓库的 `Actions` 页面，选择 `Docker 镜像同步`，点击 `Run workflow`。

## 📝 注意事项
- 请确保 GitHub Actions Runner 能访问你的阿里云 ACR 仓库。
