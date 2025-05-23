from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.api.middleware import setup_middleware

# 创建FastAPI应用
app = FastAPI(
    title="文本分析智能体",
    description="基于LangGraph和FastAPI的智能文本分析系统",
    version="1.0.0"
)

# 设置中间件
setup_middleware(app)

# 注册路由
app.include_router(router, prefix="/api/v1")

# 根路由
@app.get("/")
async def root():
    """根路由"""
    return {
        "message": "欢迎使用文本分析智能体",
        "docs_url": "/docs",
        "version": "1.0.0"
    } 