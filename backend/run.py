"""
AI Native 研发平台 - Application Entry Point
"""
import os
from app import create_app, db
from app.services.scheduler_service import shutdown_scheduler

app = create_app()


@app.route('/')
def index():
    """健康检查接口"""
    return {
        'name': 'AI Native 研发平台',
        'version': '1.0.0',
        'status': 'running'
    }


@app.route('/health')
def health():
    """健康检查"""
    return {'status': 'ok'}


if __name__ == '__main__':
    try:
        # 开发环境
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        # 关闭定时任务
        shutdown_scheduler()
