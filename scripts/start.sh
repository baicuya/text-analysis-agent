 #!/bin/bash
# 启动本地开发服务

echo "🔄 启动虚拟环境..."
if [ -d "venv" ]; then
  source venv/bin/activate
else
  echo "❌ 未找到虚拟环境，请先运行 python -m venv venv"
  exit 1
fi

echo "✅ 虚拟环境已激活"

echo "🔄 检查依赖..."
pip install -r requirements.txt

echo "🚀 启动 FastAPI 服务..."
export PYTHONPATH=.
python main.py server