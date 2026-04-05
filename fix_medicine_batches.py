"""Fix medicine_batches table on Railway MySQL"""

import mysql.connector
from mysql.connector import Error
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Railway MySQL configuration
RAILWAY_CONFIG = {
    'host': 'junction.proxy.rlwy.net',
    'port': 13039,
    'user': 'root',
    'password': 'CNLIqKdjSPHVEBDqWbGVYdZUqzKXTzkz',
    'database': 'railway'
}


def fix_medicine_batches():
    print("Fixing medicine_batches table on Railway...")
    
    # Connect to Railway
    print("Connecting to Railway MySQL...")
    railway_conn = mysql.connector.connect(
        host=RAILWAY_CONFIG['host'],
        port=RAILWAY_CONFIG['port'],
        user=RAILWAY_CONFIG['user'],
        password=RAILWAY_CONFIG['password'],
        database=RAILWAY_CONFIG['database'],
        autocommit=True
    )
    
    cursor_railway = railway_conn.cursor()
    
    # Disable foreign key checks
    print("Disabling foreign key checks...")
    cursor_railway.execute("SET FOREIGN_KEY_CHECKS = 0;")
    
    # Drop existing table
    print("Dropping old table...")
    cursor_railway.execute("DROP TABLE IF EXISTS medicine_batches;")
    
    # Create table with compatible syntax
    print("Creating table with compatible syntax...")
    create_sql = """
    CREATE TABLE medicine_batches (
        id int(11) NOT NULL AUTO_INCREMENT,
        medicine_id int(11) NOT NULL,
        batch_number varchar(50) NOT NULL,
        quantity int(11) NOT NULL DEFAULT 0,
        expiry_date date NOT NULL,
        arrival_date date NOT NULL DEFAULT (CURRENT_DATE),
        supplier varchar(255) DEFAULT NULL,
        cost_per_unit decimal(10,2) DEFAULT NULL,
        notes text DEFAULT NULL,
        status enum('available','expired','depleted') DEFAULT 'available',
        created_at timestamp NOT NULL DEFAULT current_timestamp(),
        updated_at timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
        PRIMARY KEY (id),
        KEY idx_medicine_batches_medicine_id (medicine_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """
    cursor_railway.execute(create_sql)
    print("✅ Table created")
    
    # Re-enable foreign key checks
    print("Re-enabling foreign key checks...")
    cursor_railway.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    cursor_railway.close()
    railway_conn.close()
    
    print("\n✅ medicine_batches table created successfully!")
    print("Note: Table is empty. Data will be created through the app when needed.")


if __name__ == "__main__":
    fix_medicine_batches()
