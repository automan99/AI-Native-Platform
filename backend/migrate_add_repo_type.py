"""
Migration script to add repo_type and github_repo_info columns
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

    # Columns to add
    columns = [
        ('repo_type', "VARCHAR(20) DEFAULT 'gitlab'", 'user_id'),
        ('github_repo_info', 'VARCHAR(200)', 'gitlab_project_id'),
    ]

    for col_name, col_def, after_col in columns:
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
