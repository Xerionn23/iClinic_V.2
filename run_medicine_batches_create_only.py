import sys

import mysql.connector
from mysql.connector import Error

from config.database import DatabaseConfig


def main():
    try:
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')

        conn = DatabaseConfig.get_connection()
        if not conn:
            raise RuntimeError("Database connection failed")

        cursor = conn.cursor()

        create_sql = '''
            CREATE TABLE IF NOT EXISTS medicine_batches (
                id INT AUTO_INCREMENT PRIMARY KEY,
                medicine_id INT NOT NULL,
                batch_number VARCHAR(50) NOT NULL,
                quantity INT NOT NULL DEFAULT 0,
                expiry_date DATE NOT NULL,
                arrival_date DATE NOT NULL DEFAULT (CURRENT_DATE),
                supplier VARCHAR(255) DEFAULT NULL,
                cost_per_unit DECIMAL(10,2) DEFAULT NULL,
                notes TEXT DEFAULT NULL,
                status ENUM('available', 'expired', 'depleted') DEFAULT 'available',
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                KEY idx_medicine_batches_medicine_id (medicine_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        '''

        cursor.execute(create_sql)
        conn.commit()
        print("✅ medicine_batches table created successfully")

    except Error as e:
        print(f"❌ MySQL Error: {e}")
        raise
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
