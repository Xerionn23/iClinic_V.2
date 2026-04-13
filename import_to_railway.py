"""
Database Migration Script: XAMPP MySQL -> Railway MySQL
Run this script to migrate your local iclinic_db to Railway.
"""

import mysql.connector
from mysql.connector import Error
import sys
import os
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Local XAMPP MySQL configuration
LOCAL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Default XAMPP has no password
    'database': 'iclinic_db'
}

# Railway MySQL configuration (PUBLIC connection)
RAILWAY_CONFIG = {
    'host': 'junction.proxy.rlwy.net',
    'port': 13039,
    'user': 'root',
    'password': 'CNLIqKdjSPHVEBDqWbGVYdZUqzKXTzkz',
    'database': 'railway'
}


def get_connection(config, use_database=True):
    """Create a database connection"""
    try:
        conn_config = {
            'host': config['host'],
            'port': config['port'],
            'user': config['user'],
            'password': config['password'],
        }
        if use_database and 'database' in config:
            conn_config['database'] = config['database']
        
        connection = mysql.connector.connect(**conn_config, autocommit=True)
        return connection
    except Error as e:
        print(f"❌ Connection error: {e}")
        return None


def get_all_tables(connection, database):
    """Get list of all tables in a database"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {database}")
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables
    except Error as e:
        print(f"❌ Error getting tables: {e}")
        return []


def get_table_create_statement(connection, table_name):
    """Get CREATE TABLE statement for a table"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
        result = cursor.fetchone()
        cursor.close()
        return result[1] if result else None
    except Error as e:
        print(f"❌ Error getting CREATE TABLE for {table_name}: {e}")
        return None


def sanitize_create_table_sql(create_sql: str) -> str:
    """Make MySQL CREATE TABLE DDL more compatible across versions/providers."""
    if not create_sql:
        return create_sql

    sql = create_sql

    # Some providers reject DATE defaults that use function calls like CURDATE().
    # Prefer CURRENT_DATE which is the standard.
    sql = re.sub(r"\bDEFAULT\s+curdate\s*\(\s*\)", "DEFAULT (CURRENT_DATE)", sql, flags=re.IGNORECASE)

    return sql


def get_generated_columns(connection, table_name, database):
    """Get list of generated columns in a table (these cannot be inserted into)"""
    try:
        cursor = connection.cursor()
        query = """
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = %s 
            AND EXTRA LIKE '%GENERATED%'
        """
        cursor.execute(query, (database, table_name))
        generated = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return generated
    except Error as e:
        print(f"⚠️ Error checking generated columns: {e}")
        return []


def get_table_data(connection, table_name):
    """Get all data from a table"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM `{table_name}`")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        return columns, rows
    except Error as e:
        print(f"❌ Error getting data from {table_name}: {e}")
        return [], []


def escape_value(value):
    """Escape a value for SQL INSERT"""
    if value is None:
        return 'NULL'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, bytes):
        return f"0x{value.hex()}"
    else:
        # Escape string
        escaped = str(value).replace("\\", "\\\\").replace("'", "\\'")
        return f"'{escaped}'"


def create_insert_statement(table_name, columns, row, generated_columns=None):
    """Create INSERT statement for a row, excluding generated columns"""
    if generated_columns is None:
        generated_columns = []
    
    # Filter out generated columns
    filtered_cols = []
    filtered_vals = []
    for i, col in enumerate(columns):
        if col not in generated_columns:
            filtered_cols.append(col)
            filtered_vals.append(escape_value(row[i]))
    
    if not filtered_cols:
        return None  # Nothing to insert
    
    columns_str = ', '.join([f"`{col}`" for col in filtered_cols])
    values_str = ', '.join(filtered_vals)
    return f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({values_str});"


def migrate_database():
    """Main migration function"""
    print("=" * 60)
    print("🚀 DATABASE MIGRATION: XAMPP -> Railway")
    print("=" * 60)
    
    # Step 1: Connect to local database
    print("\n📡 Step 1: Connecting to local XAMPP MySQL...")
    local_conn = get_connection(LOCAL_CONFIG)
    if not local_conn:
        print("❌ Failed to connect to local database!")
        print("   Make sure XAMPP MySQL is running.")
        return False
    print("✅ Connected to local database")
    
    # Step 2: Get all tables from local
    print("\n📋 Step 2: Getting tables from local database...")
    tables = get_all_tables(local_conn, LOCAL_CONFIG['database'])
    if not tables:
        print("❌ No tables found in local database!")
        local_conn.close()
        return False
    print(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
    
    # Step 3: Connect to Railway
    print("\n📡 Step 3: Connecting to Railway MySQL...")
    railway_conn = get_connection(RAILWAY_CONFIG, use_database=False)
    if not railway_conn:
        print("❌ Failed to connect to Railway database!")
        local_conn.close()
        return False
    print("✅ Connected to Railway database")
    
    # Step 4: Create database on Railway if not exists
    print(f"\n🏗️ Step 4: Creating database '{RAILWAY_CONFIG['database']}' on Railway...")
    try:
        cursor = railway_conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{RAILWAY_CONFIG['database']}`")
        cursor.execute(f"USE `{RAILWAY_CONFIG['database']}`")
        cursor.close()
        print("✅ Database created/selected")
    except Error as e:
        print(f"❌ Error creating database: {e}")
        local_conn.close()
        railway_conn.close()
        return False
    
    # Step 5: Disable foreign key checks for migration
    print("\n� Step 5: Disabling foreign key checks...")
    cursor_railway = railway_conn.cursor()
    cursor_railway.execute("SET FOREIGN_KEY_CHECKS = 0;")
    print("✅ Foreign key checks disabled")
    
    # Step 6: Migrate each table
    print("\n📦 Step 6: Migrating tables...")
    cursor_local = local_conn.cursor()
    
    success_count = 0
    error_count = 0
    
    for table in tables:
        print(f"\n  📄 Processing table: {table}")
        
        # Get CREATE TABLE statement
        create_sql = get_table_create_statement(local_conn, table)
        if not create_sql:
            print(f"    ⚠️ Skipping {table} - could not get CREATE statement")
            error_count += 1
            continue

        create_sql = sanitize_create_table_sql(create_sql)
        
        # Drop table if exists on Railway (to avoid conflicts)
        try:
            cursor_railway.execute(f"DROP TABLE IF EXISTS `{table}`")
        except Error:
            pass
        
        # Create table on Railway
        try:
            cursor_railway.execute(create_sql)
            print(f"    ✅ Table created")
        except Error as e:
            print(f"    ❌ Error creating table: {e}")
            error_count += 1
            continue
        
        # Get data from local
        columns, rows = get_table_data(local_conn, table)
        if not rows:
            print(f"    ℹ️ No data to migrate")
            success_count += 1
            continue
        
        # Check for generated columns (cannot insert into these)
        generated_cols = get_generated_columns(local_conn, table, LOCAL_CONFIG['database'])
        if generated_cols:
            print(f"    ℹ️ Generated columns detected (will be excluded): {', '.join(generated_cols)}")
        
        # Insert data
        print(f"    📥 Inserting {len(rows)} rows...")
        inserted = 0
        for row in rows:
            try:
                insert_sql = create_insert_statement(table, columns, row, generated_cols)
                if insert_sql:
                    cursor_railway.execute(insert_sql)
                    inserted += 1
            except Error as e:
                print(f"    ⚠️ Error inserting row: {e}")
        
        print(f"    ✅ Inserted {inserted}/{len(rows)} rows")
        success_count += 1
    
    # Re-enable foreign key checks
    print("\n🔒 Re-enabling foreign key checks...")
    cursor_railway.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("✅ Foreign key checks re-enabled")
    
    cursor_local.close()
    cursor_railway.close()
    local_conn.close()
    railway_conn.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 MIGRATION SUMMARY")
    print("=" * 60)
    print(f"✅ Tables migrated successfully: {success_count}")
    print(f"❌ Tables with errors: {error_count}")
    print(f"📦 Total tables processed: {len(tables)}")
    
    if error_count == 0:
        print("\n🎉 MIGRATION COMPLETE! All tables migrated successfully!")
        print("\nNext steps:")
        print("1. Deploy your Flask app to Railway")
        print("2. Make sure Railway MySQL variables are available to your app")
        print("3. Your app should now connect to Railway MySQL automatically")
    else:
        print("\n⚠️ Migration completed with some errors. Check the output above.")
    
    return error_count == 0


if __name__ == "__main__":
    try:
        migrate_database()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
