"""
Database Migration Script - Add Email/Password Authentication Fields
"""
import pymysql
import re
from app.config import Config

def parse_db_uri(uri):
    """Parse SQLAlchemy database URI"""
    # Format: mysql+pymysql://user:password@host:port/database
    match = re.match(r'mysql\+pymysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', uri)
    if match:
        return {
            'user': match.group(1),
            'password': match.group(2),
            'host': match.group(3),
            'port': int(match.group(4)),
            'database': match.group(5).split('?')[0]  # Remove query params
        }
    raise ValueError(f"Invalid database URI: {uri}")

def migrate():
    """Add missing columns to users table"""
    db_config = parse_db_uri(Config.SQLALCHEMY_DATABASE_URI)

    connection = pymysql.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Check if columns exist first
            cursor.execute("SHOW COLUMNS FROM users LIKE 'username'")
            if not cursor.fetchone():
                print("Adding username column...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN username VARCHAR(50) UNIQUE AFTER gitlab_token
                """)

            cursor.execute("SHOW COLUMNS FROM users LIKE 'email'")
            if not cursor.fetchone():
                print("Adding email column...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN email VARCHAR(200) UNIQUE AFTER username
                """)

            cursor.execute("SHOW COLUMNS FROM users LIKE 'password_hash'")
            if not cursor.fetchone():
                print("Adding password_hash column...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN password_hash VARCHAR(255) AFTER email
                """)

            cursor.execute("SHOW COLUMNS FROM users LIKE 'name'")
            if not cursor.fetchone():
                print("Adding name column...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN name VARCHAR(100) AFTER password_hash
                """)

            cursor.execute("SHOW COLUMNS FROM users LIKE 'avatar_url'")
            if not cursor.fetchone():
                print("Adding avatar_url column...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN avatar_url VARCHAR(500) AFTER name
                """)

            cursor.execute("SHOW COLUMNS FROM users LIKE 'is_active'")
            if not cursor.fetchone():
                print("Adding is_active column...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN is_active TINYINT(1) DEFAULT 1 AFTER avatar_url
                """)

            cursor.execute("SHOW COLUMNS FROM users LIKE 'email_verified'")
            if not cursor.fetchone():
                print("Adding email_verified column...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN email_verified TINYINT(1) DEFAULT 0 AFTER is_active
                """)

            cursor.execute("SHOW COLUMNS FROM users LIKE 'last_login_at'")
            if not cursor.fetchone():
                print("Adding last_login_at column...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN last_login_at DATETIME AFTER email_verified
                """)

        connection.commit()
        print("Migration completed successfully!")

        # Display current table structure
        print("\nCurrent users table structure:")
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE users")
            for row in cursor.fetchall():
                print(f"  {row['Field']}: {row['Type']}")

    except Exception as e:
        connection.rollback()
        print(f"Migration failed: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    migrate()
