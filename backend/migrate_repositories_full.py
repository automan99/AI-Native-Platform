"""
Complete migration script for repositories table
"""
import pymysql
from urllib.parse import urlparse

# Database connection info from config
DATABASE_URL = 'mysql+pymysql://ai-agent-hub:we5ir3wp5hRDcjea@119.28.226.35:3306/ai-agent-hub?charset=utf8mb4'

# Parse DATABASE_URL
parsed = urlparse(DATABASE_URL)
host = parsed.hostname or 'localhost'
port = parsed.port or 3306
user = parsed.username or 'root'
password = parsed.password or 'password'
database = parsed.path.lstrip('/') if parsed.path else 'ai-agent-hub'

print(f"Connecting to MySQL: {user}@{host}:{port}/{database}")

try:
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    # Columns to add
    columns_to_add = [
        ('user_id', 'INT NOT NULL DEFAULT 1', 'id'),
        ('description', 'VARCHAR(500)', 'name'),
        ('branch', 'VARCHAR(100)', 'url'),
        ('path', 'VARCHAR(500)', 'branch'),
        ('auth_type', 'VARCHAR(20) DEFAULT "public"', 'path'),
        ('auth_token', 'TEXT', 'auth_type'),
        ('ssh_key', 'TEXT', 'auth_token'),
        ('sync_mode', 'VARCHAR(20) DEFAULT "manual"', 'ssh_key'),
        ('sync_interval', 'INT DEFAULT 60', 'sync_mode'),
        ('sync_enabled', 'BOOLEAN DEFAULT TRUE', 'sync_interval'),
        ('enabled', 'BOOLEAN DEFAULT TRUE', 'sync_enabled'),
        ('sync_status', 'VARCHAR(20) DEFAULT "pending"', 'enabled'),
        ('last_sync_at', 'DATETIME', 'sync_status'),
        ('last_sync_status', 'VARCHAR(20)', 'last_sync_at'),
        ('error_message', 'TEXT', 'last_sync_status'),
        ('webhook_secret', 'TEXT', 'error_message'),
        ('webhook_url', 'VARCHAR(500)', 'webhook_secret'),
    ]

    for col_name, col_def, after_col in columns_to_add:
        # Check if column already exists
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'repositories' AND COLUMN_NAME = %s
        """, (database, col_name))

        if cursor.fetchone():
            print(f"Column '{col_name}' already exists.")
        else:
            print(f"Adding column '{col_name}'...")
            cursor.execute(f"""
                ALTER TABLE repositories
                ADD COLUMN {col_name} {col_def}
                AFTER {after_col}
            """)
            print(f"Added column '{col_name}' successfully.")

    conn.commit()
    cursor.close()
    conn.close()
    print("\nMigration completed successfully!")

except Exception as e:
    print(f"Migration failed: {e}")
