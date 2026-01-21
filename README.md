# Docker Mirror Sync

利用 GitHub Actions 的海外网络环境，解决国内服务器 `docker pull` 官方镜像慢或失败的问题。
工作流会自动拉取 `mirror-list.txt` 中指定的镜像，并推送到你的阿里云容器镜像服务 (ACR)。

## 🚀 功能特点

- **高速拉取**：利用 GitHub Actions (Azure US) 网络拉取 Docker Hub 官方镜像。
- **自动推送**：自动打标并推送到指定的阿里云 ACR 仓库。
- **消息通知**：支持钉钉机器人 Webhook 通知（带加签），实时掌握同步状态。
- **配置简单**：只需修改 `mirror-list.txt` 即可触发同步。
- **安全可靠**：支持 GitHub Secrets 管理敏感信息。

## 🛠️ 使用方法

### 1. 准备工作
- **阿里云 ACR**：拥有阿里云账号，开通容器镜像服务 (ACR)，创建命名空间 (Namespace)。
- **钉钉机器人**：在钉钉群组中添加自定义机器人，安全设置选择“加签”，获取 `Access Token` 和 `Secret`。

### 2. 配置参数
建议使用 **GitHub Secrets** 进行安全配置。在 GitHub 仓库的 `Settings` -> `Secrets and variables` -> `Actions` 中添加以下 Secrets：

#### 基础配置 (阿里云 ACR)
| Secret Name | 说明 | 示例值 |
| :--- | :--- | :--- |
| `ALIYUN_REGISTRY` | 阿里云 ACR 地址 | `registry.cn-hangzhou.aliyuncs.com` |
| `ALIYUN_NAMESPACE` | 阿里云命名空间 | `my-docker-repo` |
| `ALIYUN_USERNAME` | 阿里云账号用户名 | (手机号或邮箱) |
| `ALIYUN_PASSWORD` | ACR 访问凭证密码 | (注意：这是在 ACR 控制台设置的独立密码) |

#### 通知配置 (钉钉机器人) - 可选
| Secret Name | 说明 | 示例值 |
| :--- | :--- | :--- |
| `DINGTALK_ACCESS_TOKEN` | 机器人 Access Token | `a4b55...` |
| `DINGTALK_SECRET` | 机器人加签 Secret | `SEC...` |

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
- 钉钉通知配置成功后，无论同步成功还是失败，都会发送通知；成功通知中会列出本次同步的镜像列表。
