from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = time.time()
        
        # 处理请求
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录请求信息
        logger.info(
            f"Method: {request.method} "
            f"Path: {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time:.2f}s"
        )
        
        return response


def setup_middleware(app):
    """设置中间件"""
    # CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 在生产环境中应该限制来源
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 请求日志中间件
    app.add_middleware(RequestLoggingMiddleware) 