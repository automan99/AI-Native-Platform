"""
AI Native 研发平台 - Scheduler Service
"""
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.sync_service import SyncService

_scheduler = None


def init_scheduler(app):
    """初始化定时调度器"""
    global _scheduler

    if _scheduler is not None:
        return

    _scheduler = BackgroundScheduler()

    # 添加定时同步任务
    from app.config import Config
    interval_minutes = getattr(Config, 'SYNC_INTERVAL_MINUTES', 60)

    _scheduler.add_job(
        func=scheduled_sync,
        trigger='interval',
        minutes=interval_minutes,
        id='sync_all_repos',
        replace_existing=True
    )

    _scheduler.start()

    with app.app_context():
        app.logger.info(f'Scheduler started with sync interval: {interval_minutes} minutes')


def scheduled_sync():
    """定时同步任务"""
    try:
        results = SyncService.sync_all()
        # 可以在这里添加日志记录
    except Exception as e:
        # 记录错误
        pass


def shutdown_scheduler():
    """关闭调度器"""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown()
        _scheduler = None
