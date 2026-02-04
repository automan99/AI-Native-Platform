"""
AI Native 研发平台 - Database Initialization Script
"""
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Repository, Resource, SyncLog, Stat

app = create_app()


def init_database():
    """初始化数据库表"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")


def drop_database():
    """删除所有数据库表"""
    with app.app_context():
        print("Dropping database tables...")
        db.drop_all()
        print("Database tables dropped successfully!")


def reset_database():
    """重置数据库"""
    drop_database()
    init_database()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'init':
            init_database()
        elif command == 'drop':
            drop_database()
        elif command == 'reset':
            reset_database()
        else:
            print("Usage: python init_db.py [init|drop|reset]")
    else:
        init_database()
