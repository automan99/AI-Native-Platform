"""
Migration script to add user_id column to repositories table
"""
import pymysql
from urllib.parse import urlparse

# Database connection info from config
DATABASE_URL = 'mysql+pymysql://root:password@localhost:3306/ai-agent-hub?charset=utf8mb4'

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

    # Check if user_id column already exists
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'repositories' AND COLUMN_NAME = 'user_id'
    """, (database,))

    if cursor.fetchone():
        print("Column 'user_id' already exists in repositories table.")
    else:
        # Add user_id column after id column
        print("Adding user_id column to repositories table...")
        cursor.execute("""
            ALTER TABLE repositories
            ADD COLUMN user_id INT NOT NULL DEFAULT 1
            AFTER id
        """)
        print("Added user_id column successfully.")

    conn.commit()
    cursor.close()
    conn.close()
    print("Migration completed successfully!")

except Exception as e:
    print(f"Migration failed: {e}")
