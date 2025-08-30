# 网站状态监控与警报器 - 完整部署教程

## 🎯 项目简介

这是一个功能强大的网站监控系统，能够：
- **24/7不间断监控**多个网站的健康状况
- **智能故障检测**：HTTP状态码、响应时间、页面内容检查
- **多种通知方式**：邮件警报、Webhook通知（支持Slack、钉钉等）
- **数据持久化**：SQLite数据库记录所有监控历史
- **可视化报告**：每日状态摘要和趋势分析

## 📋 环境要求

```bash
# Python版本要求
Python 3.7+

# 必需的Python包
pip install requests schedule sqlite3
```

## 🚀 快速开始

### 第一步：安装依赖

```bash
# 创建项目目录
mkdir website-monitor
cd website-monitor

# 安装依赖包
pip install requests schedule
```

### 第二步：创建配置文件

首次运行程序会自动生成 `monitor_config.json`，或手动创建：

```json
{
  "websites": [
    {
      "url": "https://www.google.com",
      "name": "Google搜索",
      "timeout": 10,
      "expected_status": 200,
      "check_interval": 300,
      "check_content": null
    },
    {
      "url": "https://github.com",
      "name": "GitHub代码托管",
      "timeout": 15,
      "expected_status": 200,
      "check_interval": 600,
      "check_content": "GitHub"
    },
    {
      "url": "https://your-website.com",
      "name": "我的网站",
      "timeout": 20,
      "expected_status": 200,
      "check_interval": 300,
      "check_content": "欢迎"
    }
  ],
  "email_config": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your_email@gmail.com",
    "password": "your_app_password",
    "from_email": "your_email@gmail.com",
    "to_emails": ["admin@example.com", "tech@example.com"]
  },
  "webhook_config": {
    "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json"
    }
  }
}
```

### 第三步：配置邮件通知

#### Gmail配置示例
```json
"email_config": {
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "username": "your_email@gmail.com",
  "password": "abcd efgh ijkl mnop",  // 应用专用密码
  "from_email": "your_email@gmail.com",
  "to_emails": ["admin@company.com"]
}
```

**Gmail设置步骤：**
1. 登录Gmail账户
2. 前往 Google账户设置 > 安全
3. 启用"两步验证"
4. 生成"应用专用密码"
5. 将应用密码填入配置文件

#### 其他邮箱配置
```json
# QQ邮箱
"email_config": {
  "smtp_server": "smtp.qq.com",
  "smtp_port": 587,
  "username": "your_qq@qq.com",
  "password": "your_authorization_code",
  "from_email": "your_qq@qq.com",
  "to_emails": ["admin@example.com"]
}

# 163邮箱
"email_config": {
  "smtp_server": "smtp.163.com",
  "smtp_port": 25,
  "username": "your_email@163.com",
  "password": "your_password",
  "from_email": "your_email@163.com",
  "to_emails": ["admin@example.com"]
}
```

### 第四步：配置Webhook通知

#### Slack Webhook配置
```json
"webhook_config": {
  "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

**Slack设置步骤：**
1. 访问 https://api.slack.com/apps
2. 创建新应用或选择现有应用
3. 启用"Incoming Webhooks"
4. 创建新的Webhook URL
5. 将URL添加到配置文件

#### 钉钉机器人配置
```json
"webhook_config": {
  "url": "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

#### 企业微信机器人配置
```json
"webhook_config": {
  "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

### 第五步：运行监控器

```bash
# 直接运行
python monitor.py

# 后台运行 (Linux/Mac)
nohup python monitor.py > monitor.log 2>&1 &

# Windows服务运行
# 使用任务计划程序或第三方工具
```

## 📊 功能详解

### 网站配置参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `url` | string | 要监控的网站URL | 必填 |
| `name` | string | 网站显示名称 | 必填 |
| `timeout` | int | 请求超时时间(秒) | 10 |
| `expected_status` | int | 期望的HTTP状态码 | 200 |
| `check_interval` | int | 检查间隔(秒) | 300 |
| `check_content` | string | 页面必须包含的内容 | null |