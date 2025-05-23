# 🚀 文本分析智能体部署指南

本文档提供了文本分析智能体的详细部署说明，包括开发环境和生产环境的部署方式。

## 📋 部署前检查清单

### 系统要求
- [ ] Python 3.11+ 已安装
- [ ] Docker 和 Docker Compose 已安装（可选）
- [ ] 有效的OpenAI API密钥
- [ ] 至少 2GB 可用内存
- [ ] 网络连接正常

### 环境准备
```bash
# 检查Python版本
python --version  # 应该 >= 3.11

# 检查Docker（可选）
docker --version
docker-compose --version

# 检查网络连接
curl -I https://dashscope.aliyuncs.com
```

## 🛠️ 快速部署

### 方式一：本地开发部署（推荐新手）

```bash
# 1. 克隆项目
git clone <repository-url>
cd text-analysis-agent

# 2. 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp config.env.example .env

# 编辑 .env 文件，设置你的API密钥
nano .env  # 或使用其他编辑器
```

**必须配置的环境变量**：
```env
OPENAI_API_KEY=your-actual-api-key-here
```

```bash
# 5. 运行测试
python -m pytest tests/ -v

# 6. 启动服务
python main.py server
```

### 方式二：Docker部署（推荐生产环境）

```bash
# 1. 克隆项目
git clone <repository-url>
cd text-analysis-agent

# 2. 配置环境变量
cp config.env.example .env
# 编辑 .env 文件设置API密钥

# 3. 一键部署
./scripts/deploy.sh
```

## 🔧 详细配置说明

### 环境变量配置

创建 `.env` 文件，包含以下配置：

```env
# ===== 必须配置 =====
OPENAI_API_KEY=sk-your-api-key-here

# ===== 可选配置 =====
# OpenAI设置
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-plus

# 应用设置
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false

# 日志设置
LOG_LEVEL=INFO

# 性能设置
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### API密钥获取

#### 阿里云通义千问
1. 访问 [阿里云百炼平台](https://bailian.aliyun.com/)
2. 注册并创建应用
3. 获取API Key
4. 设置 `OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1`

#### OpenAI
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 创建API Key
3. 设置 `OPENAI_BASE_URL=https://api.openai.com/v1`

## 🧪 部署验证

### 1. 健康检查
```bash
# 本地部署
curl http://localhost:8000/api/v1/health

# Docker部署
curl http://localhost/health
```

### 2. 功能测试
```bash
# 运行客户端示例
python examples/client_example.py

# 或手动测试
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这是一个测试文本。",
    "include_classification": true,
    "include_entities": true,
    "include_summary": true
  }'
```

### 3. 性能测试
```bash
# 简单压力测试
for i in {1..10}; do
  curl -X POST "http://localhost:8000/api/v1/analyze" \
    -H "Content-Type: application/json" \
    -d '{"text": "性能测试文本 '$i'"}' &
done
wait
```

## 🌐 生产部署

### 1. 云服务器部署

#### 阿里云ECS
```bash
# 在ECS实例上执行
sudo apt update && sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# 克隆项目并部署
git clone <repository-url>
cd text-analysis-agent
cp config.env.example .env
# 配置.env文件
sudo ./scripts/deploy.sh
```

#### AWS EC2
```bash
# Amazon Linux 2
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 部署应用
git clone <repository-url>
cd text-analysis-agent
cp config.env.example .env
# 配置.env文件
./scripts/deploy.sh
```

### 2. 负载均衡配置

#### Nginx配置示例
```nginx
upstream text_analysis {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;  # 如果有多个实例
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://text_analysis;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. SSL证书配置

#### 使用Let's Encrypt
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 监控设置

### 1. 访问监控面板

部署完成后，可以访问以下监控面板：

- **应用主页**: http://your-server/
- **API文档**: http://your-server/docs
- **健康检查**: http://your-server/health
- **Grafana监控**: http://your-server:3000 (admin/admin123)
- **Prometheus指标**: http://your-server:9090

### 2. 设置告警

编辑 `prometheus.yml` 添加告警规则：

```yaml
rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

## 🔒 安全配置

### 1. 防火墙设置
```bash
# Ubuntu/Debian
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

### 2. API密钥安全
- 使用环境变量存储敏感信息
- 定期轮换API密钥
- 监控API使用情况
- 设置合理的请求限流

### 3. 网络安全
- 使用HTTPS
- 配置CORS策略
- 实施IP白名单（如需要）
- 定期更新依赖包

## 🐛 故障排除

### 常见问题及解决方案

#### 1. 端口被占用
```bash
# 查找占用端口的进程
sudo netstat -tlnp | grep :8000
# 或
sudo lsof -i :8000

# 杀死进程
sudo kill -9 <PID>
```

#### 2. API密钥错误
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 测试API连接
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://dashscope.aliyuncs.com/compatible-mode/v1/models
```

#### 3. 内存不足
```bash
# 检查内存使用
free -h
docker stats

# 增加虚拟内存
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 4. Docker相关问题
```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f text-analysis-api

# 重启服务
docker-compose restart

# 清理资源
docker-compose down
docker system prune -f
```

### 日志分析

#### 查看应用日志
```bash
# Docker部署
docker-compose logs -f text-analysis-api

# 本地部署
tail -f logs/app.log

# 搜索错误
grep -i error logs/app.log
```

#### 常见错误模式
- `ConnectionError`: 网络连接问题
- `AuthenticationError`: API密钥错误
- `RateLimitError`: 请求频率过高
- `TimeoutError`: 请求超时

## 📈 性能优化

### 1. 系统优化
```bash
# 增加文件描述符限制
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# 优化TCP参数
echo "net.core.rmem_max = 16777216" >> /etc/sysctl.conf
echo "net.core.wmem_max = 16777216" >> /etc/sysctl.conf
sysctl -p
```

### 2. 应用优化
- 使用连接池
- 实施缓存策略
- 优化数据库查询
- 配置合适的worker数量

### 3. 监控指标
- 响应时间
- 错误率
- 吞吐量
- 资源使用率

## 📞 获取支持

如果在部署过程中遇到问题：

1. 查看本文档的故障排除部分
2. 检查 [GitHub Issues](../../issues)
3. 发送邮件至 support@example.com
4. 查看 [项目Wiki](../../wiki)

---

**🎉 部署成功后，您就可以开始使用强大的文本分析功能了！** 