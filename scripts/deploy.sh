 #!/bin/bash
# 一键 Docker 部署脚本

set -e

echo "🐳 构建并启动 Docker 服务..."
docker-compose up -d --build

echo "✅ 服务已启动！"
echo "访问 API: http://localhost:8000/api/v1"
echo "访问文档: http://localhost:8000/docs"