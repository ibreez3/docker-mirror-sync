import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import os
import json

def get_timestamp_and_sign(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign

def send_dingtalk_notification():
    # 从环境变量获取配置
    webhook_token = os.environ.get('DINGTALK_ACCESS_TOKEN')
    secret = os.environ.get('DINGTALK_SECRET')
    
    # 获取工作流上下文信息
    workflow_status = os.environ.get('WORKFLOW_STATUS', 'unknown') # success, failure, cancelled
    repo_name = os.environ.get('GITHUB_REPOSITORY', 'unknown/repo')
    run_id = os.environ.get('GITHUB_RUN_ID', '')
    run_number = os.environ.get('GITHUB_RUN_NUMBER', '')
    actor = os.environ.get('GITHUB_ACTOR', 'ghost')
    
    # 获取阿里云配置
    aliyun_registry = os.environ.get('ALIYUN_REGISTRY', '')
    aliyun_namespace = os.environ.get('ALIYUN_NAMESPACE', '')
    
    # 获取成功同步的镜像列表
    success_images_str = os.environ.get('SUCCESS_IMAGES', '').strip()
    success_images = success_images_str.split() if success_images_str else []

    if not webhook_token or not secret:
        print("Error: DINGTALK_ACCESS_TOKEN or DINGTALK_SECRET is missing.")
        return

    # 构造基础 URL
    base_url = "https://oapi.dingtalk.com/robot/send"
    timestamp, sign = get_timestamp_and_sign(secret)
    webhook_url = f"{base_url}?access_token={webhook_token}&timestamp={timestamp}&sign={sign}"

    # 构造消息内容 (Markdown)
    
    # 1. 标题与颜色
    if workflow_status == 'success':
        title = "构建成功"
        color = "#00B42A" # 绿色
        status_icon = "✅"
    elif workflow_status == 'failure':
        title = "构建失败"
        color = "#F53F3F" # 红色
        status_icon = "❌"
    else:
        title = "构建取消/未知"
        color = "#FF7D00" # 橙色
        status_icon = "⚠️"

    # 2. 详情内容
    text_lines = [
        f"# {status_icon} Docker Sync: {title}",
        "---",
        f"- **仓库**: {repo_name}",
        f"- **触发者**: {actor}",
        f"- **任务 ID**: #{run_number}",
        f"- **状态**: <font color='{color}'>{workflow_status.upper()}</font>",
    ]

    # 3. 如果有同步成功的镜像，列出来
    if success_images:
        text_lines.append(f"\n**🚀 同步成功的镜像 ({len(success_images)}个):**")
        for img in success_images:
            # 计算目标镜像地址
            image_name_tag = img.split('/')[-1]
            if aliyun_registry and aliyun_namespace:
                target_image = f"{aliyun_registry}/{aliyun_namespace}/{image_name_tag}"
                # 格式化输出：源 -> 目标
                text_lines.append(f"> **Source**: `{img}`")
                text_lines.append(f"> **Target**: `{target_image}`")
                # 提供方便复制的 pull 命令
                text_lines.append(f"> ```bash\n> docker pull {target_image}\n> ```")
            else:
                # 如果没有配置阿里云信息，只显示源镜像
                text_lines.append(f"> - {img}")
            
            text_lines.append("> ---") # 分隔线

    elif workflow_status == 'success':
        text_lines.append("\n**ℹ️ 本次没有检测到需要同步的新镜像。**")

    # 4. 底部链接
    run_url = f"https://github.com/{repo_name}/actions/runs/{run_id}"
    text_lines.append(f"\n[查看工作流日志]({run_url})")

    markdown_content = "\n".join(text_lines)

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"镜像同步通知: {title}",
            "text": markdown_content
        }
    }

    try:
        response = requests.post(webhook_url, json=payload)
        result = response.json()
        if result.get('errcode') == 0:
            print("钉钉通知发送成功")
        else:
            print(f"钉钉通知发送失败: {result}")
    except Exception as e:
        print(f"发送请求异常: {e}")

if __name__ == "__main__":
    send_dingtalk_notification()
