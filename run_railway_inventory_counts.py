import sys

from mysql.connector import Error

from config.database import DatabaseConfig


def main():
    conn = None
    cursor = None
    try:
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')

        conn = DatabaseConfig.get_connection()
        if not conn:
            raise RuntimeError("Database connection failed")

        cursor = conn.cursor()

        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()[0]
        print(f"Current database: {current_db}")

        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Total tables: {len(tables)}")
        for t in sorted(tables):
            print(f"- {t}")

        def safe_count(table_name: str):
            if table_name not in tables:
                print(f"{table_name}: (table not found)")
                return
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            print(f"{table_name}: {cursor.fetchone()[0]}")

        def safe_scalar(label: str, sql: str):
            try:
                cursor.execute(sql)
                val = cursor.fetchone()[0]
                print(f"{label}: {val}")
            except Exception as e:
                print(f"{label}: (error: {e})")

        def safe_sample(label: str, sql: str, limit: int = 5):
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                print(f"{label}: showing {min(len(rows), limit)}/{len(rows)}")
                for r in rows[:limit]:
                    print(r)
            except Exception as e:
                print(f"{label}: (error: {e})")

        safe_count("medicines")
        safe_count("medicine_batches")
        safe_count("medicine_inventory")

        if "medicines" in tables:
            safe_scalar("medicines.sum_quantity_in_stock", "SELECT COALESCE(SUM(quantity_in_stock), 0) FROM medicines")
            safe_sample(
                "medicines.sample",
                "SELECT medicine_id, medicine_name, quantity_in_stock, status, expiry_date FROM medicines ORDER BY medicine_id ASC"
            )

        if "medicine_batches" in tables:
            safe_scalar("medicine_batches.sum_quantity", "SELECT COALESCE(SUM(quantity), 0) FROM medicine_batches")
            safe_scalar(
                "medicine_batches.distinct_status",
                "SELECT GROUP_CONCAT(DISTINCT status ORDER BY status SEPARATOR ', ') FROM medicine_batches"
            )
            safe_sample(
                "medicine_batches.sample",
                "SELECT id, medicine_id, batch_number, quantity, status, expiry_date FROM medicine_batches ORDER BY id ASC"
            )

    except Error as e:
        print(f"❌ MySQL Error: {e}")
        raise
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
