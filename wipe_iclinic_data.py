import os
import sys
from pathlib import Path

from config.database import DatabaseConfig


CONFIRM_PHRASE = "WIPE_ICLINIC_DATA"

# User requested to keep ONLY:
# - nurses table
# - specific users rows (from screenshot)
# - clinic_events
KEEP_ONLY_TABLES = {
    "nurses",
    "clinic_events",
    "users",
}

KEEP_USERS_USER_IDS = {
    "IT-001",
    "NURSE-001",
}


KEEP_TABLES_EXACT = set()


KEEP_TABLES_PREFIXES = tuple()


WIPE_TABLES_PREFIXES = tuple()


WIPE_TABLES_EXACT = set()


CANDIDATE_UPLOAD_DIRS = (
    "static/uploads",
    "static/upload",
    "uploads",
    "upload",
    "assets/uploads",
    "assets/upload",
)


def _is_keep_table(table_name: str) -> bool:
    t = (table_name or "").strip()
    if not t:
        return True
    if t in KEEP_ONLY_TABLES:
        return True
    if t in KEEP_TABLES_EXACT:
        return True
    for p in KEEP_TABLES_PREFIXES:
        if t.startswith(p):
            return True
    return False


def _is_wipe_table(table_name: str) -> bool:
    t = (table_name or "").strip()
    if not t:
        return False
    # With current requirement, wipe everything not in KEEP_ONLY_TABLES.
    if t not in KEEP_ONLY_TABLES:
        return True
    if t in WIPE_TABLES_EXACT:
        return True
    for p in WIPE_TABLES_PREFIXES:
        if t.startswith(p):
            return True
    return False


def _get_row_count(conn, table: str) -> int:
    c = conn.cursor()
    try:
        c.execute(f"SELECT COUNT(*) FROM `{table}`")
        return int(c.fetchone()[0] or 0)
    finally:
        try:
            c.close()
        except Exception:
            pass


def _fetch_all_tables(conn):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name",
            (DatabaseConfig.MYSQL_DATABASE,),
        )
        return [r[0] for r in cur.fetchall()]
    finally:
        try:
            cur.close()
        except Exception:
            pass


def _truncate_tables(conn, tables):
    cur = conn.cursor()
    try:
        cur.execute("SET FOREIGN_KEY_CHECKS=0")
        for t in tables:
            cur.execute(f"TRUNCATE TABLE `{t}`")
            print(f"TRUNCATED: {t}")
        cur.execute("SET FOREIGN_KEY_CHECKS=1")
    finally:
        try:
            cur.close()
        except Exception:
            pass


def _prune_users_table(conn):
    if "users" not in KEEP_ONLY_TABLES:
        return
    if not KEEP_USERS_USER_IDS:
        return

    cur = conn.cursor()
    try:
        placeholders = ",".join(["%s"] * len(KEEP_USERS_USER_IDS))
        cur.execute(
            f"DELETE FROM `users` WHERE `user_id` NOT IN ({placeholders})",
            tuple(sorted(KEEP_USERS_USER_IDS)),
        )
        print(f"PRUNED users (kept user_id in {sorted(KEEP_USERS_USER_IDS)})")
    finally:
        try:
            cur.close()
        except Exception:
            pass


def _delete_upload_files(project_root: Path):
    deleted_files = 0
    deleted_dirs = 0

    for rel in CANDIDATE_UPLOAD_DIRS:
        target = (project_root / rel).resolve()
        if not target.exists() or not target.is_dir():
            continue

        for p in target.rglob("*"):
            try:
                if p.is_file():
                    p.unlink()
                    deleted_files += 1
                elif p.is_dir():
                    continue
            except Exception as e:
                print(f"FAILED_DELETE_FILE: {p} ({e})")

        for p in sorted([x for x in target.rglob("*") if x.is_dir()], reverse=True):
            try:
                if not any(p.iterdir()):
                    p.rmdir()
                    deleted_dirs += 1
            except Exception:
                pass

        print(f"CLEANED_UPLOAD_DIR: {target}")

    return deleted_files, deleted_dirs


def main():
    project_root = Path(__file__).resolve().parent

    print(f"Database: {DatabaseConfig.MYSQL_DATABASE}")
    print("This will DELETE DATA (rows) from ALL tables EXCEPT:")
    for t in sorted(KEEP_ONLY_TABLES):
        print(f"- {t}")
    print("Users table will be pruned to keep ONLY these user_id values:")
    for uid in sorted(KEEP_USERS_USER_IDS):
        print(f"- {uid}")
    print("It will NOT drop tables or the database.")

    conn = DatabaseConfig.get_connection()
    if not conn:
        print("ERROR: Database connection failed")
        return 1

    try:
        all_tables = _fetch_all_tables(conn)

        wipe_tables = []
        skipped_tables = []
        for t in all_tables:
            if _is_keep_table(t):
                skipped_tables.append(t)
                continue
            if _is_wipe_table(t):
                wipe_tables.append(t)
            else:
                skipped_tables.append(t)

        print("\nCURRENT ROW COUNTS:")
        for t in all_tables:
            try:
                print(f"{t}: {_get_row_count(conn, t)}")
            except Exception as e:
                print(f"{t}: ERROR ({e})")

        print("\nTables to TRUNCATE:")
        for t in wipe_tables:
            print(f"- {t}")

        print("\nTables to KEEP/SKIP:")
        for t in skipped_tables:
            print(f"- {t}")

        if not wipe_tables:
            print("\nNothing to wipe based on current rules.")
            return 0

        phrase = input(f"\nType '{CONFIRM_PHRASE}' to proceed: ").strip()
        if phrase != CONFIRM_PHRASE:
            print("Cancelled.")
            return 0

        _truncate_tables(conn, wipe_tables)
        _prune_users_table(conn)

        deleted_files, deleted_dirs = _delete_upload_files(project_root)
        print(f"UPLOAD_FILES_DELETED: {deleted_files}")
        print(f"UPLOAD_EMPTY_DIRS_DELETED: {deleted_dirs}")

        print("\nROW COUNTS AFTER WIPE:")
        for t in all_tables:
            try:
                print(f"{t}: {_get_row_count(conn, t)}")
            except Exception as e:
                print(f"{t}: ERROR ({e})")

        print("DONE.")
        return 0
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
