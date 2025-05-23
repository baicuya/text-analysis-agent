from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.api.middleware import RequestLoggingMiddleware

def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="文本分析服务",
        description="提供文本分类、实体识别和摘要生成功能",
        version="1.0.0"
    )
    
    # 添加 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 添加请求日志中间件
    app.add_middleware(RequestLoggingMiddleware)
    
    # 注册路由
    app.include_router(router, prefix="/api/v1")
    
    return app 