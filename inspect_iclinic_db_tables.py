from config.database import DatabaseConfig


def main():
    conn = DatabaseConfig.get_connection()
    if not conn:
        print("ERROR: Database connection failed")
        return 1

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name",
            (DatabaseConfig.MYSQL_DATABASE,),
        )
        tables = [r[0] for r in cur.fetchall()]
        cur.close()

        print(f"Database: {DatabaseConfig.MYSQL_DATABASE}")
        print(f"Tables: {len(tables)}")
        print("\nROW COUNTS:")

        for t in tables:
            c = conn.cursor()
            try:
                c.execute(f"SELECT COUNT(*) FROM `{t}`")
                cnt = c.fetchone()[0]
                print(f"{t}: {cnt}")
            except Exception as e:
                print(f"{t}: ERROR ({e})")
            finally:
                try:
                    c.close()
                except Exception:
                    pass
        return 0
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
