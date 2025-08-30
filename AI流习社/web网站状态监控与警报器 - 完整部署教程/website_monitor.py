# 网站状态监控与警报器
# Website Status Monitor & Alert System
# 一个强大的网站监控工具，支持多种通知方式

import requests
import smtplib
import json
import time
import logging
import threading
from datetime import datetime, timedelta
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import List, Dict, Optional
import sqlite3
import schedule
from dataclasses import dataclass, asdict
import os
from pathlib import Path

# 配置数据结构
@dataclass
class WebsiteConfig:
    url: str
    name: str
    timeout: int = 10
    expected_status: int = 200
    check_content: Optional[str] = None
    check_interval: int = 300  # 5分钟

@dataclass
class EmailConfig:
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    from_email: str
    to_emails: List[str]

@dataclass
class WebhookConfig:
    url: str
    method: str = "POST"
    headers: Dict[str, str] = None

class DatabaseManager:
    """数据库管理器 - 存储监控历史"""
    
    def __init__(self, db_path: str = "monitor.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitor_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_name TEXT NOT NULL,
                url TEXT NOT NULL,
                status TEXT NOT NULL,
                response_time REAL,
                status_code INTEGER,
                error_message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_name TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                sent_successfully BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_check(self, website_name: str, url: str, status: str, 
                  response_time: float = None, status_code: int = None, 
                  error_message: str = None):
        """记录检查结果"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO monitor_logs 
            (website_name, url, status, response_time, status_code, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (website_name, url, status, response_time, status_code, error_message))
        
        conn.commit()
        conn.close()
    
    def log_alert(self, website_name: str, alert_type: str, message: str, 
                  sent_successfully: bool):
        """记录警报发送"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alert_logs 
            (website_name, alert_type, message, sent_successfully)
            VALUES (?, ?, ?, ?)
        ''', (website_name, alert_type, message, sent_successfully))
        
        conn.commit()
        conn.close()
    
    def get_website_history(self, website_name: str, hours: int = 24) -> List[Dict]:
        """获取网站历史记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM monitor_logs 
            WHERE website_name = ? 
            AND timestamp > datetime('now', '-{} hours')
            ORDER BY timestamp DESC
        '''.format(hours), (website_name,))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results

class NotificationManager:
    """通知管理器 - 处理各种通知方式"""
    
    def __init__(self, email_config: EmailConfig = None, 
                 webhook_config: WebhookConfig = None):
        self.email_config = email_config
        self.webhook_config = webhook_config
        self.logger = logging.getLogger(__name__)
    
    def send_email_alert(self, subject: str, message: str) -> bool:
        """发送邮件警报"""
        if not self.email_config:
            self.logger.warning("邮件配置未设置，跳过邮件通知")
            return False
        
        try:
            msg = MimeMultipart()
            msg['From'] = self.email_config.from_email
            msg['To'] = ', '.join(self.email_config.to_emails)
            msg['Subject'] = subject
            
            msg.attach(MimeText(message, 'html'))
            
            server = smtplib.SMTP(self.email_config.smtp_server, 
                                self.email_config.smtp_port)
            server.starttls()
            server.login(self.email_config.username, self.email_config.password)
            
            text = msg.as_string()
            server.sendmail(self.email_config.from_email, 
                          self.email_config.to_emails, text)
            server.quit()
            
            self.logger.info(f"邮件警报发送成功: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"邮件发送失败: {str(e)}")
            return False
    
    def send_webhook_alert(self, website_name: str, status: str, 
                          message: str) -> bool:
        """发送Webhook警报"""
        if not self.webhook_config:
            self.logger.warning("Webhook配置未设置，跳过Webhook通知")
            return False
        
        try:
            payload = {
                "website": website_name,
                "status": status,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            headers = self.webhook_config.headers or {}
            headers.setdefault('Content-Type', 'application/json')
            
            response = requests.request(
                method=self.webhook_config.method,
                url=self.webhook_config.url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info(f"Webhook警报发送成功: {website_name}")
                return True
            else:
                self.logger.error(f"Webhook发送失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Webhook发送失败: {str(e)}")
            return False

class WebsiteMonitor:
    """网站监控器 - 核心监控逻辑"""
    
    def __init__(self, config_file: str = "monitor_config.json"):
        self.config_file = config_file
        self.websites: List[WebsiteConfig] = []
        self.notification_manager: NotificationManager = None
        self.db_manager = DatabaseManager()
        self.website_status: Dict[str, Dict] = {}
        
        # 设置日志
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # 加载配置
        self.load_config()
    
    def setup_logging(self):
        """设置日志系统"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'monitor.log'),
                logging.StreamHandler()
            ]
        )
    
    def load_config(self):
        """加载配置文件"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # 加载网站配置
                self.websites = [
                    WebsiteConfig(**site) 
                    for site in config_data.get('websites', [])
                ]
                
                # 加载邮件配置
                email_config = config_data.get('email_config')
                if email_config:
                    self.notification_manager = NotificationManager(
                        email_config=EmailConfig(**email_config)
                    )
                
                # 加载Webhook配置
                webhook_config = config_data.get('webhook_config')
                if webhook_config and self.notification_manager:
                    self.notification_manager.webhook_config = WebhookConfig(**webhook_config)
                elif webhook_config:
                    self.notification_manager = NotificationManager(
                        webhook_config=WebhookConfig(**webhook_config)
                    )
                
                self.logger.info(f"配置加载成功，监控 {len(self.websites)} 个网站")
            else:
                self.create_default_config()
                
        except Exception as e:
            self.logger.error(f"配置加载失败: {str(e)}")
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            "websites": [
                {
                    "url": "https://www.google.com",
                    "name": "Google",
                    "timeout": 10,
                    "expected_status": 200,
                    "check_interval": 300
                },
                {
                    "url": "https://github.com",
                    "name": "GitHub",
                    "timeout": 15,
                    "expected_status": 200,
                    "check_content": "GitHub",
                    "check_interval": 600
                }
            ],
            "email_config": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "your_email@gmail.com",
                "password": "your_app_password",
                "from_email": "your_email@gmail.com",
                "to_emails": ["admin@example.com"]
            },
            "webhook_config": {
                "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
                "method": "POST",
                "headers": {"Content-Type": "application/json"}
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"已创建默认配置文件: {self.config_file}")
        self.logger.info("请编辑配置文件后重新启动监控器")
    
    def check_website(self, website: WebsiteConfig) -> Dict:
        """检查单个网站状态"""
        result = {
            'name': website.name,
            'url': website.url,
            'status': 'unknown',
            'response_time': None,
            'status_code': None,
            'error_message': None,
            'timestamp': datetime.now()
        }
        
        try:
            start_time = time.time()
            
            # 发送HTTP请求
            response = requests.get(
                website.url,
                timeout=website.timeout,
                allow_redirects=True,
                headers={'User-Agent': 'Website Monitor Bot 1.0'}
            )
            
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)  # 毫秒
            
            result['response_time'] = response_time
            result['status_code'] = response.status_code
            
            # 检查状态码
            if response.status_code == website.expected_status:
                # 检查页面内容（如果配置了）
                if website.check_content:
                    if website.check_content in response.text:
                        result['status'] = 'up'
                    else:
                        result['status'] = 'down'
                        result['error_message'] = f"页面不包含预期内容: {website.check_content}"
                else:
                    result['status'] = 'up'
            else:
                result['status'] = 'down'
                result['error_message'] = f"状态码异常: {response.status_code}"
            
            # 记录到数据库
            self.db_manager.log_check(
                website.name, website.url, result['status'],
                response_time, response.status_code, result['error_message']
            )
            
        except requests.exceptions.Timeout:
            result['status'] = 'down'
            result['error_message'] = f"请求超时 (>{website.timeout}s)"
            self.db_manager.log_check(
                website.name, website.url, result['status'],
                error_message=result['error_message']
            )
            
        except requests.exceptions.ConnectionError:
            result['status'] = 'down'
            result['error_message'] = "连接失败"
            self.db_manager.log_check(
                website.name, website.url, result['status'],
                error_message=result['error_message']
            )
            
        except Exception as e:
            result['status'] = 'down'
            result['error_message'] = f"未知错误: {str(e)}"
            self.db_manager.log_check(
                website.name, website.url, result['status'],
                error_message=result['error_message']
            )
        
        return result
    
    def handle_status_change(self, website_name: str, old_status: str, 
                           new_status: str, check_result: Dict):
        """处理状态变化"""
        if old_status == new_status:
            return
        
        self.logger.warning(f"网站状态变化: {website_name} {old_status} -> {new_status}")
        
        # 构建警报消息
        if new_status == 'down':
            subject = f"🚨 网站故障警报: {website_name}"
            message = self.build_down_alert_message(check_result)
        else:
            subject = f"✅ 网站恢复通知: {website_name}"
            message = self.build_recovery_alert_message(check_result)
        
        # 发送通知
        if self.notification_manager:
            # 邮件通知
            email_success = self.notification_manager.send_email_alert(subject, message)
            if email_success:
                self.db_manager.log_alert(website_name, "email", subject, True)
            
            # Webhook通知
            webhook_success = self.notification_manager.send_webhook_alert(
                website_name, new_status, message
            )
            if webhook_success:
                self.db_manager.log_alert(website_name, "webhook", subject, True)
    
    def build_down_alert_message(self, result: Dict) -> str:
        """构建故障警报消息"""
        return f"""
        <html>
        <body>
            <h2>🚨 网站监控警报</h2>
            <p><strong>网站名称:</strong> {result['name']}</p>
            <p><strong>网站地址:</strong> {result['url']}</p>
            <p><strong>当前状态:</strong> <span style="color: red;">离线</span></p>
            <p><strong>错误信息:</strong> {result['error_message']}</p>
            <p><strong>检查时间:</strong> {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <hr>
            <p style="color: gray; font-size: 12px;">
                此邮件由网站监控系统自动发送，请及时处理网站故障。
            </p>
        </body>
        </html>
        """
    
    def build_recovery_alert_message(self, result: Dict) -> str:
        """构建恢复通知消息"""
        return f"""
        <html>
        <body>
            <h2>✅ 网站恢复通知</h2>
            <p><strong>网站名称:</strong> {result['name']}</p>
            <p><strong>网站地址:</strong> {result['url']}</p>
            <p><strong>当前状态:</strong> <span style="color: green;">在线</span></p>
            <p><strong>响应时间:</strong> {result['response_time']}ms</p>
            <p><strong>状态码:</strong> {result['status_code']}</p>
            <p><strong>恢复时间:</strong> {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <hr>
            <p style="color: gray; font-size: 12px;">
                网站已恢复正常访问，感谢您的关注。
            </p>
        </body>
        </html>
        """
    
    def monitor_all_websites(self):
        """监控所有网站"""
        self.logger.info("开始监控所有网站...")
        
        for website in self.websites:
            try:
                # 检查网站
                result = self.check_website(website)
                
                # 获取之前的状态
                old_status = self.website_status.get(website.name, {}).get('status', 'unknown')
                
                # 更新状态
                self.website_status[website.name] = result
                
                # 处理状态变化
                self.handle_status_change(website.name, old_status, result['status'], result)
                
                # 日志记录
                if result['status'] == 'up':
                    self.logger.info(
                        f"✅ {website.name} 正常 - 响应时间: {result['response_time']}ms"
                    )
                else:
                    self.logger.warning(
                        f"❌ {website.name} 异常 - {result['error_message']}"
                    )
                    
            except Exception as e:
                self.logger.error(f"监控 {website.name} 时发生错误: {str(e)}")
    
    def get_status_summary(self) -> Dict:
        """获取状态摘要"""
        total = len(self.websites)
        up_count = sum(1 for status in self.website_status.values() 
                      if status.get('status') == 'up')
        down_count = total - up_count
        
        return {
            'total': total,
            'up': up_count,
            'down': down_count,
            'uptime_percentage': round((up_count / total * 100) if total > 0 else 0, 2)
        }
    
    def start_monitoring(self):
        """启动监控"""
        if not self.websites:
            self.logger.error("没有配置监控网站，请检查配置文件")
            return
        
        self.logger.info("🚀 网站监控器启动")
        self.logger.info(f"监控网站数量: {len(self.websites)}")
        
        # 立即执行一次检查
        self.monitor_all_websites()
        
        # 设置定期检查
        schedule.every(5).minutes.do(self.monitor_all_websites)
        
        # 每天发送状态报告
        schedule.every().day.at("09:00").do(self.send_daily_report)
        
        # 主循环
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次调度
                
        except KeyboardInterrupt:
            self.logger.info("监控器已停止")
    
    def send_daily_report(self):
        """发送每日状态报告"""
        if not self.notification_manager:
            return
        
        summary = self.get_status_summary()
        report_html = f"""
        <html>
        <body>
            <h2>📊 每日网站监控报告</h2>
            <p><strong>报告日期:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
            
            <h3>状态概览</h3>
            <ul>
                <li>总监控网站: {summary['total']}</li>
                <li>正常网站: {summary['up']}</li>
                <li>异常网站: {summary['down']}</li>
                <li>可用率: {summary['uptime_percentage']}%</li>
            </ul>
            
            <h3>各网站当前状态</h3>
            <table border="1" style="border-collapse: collapse;">
                <tr>
                    <th>网站名称</th>
                    <th>状态</th>
                    <th>响应时间</th>
                    <th>最后检查时间</th>
                </tr>
        """
        
        for name, status in self.website_status.items():
            status_color = "green" if status['status'] == 'up' else "red"
            report_html += f"""
                <tr>
                    <td>{name}</td>
                    <td style="color: {status_color};">{status['status']}</td>
                    <td>{status['response_time'] or 'N/A'}ms</td>
                    <td>{status['timestamp'].strftime('%H:%M:%S')}</td>
                </tr>
            """
        
        report_html += """
            </table>
            
            <hr>
            <p style="color: gray; font-size: 12px;">
                网站监控系统每日自动报告
            </p>
        </body>
        </html>
        """
        
        self.notification_manager.send_email_alert(
            f"📊 每日监控报告 - {datetime.now().strftime('%Y-%m-%d')}", 
            report_html
        )

def main():
    """主函数"""
    print("🚀 网站状态监控与警报器")
    print("=" * 50)
    
    monitor = WebsiteMonitor()
    
    try:
        monitor.start_monitoring()
    except Exception as e:
        logging.error(f"监控器启动失败: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())