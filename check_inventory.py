import mysql.connector
from datetime import datetime

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'iclinic_db'
}

def check_inventory():
    """Check current inventory data"""
    print("\n" + "="*80)
    print("🔍 CHECKING INVENTORY DATABASE")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check medicines table structure
        print("\n📋 MEDICINES TABLE STRUCTURE:")
        cursor.execute("SHOW COLUMNS FROM medicines")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Check medicines data
        print("\n💊 MEDICINES TABLE DATA:")
        cursor.execute("SELECT * FROM medicines")
        medicines = cursor.fetchall()
        print(f"Total medicines: {len(medicines)}")
        
        if medicines:
            print("\nSample medicines:")
            for med in medicines[:5]:
                print(f"  ID: {med[0]}, Name: {med[1]}, Stock: {med[6]}, Expiry: {med[9]}, Status: {med[10]}")
        
        # Check medicine_batches table structure
        print("\n📦 MEDICINE_BATCHES TABLE STRUCTURE:")
        cursor.execute("SHOW COLUMNS FROM medicine_batches")
        batch_columns = cursor.fetchall()
        for col in batch_columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Check medicine_batches data
        print("\n📦 MEDICINE_BATCHES TABLE DATA:")
        cursor.execute("SELECT * FROM medicine_batches")
        batches = cursor.fetchall()
        print(f"Total batches: {len(batches)}")
        
        if batches:
            print("\nSample batches:")
            for batch in batches[:5]:
                print(f"  ID: {batch[0]}, Medicine ID: {batch[1]}, Batch: {batch[2]}, Qty: {batch[3]}, Expiry: {batch[4]}")
        
        # Check for issues
        print("\n⚠️  POTENTIAL ISSUES:")
        
        # Issue 1: Medicines with no batches
        cursor.execute("""
            SELECT m.medicine_id, m.medicine_name, m.quantity_in_stock
            FROM medicines m
            LEFT JOIN medicine_batches mb ON m.medicine_id = mb.medicine_id
            WHERE mb.id IS NULL
        """)
        no_batches = cursor.fetchall()
        if no_batches:
            print(f"\n❌ {len(no_batches)} medicines have NO batches:")
            for med in no_batches[:5]:
                print(f"  - {med[1]} (ID: {med[0]}, Stock: {med[2]})")
        
        # Issue 2: Stock quantity mismatch
        cursor.execute("""
            SELECT m.medicine_id, m.medicine_name, m.quantity_in_stock,
                   COALESCE(SUM(mb.quantity), 0) as total_batch_qty
            FROM medicines m
            LEFT JOIN medicine_batches mb ON m.medicine_id = mb.medicine_id
            GROUP BY m.medicine_id, m.medicine_name, m.quantity_in_stock
            HAVING m.quantity_in_stock != total_batch_qty
        """)
        mismatches = cursor.fetchall()
        if mismatches:
            print(f"\n❌ {len(mismatches)} medicines have STOCK MISMATCH:")
            for med in mismatches[:5]:
                print(f"  - {med[1]}: Medicine stock={med[2]}, Batch total={med[3]}")
        
        # Issue 3: Expired medicines
        cursor.execute("""
            SELECT medicine_id, medicine_name, expiry_date, quantity_in_stock
            FROM medicines
            WHERE expiry_date < CURDATE() AND quantity_in_stock > 0
        """)
        expired = cursor.fetchall()
        if expired:
            print(f"\n⚠️  {len(expired)} medicines are EXPIRED:")
            for med in expired[:5]:
                print(f"  - {med[1]}: Expired {med[2]}, Stock: {med[3]}")
        
        # Issue 4: Expired batches
        cursor.execute("""
            SELECT mb.id, m.medicine_name, mb.batch_number, mb.expiry_date, mb.quantity
            FROM medicine_batches mb
            JOIN medicines m ON mb.medicine_id = m.medicine_id
            WHERE mb.expiry_date < CURDATE() AND mb.quantity > 0
        """)
        expired_batches = cursor.fetchall()
        if expired_batches:
            print(f"\n⚠️  {len(expired_batches)} batches are EXPIRED:")
            for batch in expired_batches[:5]:
                print(f"  - {batch[1]} (Batch: {batch[2]}): Expired {batch[3]}, Qty: {batch[4]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*80)
        print("✅ INVENTORY CHECK COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error checking inventory: {e}")

if __name__ == "__main__":
    check_inventory()
