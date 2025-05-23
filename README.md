# 文本分析智能体 (Text Analysis Agent)

一个基于LangGraph和FastAPI的智能文本分析系统，支持文本分类、实体提取和摘要生成。

## ✨ 功能特性

- 🏷️ **文本分类**: 将文本自动分类为新闻、博客、研究或其他类别
- 🎯 **实体提取**: 识别并提取文本中的人物、组织、地点等实体
- 📝 **文本摘要**: 生成简洁明了的文本摘要
- 🚀 **高性能API**: 基于FastAPI的RESTful API服务
- 📊 **监控指标**: 内置Prometheus监控和Grafana可视化
- 🔒 **安全特性**: 请求限流、日志记录、错误处理
- 🐳 **容器化部署**: Docker和Docker Compose支持

## 🏗️ 项目结构

```
text-analysis-agent/
├── src/                    # 源代码
│   ├── core/              # 核心模块
│   │   ├── agent.py       # 文本分析智能体
│   │   └── models.py      # 数据模型
│   ├── api/               # API模块
│   │   ├── routes.py      # 路由定义
│   │   └── middleware.py  # 中间件
│   ├── config.py          # 配置管理
│   └── main.py           # 主应用程序
├── tests/                 # 测试文件
├── scripts/               # 部署脚本
├── docker-compose.yml     # Docker编排
├── Dockerfile            # Docker镜像配置
├── requirements.txt      # Python依赖
└── README.md            # 项目文档
```

## 🚀 快速开始

### 前置要求

- Python 3.11+
- Docker & Docker Compose (可选，用于容器化部署)
- 有效的OpenAI API密钥

### 1. 本地开发部署

```bash
# 克隆项目
git clone <repository-url>
cd text-analysis-agent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp config.env.example .env
# 编辑 .env 文件，设置您的API密钥

# 运行测试
python -m pytest tests/ -v

# 启动服务
chmod +x scripts/start.sh
./scripts/start.sh
```

### 2. Docker部署

```bash
# 快速部署
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# 手动部署
docker-compose up -d
```

## 📖 API使用指南

### 基础URL
- 本地开发: `http://localhost:8000/api/v1`
- Docker部署: `http://localhost/api/v1`

### 主要端点

#### 1. 文本分析
```http
POST /api/v1/analyze
Content-Type: application/json

{
  "text": "Anthropic的MCP技术是一个强大的API交互工具。",
  "include_classification": true,
  "include_entities": true,
  "include_summary": true,
  "language": "zh"
}
```

**响应示例**:
```json
{
  "original_text": "Anthropic的MCP技术是一个强大的API交互工具。",
  "classification": "研究",
  "entities": ["Anthropic", "MCP", "API"],
  "summary": "这是关于Anthropic公司MCP技术的介绍。",
  "processing_time": 1.23,
  "metadata": {
    "model": "qwen-plus",
    "text_length": 29
  }
}
```

#### 2. 健康检查
```http
GET /api/v1/health
```

#### 3. 服务信息
```http
GET /api/v1/info
```

### 客户端示例

#### Python
```python
import requests

# 分析文本
response = requests.post('http://localhost:8000/api/v1/analyze', json={
    'text': '这是一篇关于人工智能发展的新闻报道。',
    'include_classification': True,
    'include_entities': True,
    'include_summary': True
})

result = response.json()
print(f"分类: {result['classification']}")
print(f"实体: {result['entities']}")
print(f"摘要: {result['summary']}")
```

#### JavaScript
```javascript
const response = await fetch('http://localhost:8000/api/v1/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: '这是一篇关于人工智能发展的新闻报道。',
    include_classification: true,
    include_entities: true,
    include_summary: true
  })
});

const result = await response.json();
console.log('分析结果:', result);
```

#### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这是一篇关于人工智能发展的新闻报道。",
    "include_classification": true,
    "include_entities": true,
    "include_summary": true
  }'
```

## ⚙️ 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | OpenAI API密钥 | - | ✅ |
| `OPENAI_BASE_URL` | API基础URL | https://dashscope.aliyuncs.com/compatible-mode/v1 | ❌ |
| `OPENAI_MODEL` | 使用的模型 | qwen-plus | ❌ |
| `APP_HOST` | 服务主机 | 0.0.0.0 | ❌ |
| `APP_PORT` | 服务端口 | 8000 | ❌ |
| `LOG_LEVEL` | 日志级别 | INFO | ❌ |
| `RATE_LIMIT_REQUESTS` | 速率限制请求数 | 100 | ❌ |

### 模型支持

目前支持以下AI模型：
- Qwen-Plus (阿里云)
- GPT-3.5-turbo (OpenAI)
- GPT-4 (OpenAI)
- 其他兼容OpenAI API的模型

## 📊 监控和日志

### 访问监控面板

- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090

### 日志查看

```bash
# 查看应用日志
docker-compose logs -f text-analysis-api

# 查看所有服务日志
docker-compose logs -f

# 本地开发日志
tail -f logs/app.log
```

### 性能指标

系统会自动收集以下指标：
- 请求处理时间
- 请求成功率
- 错误率
- 文本长度分布
- 并发用户数

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_agent.py -v

# 生成覆盖率报告
python -m pytest tests/ --cov=src --cov-report=html
```

## 🚀 生产部署

### 1. 云服务器部署

```bash
# 在服务器上部署
git clone <repository-url>
cd text-analysis-agent

# 配置生产环境变量
cp config.env.example .env
# 编辑 .env 文件

# 部署
./scripts/deploy.sh
```

### 2. Kubernetes部署

查看 `k8s/` 目录中的Kubernetes配置文件。

### 3. 负载均衡

建议使用Nginx或云负载均衡器进行流量分发。

## 🔧 开发指南

### 代码结构

- `src/core/`: 核心业务逻辑
- `src/api/`: API接口层
- `src/config.py`: 配置管理
- `tests/`: 单元测试和集成测试

### 添加新功能

1. 在 `src/core/models.py` 中定义数据模型
2. 在 `src/core/agent.py` 中实现业务逻辑
3. 在 `src/api/routes.py` 中添加API端点
4. 编写相应的测试用例

### 代码规范

- 使用Python类型提示
- 遵循PEP 8代码规范
- 编写完整的文档字符串
- 添加适当的错误处理

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   ```
   解决方案: 检查 .env 文件中的 OPENAI_API_KEY 是否正确
   ```

2. **端口冲突**
   ```
   解决方案: 修改 .env 文件中的 APP_PORT 或停止占用端口的进程
   ```

3. **内存不足**
   ```
   解决方案: 增加服务器内存或调整Docker容器内存限制
   ```

### 日志分析

查看详细错误信息：
```bash
# Docker部署
docker-compose logs text-analysis-api | grep ERROR

# 本地部署
grep ERROR logs/app.log
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如有问题或建议，请：
- 提交 [Issue](../../issues)
- 发送邮件至 support@example.com
- 查看 [Wiki](../../wiki) 文档

---

**⭐ 如果这个项目对您有帮助，请给我们一个星标！** 