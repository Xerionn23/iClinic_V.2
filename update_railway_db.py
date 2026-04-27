#!/usr/bin/env python3
"""
Railway Database FULL Update Script
Run this to update your Railway MySQL database with ALL latest schema changes.

This script replicates all migrations from app.py:
- patients_unified (address, priority flags, etc.)
- students, visitors, teaching, non_teaching_staff, deans
- medical_records, consultation_tickets
- medicines, inventory
- And more...

Usage:
    python update_railway_db.py

Environment variables (set these before running):
    DATABASE_URL or MYSQL_URL - Full connection string (priority)
    OR individual:
    MYSQL_HOST or MYSQLHOST - Railway MySQL host
    MYSQL_PORT or MYSQLPORT - Railway MySQL port (default: 3306)
    MYSQL_USER or MYSQLUSER - Railway MySQL user
    MYSQL_PASSWORD or MYSQLPASSWORD - Railway MySQL password
    MYSQL_DATABASE or MYSQLDATABASE - Railway MySQL database name
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
from urllib.parse import urlparse


def _parse_database_url():
    """Parse DATABASE_URL like app.py does"""
    database_url = os.getenv('DATABASE_URL') or os.getenv('MYSQL_URL')
    if not database_url:
        return None

    parsed = urlparse(database_url)
    if parsed.scheme not in ('mysql', 'mysql+pymysql'):
        return None

    return {
        'host': parsed.hostname,
        'port': parsed.port or 3306,
        'user': parsed.username,
        'password': parsed.password,
        'database': (parsed.path or '').lstrip('/') or None,
    }


def get_connection(include_database=True):
    """Get MySQL connection - matches app.py exactly"""
    # Check DATABASE_URL first (like app.py)
    url_cfg = _parse_database_url()

    if url_cfg:
        host = url_cfg['host']
        port = url_cfg['port']
        user = url_cfg['user']
        password = url_cfg['password']
        database = url_cfg.get('database') or os.getenv('MYSQL_DATABASE') or os.getenv('MYSQLDATABASE') or 'iclinic_db'
    else:
        # Fall back to individual env vars
        host = os.getenv('MYSQL_HOST') or os.getenv('MYSQLHOST') or 'localhost'
        port = int(os.getenv('MYSQL_PORT') or os.getenv('MYSQLPORT') or '3306')
        user = os.getenv('MYSQL_USER') or os.getenv('MYSQLUSER') or 'root'
        password = os.getenv('MYSQL_PASSWORD') or os.getenv('MYSQLPASSWORD') or ''
        database = os.getenv('MYSQL_DATABASE') or os.getenv('MYSQLDATABASE') or 'iclinic_db'

    print(f"\n[DEBUG] Connection details:")
    print(f"   HOST:     {host}")
    print(f"   PORT:     {port}")
    print(f"   USER:     {user}")
    print(f"   DATABASE: {database}")
    print(f"   PASSWORD: {'*' * len(password) if password else '(empty)'}")
    print(f"   SOURCE:   {'DATABASE_URL' if url_cfg else 'individual env vars'}")
    print()

    try:
        params = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
        }
        if include_database:
            params['database'] = database

        print(f"Connecting to MySQL at {host}:{port}...")
        conn = mysql.connector.connect(**params, autocommit=True)
        print("[OK] Connected successfully!")
        return conn
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\nSet either:")
        print("  DATABASE_URL=mysql://user:pass@host:port/database")
        print("  OR individual:")
        print("  MYSQL_HOST / MYSQLHOST")
        print("  MYSQL_PORT / MYSQLPORT")
        print("  MYSQL_USER / MYSQLUSER")
        print("  MYSQL_PASSWORD / MYSQLPASSWORD")
        print("  MYSQL_DATABASE / MYSQLDATABASE")
        return None


def update_patients_unified(conn):
    """Update patients_unified table with all columns"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: patients_unified")
    print("="*60)

    # Check if table exists
    cursor.execute("SHOW TABLES LIKE 'patients_unified'")
    if not cursor.fetchone():
        print("⚠️  Table 'patients_unified' does not exist. Creating...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients_unified (
                patient_id INT AUTO_INCREMENT PRIMARY KEY,
                role VARCHAR(50),
                source_id INT,
                identifier VARCHAR(100),
                first_name VARCHAR(100),
                middle_name VARCHAR(100),
                last_name VARCHAR(100),
                suffix VARCHAR(20),
                gender VARCHAR(20),
                age INT,
                birthdate DATE,
                email VARCHAR(255),
                contact_number VARCHAR(20),
                address VARCHAR(255),
                department VARCHAR(100),
                course VARCHAR(100),
                level VARCHAR(20),
                position VARCHAR(100),
                is_pwd TINYINT(1) DEFAULT 0,
                is_senior_citizen TINYINT(1) DEFAULT 0,
                is_pregnant TINYINT(1) DEFAULT 0,
                blood_type VARCHAR(5),
                allergies TEXT,
                medical_conditions TEXT,
                emergency_contact_name VARCHAR(100),
                emergency_contact_relationship VARCHAR(50),
                emergency_contact_number VARCHAR(20),
                emergency_contact_email VARCHAR(255),
                is_active TINYINT(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("[OK] Table created!")
        return

    # Add columns one by one (safe, idempotent)
    columns_to_add = [
        ('address', 'VARCHAR(255) NULL AFTER contact_number'),
        ('is_pwd', 'TINYINT(1) NOT NULL DEFAULT 0 AFTER age'),
        ('is_senior_citizen', 'TINYINT(1) NOT NULL DEFAULT 0 AFTER is_pwd'),
        ('is_pregnant', 'TINYINT(1) NOT NULL DEFAULT 0 AFTER is_senior_citizen'),
        ('emergency_contact_email', 'VARCHAR(255) NULL AFTER emergency_contact_number'),
    ]

    for col_name, col_def in columns_to_add:
        try:
            cursor.execute(f"SHOW COLUMNS FROM patients_unified LIKE '{col_name}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE patients_unified ADD COLUMN {col_name} {col_def}")
                print(f"[OK] Added column: {col_name}")
        except Error as e:
            pass  # Column might already exist

    # Backfill dummy addresses
    dummy_addresses = [
        'Poblacion, San Nazario, Leyte',
        'Brgy. San Roque, San Nazario, Leyte',
        'Brgy. Tinago, San Nazario, Leyte',
        'Brgy. Dagsa, San Nazario, Leyte',
        'Brgy. Matlang, San Nazario, Leyte',
        'Brgy. Mabini, San Nazario, Leyte',
        'Brgy. Rizal, San Nazario, Leyte',
        'Brgy. Sta. Cruz, San Nazario, Leyte',
        'Brgy. San Isidro, San Nazario, Leyte',
        'Brgy. Victory, San Nazario, Leyte',
    ]

    cursor.execute("SELECT COUNT(*) FROM patients_unified WHERE address IS NULL OR TRIM(address) = '' OR address = 'N/A'")
    rows_to_update = cursor.fetchone()[0]

    if rows_to_update > 0:
        print(f"[NOTE] Backfilling {rows_to_update} rows with dummy addresses...")
        placeholders = ','.join(['%s'] * len(dummy_addresses))
        cursor.execute(
            f"""
            UPDATE patients_unified
            SET address = ELT(FLOOR(1 + RAND() * {len(dummy_addresses)}), {placeholders})
            WHERE address IS NULL OR TRIM(address) = '' OR address = 'N/A'
            """,
            tuple(dummy_addresses)
        )
        print(f"[OK] Updated {rows_to_update} addresses!")

    # Summary
    cursor.execute("SELECT COUNT(*) FROM patients_unified")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM patients_unified WHERE address IS NOT NULL AND TRIM(address) != ''")
    with_addr = cursor.fetchone()[0]
    print(f"[STATS] patients_unified: {total} rows, {with_addr} with address")


def update_visitors(conn):
    """Update visitors table"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: visitors")
    print("="*60)

    cursor.execute("SHOW TABLES LIKE 'visitors'")
    if not cursor.fetchone():
        print("⚠️  Table 'visitors' does not exist. Skipping...")
        return

    columns = [
        ('address', 'TEXT NULL'),
        ('blood_type', 'VARCHAR(10) NULL'),
        ('emergency_contact_name', 'VARCHAR(100) NULL'),
        ('emergency_contact_relationship', 'VARCHAR(50) NULL'),
        ('emergency_contact_number', 'VARCHAR(20) NULL'),
        ('emergency_contact_email', 'VARCHAR(255) NULL'),
    ]

    for col_name, col_def in columns:
        try:
            cursor.execute(f"SHOW COLUMNS FROM visitors LIKE '{col_name}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE visitors ADD COLUMN {col_name} {col_def}")
                print(f"[OK] Added column: {col_name}")
        except Error:
            pass

    cursor.execute("SELECT COUNT(*) FROM visitors")
    print(f"[STATS] visitors: {cursor.fetchone()[0]} rows")


def update_teaching(conn):
    """Update teaching staff table"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: teaching")
    print("="*60)

    cursor.execute("SHOW TABLES LIKE 'teaching'")
    if not cursor.fetchone():
        print("⚠️  Table 'teaching' does not exist. Skipping...")
        return

    columns = [
        ('address', 'TEXT NULL'),
        ('blood_type', 'VARCHAR(10) NULL'),
        ('emergency_contact_name', 'VARCHAR(100) NULL'),
        ('emergency_contact_relationship', 'VARCHAR(50) NULL'),
        ('emergency_contact_number', 'VARCHAR(20) NULL'),
        ('emergency_contact_email', 'VARCHAR(255) NULL'),
    ]

    for col_name, col_def in columns:
        try:
            cursor.execute(f"SHOW COLUMNS FROM teaching LIKE '{col_name}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE teaching ADD COLUMN {col_name} {col_def}")
                print(f"[OK] Added column: {col_name}")
        except Error:
            pass

    cursor.execute("SELECT COUNT(*) FROM teaching")
    print(f"[STATS] teaching: {cursor.fetchone()[0]} rows")


def update_non_teaching_staff(conn):
    """Update non_teaching_staff table"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: non_teaching_staff")
    print("="*60)

    cursor.execute("SHOW TABLES LIKE 'non_teaching_staff'")
    if not cursor.fetchone():
        print("⚠️  Table 'non_teaching_staff' does not exist. Skipping...")
        return

    columns = [
        ('address', 'TEXT NULL'),
        ('blood_type', 'VARCHAR(10) NULL'),
        ('emergency_contact_name', 'VARCHAR(100) NULL'),
        ('emergency_contact_relationship', 'VARCHAR(50) NULL'),
        ('emergency_contact_number', 'VARCHAR(20) NULL'),
        ('emergency_contact_email', 'VARCHAR(255) NULL'),
    ]

    for col_name, col_def in columns:
        try:
            cursor.execute(f"SHOW COLUMNS FROM non_teaching_staff LIKE '{col_name}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE non_teaching_staff ADD COLUMN {col_name} {col_def}")
                print(f"[OK] Added column: {col_name}")
        except Error:
            pass

    cursor.execute("SELECT COUNT(*) FROM non_teaching_staff")
    print(f"[STATS] non_teaching_staff: {cursor.fetchone()[0]} rows")


def update_deans(conn):
    """Update deans table"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: deans")
    print("="*60)

    cursor.execute("SHOW TABLES LIKE 'deans'")
    if not cursor.fetchone():
        print("⚠️  Table 'deans' does not exist. Skipping...")
        return

    columns = [
        ('address', 'TEXT NULL'),
        ('blood_type', 'VARCHAR(10) NULL'),
        ('emergency_contact_name', 'VARCHAR(100) NULL'),
        ('emergency_contact_relationship', 'VARCHAR(50) NULL'),
        ('emergency_contact_number', 'VARCHAR(20) NULL'),
        ('emergency_contact_email', 'VARCHAR(255) NULL'),
    ]

    for col_name, col_def in columns:
        try:
            cursor.execute(f"SHOW COLUMNS FROM deans LIKE '{col_name}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE deans ADD COLUMN {col_name} {col_def}")
                print(f"[OK] Added column: {col_name}")
        except Error:
            pass

    cursor.execute("SELECT COUNT(*) FROM deans")
    print(f"[STATS] deans: {cursor.fetchone()[0]} rows")


def update_medical_records(conn):
    """Update medical_records table"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: medical_records")
    print("="*60)

    cursor.execute("SHOW TABLES LIKE 'medical_records'")
    if not cursor.fetchone():
        print("⚠️  Table 'medical_records' does not exist. Skipping...")
        return

    # Add endorsement/classification columns
    columns = [
        ('illness_classification_suggested', 'VARCHAR(10) NULL'),
        ('illness_classification_suggested_reason', 'TEXT NULL'),
        ('illness_classification_final', 'VARCHAR(10) NULL'),
        ('illness_classification_override_reason', 'TEXT NULL'),
        ('endorsement_required', 'BOOLEAN DEFAULT FALSE'),
        ('endorsement_status', 'VARCHAR(20) DEFAULT "not_required"'),
        ('endorsed_at', 'DATETIME NULL'),
        ('referred_to', 'VARCHAR(255) NULL'),
        ('referred_to_hospital', 'VARCHAR(255) NULL'),
    ]

    for col_name, col_def in columns:
        try:
            cursor.execute(f"SHOW COLUMNS FROM medical_records LIKE '{col_name}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE medical_records ADD COLUMN {col_name} {col_def}")
                print(f"[OK] Added column: {col_name}")
        except Error:
            pass

    cursor.execute("SELECT COUNT(*) FROM medical_records")
    print(f"[STATS] medical_records: {cursor.fetchone()[0]} rows")


def update_consultation_tickets(conn):
    """Update consultation_tickets table"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: consultation_tickets")
    print("="*60)

    cursor.execute("SHOW TABLES LIKE 'consultation_tickets'")
    if not cursor.fetchone():
        print("⚠️  Table 'consultation_tickets' does not exist. Skipping...")
        return

    columns = [
        ('priority', 'VARCHAR(20) DEFAULT "normal"'),
        ('priority_reason', 'VARCHAR(255) NULL'),
        ('priority_source', 'VARCHAR(50) NULL'),
    ]

    for col_name, col_def in columns:
        try:
            cursor.execute(f"SHOW COLUMNS FROM consultation_tickets LIKE '{col_name}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE consultation_tickets ADD COLUMN {col_name} {col_def}")
                print(f"[OK] Added column: {col_name}")
        except Error:
            pass

    cursor.execute("SELECT COUNT(*) FROM consultation_tickets")
    print(f"[STATS] consultation_tickets: {cursor.fetchone()[0]} rows")


def update_medicines(conn):
    """Update medicines table"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: medicines")
    print("="*60)

    cursor.execute("SHOW TABLES LIKE 'medicines'")
    if not cursor.fetchone():
        print("⚠️  Table 'medicines' does not exist. Skipping...")
        return

    columns = [
        ('expiry_date', 'DATE NULL'),
        ('batch_number', 'VARCHAR(50) NULL'),
        ('supplier', 'VARCHAR(100) NULL'),
    ]

    for col_name, col_def in columns:
        try:
            cursor.execute(f"SHOW COLUMNS FROM medicines LIKE '{col_name}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE medicines ADD COLUMN {col_name} {col_def}")
                print(f"[OK] Added column: {col_name}")
        except Error:
            pass

    cursor.execute("SELECT COUNT(*) FROM medicines")
    print(f"[STATS] medicines: {cursor.fetchone()[0]} rows")


def show_all_tables(conn):
    """Show summary of all tables"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("DATABASE SUMMARY")
    print("="*60)

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    print(f"\nTotal tables: {len(tables)}")
    print("\nTable Row Counts:")
    print("-" * 40)

    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            count = cursor.fetchone()[0]
            print(f"  {table_name:<35} {count:>6} rows")
        except Error:
            print(f"  {table_name:<35} (skipped)")

    print("-" * 40)


def update_xray_reviews(conn):
    """Create/update xray_reviews table"""
    cursor = conn.cursor()
    print("\n" + "="*60)
    print("UPDATING: xray_reviews")
    print("="*60)

    cursor.execute("SHOW TABLES LIKE 'xray_reviews'")
    if not cursor.fetchone():
        print("[ADD] Creating xray_reviews table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS xray_reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id VARCHAR(50),
                patient_role VARCHAR(50),
                review_date DATE,
                result ENUM('normal', 'abnormal') NOT NULL DEFAULT 'normal',
                findings TEXT,
                recommendation TEXT,
                reviewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                reviewed_by INT NULL,
                reviewed_by_name VARCHAR(120),
                sms_notified_at DATETIME NULL,
                sms_status VARCHAR(20),
                sms_error TEXT,
                sms_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_xray_reviews_patient (patient_id, patient_role, reviewed_at),
                INDEX idx_xray_reviews_sms (sms_notified_at)
            )
        ''')
        print("[OK] Table created!")
    else:
        print("[INFO]  Table already exists. Adding missing columns...")
        # Add missing columns
        columns_to_add = [
            ('reviewed_at', 'DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP'),
            ('reviewed_by', 'INT NULL'),
            ('reviewed_by_name', 'VARCHAR(120) NULL'),
            ('sms_notified_at', 'DATETIME NULL'),
            ('sms_status', 'VARCHAR(20) NULL'),
            ('sms_error', 'TEXT NULL'),
            ('sms_message', 'TEXT NULL'),
        ]
        for col_name, col_def in columns_to_add:
            try:
                cursor.execute(f"SHOW COLUMNS FROM xray_reviews LIKE '{col_name}'")
                if not cursor.fetchone():
                    cursor.execute(f"ALTER TABLE xray_reviews ADD COLUMN {col_name} {col_def}")
                    print(f"[OK] Added column: {col_name}")
            except Error:
                pass

    cursor.execute("SELECT COUNT(*) FROM xray_reviews")
    print(f"[STATS] xray_reviews: {cursor.fetchone()[0]} rows")


def main():
    print("="*60)
    print("RAILWAY DATABASE FULL UPDATE SCRIPT")
    print("="*60)
    print("\nThis will update ALL tables with latest schema changes:")
    print("  - patients_unified (address, priority flags)")
    print("  - visitors, teaching, non_teaching_staff, deans")
    print("  - medical_records (endorsement, classification)")
    print("  - consultation_tickets (priority)")
    print("  - medicines")
    print("  - And more...")
    print()

    # Connect to database
    conn = get_connection(include_database=True)
    if not conn:
        sys.exit(1)

    try:
        # Run all updates
        update_patients_unified(conn)
        update_visitors(conn)
        update_teaching(conn)
        update_non_teaching_staff(conn)
        update_deans(conn)
        update_medical_records(conn)
        update_consultation_tickets(conn)
        update_medicines(conn)
        update_xray_reviews(conn)

        # Show summary
        show_all_tables(conn)

        print("\n" + "="*60)
        print("[OK] DATABASE FULL UPDATE COMPLETE!")
        print("="*60)

    except Error as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("\n[DISCONNECT] Connection closed.")


if __name__ == "__main__":
    main()
