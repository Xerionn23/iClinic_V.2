import mysql.connector
from datetime import datetime, timedelta
import random
import json

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'iclinic_db'
}

# Professional medicine data
MEDICINES_DATA = [
    # Analgesics & Antipyretics
    {"name": "Paracetamol", "generic": "Acetaminophen", "brand": "Biogesic", "category": "Analgesic", "form": "Tablet", "strength": "500mg"},
    {"name": "Ibuprofen", "generic": "Ibuprofen", "brand": "Advil", "category": "NSAID", "form": "Tablet", "strength": "400mg"},
    {"name": "Mefenamic Acid", "generic": "Mefenamic Acid", "brand": "Ponstan", "category": "NSAID", "form": "Capsule", "strength": "500mg"},
    {"name": "Aspirin", "generic": "Acetylsalicylic Acid", "brand": "Aspirin", "category": "Analgesic", "form": "Tablet", "strength": "80mg"},
    
    # Antibiotics
    {"name": "Amoxicillin", "generic": "Amoxicillin", "brand": "Amoxil", "category": "Antibiotic", "form": "Capsule", "strength": "500mg"},
    {"name": "Cefalexin", "generic": "Cefalexin", "brand": "Keflex", "category": "Antibiotic", "form": "Capsule", "strength": "500mg"},
    {"name": "Azithromycin", "generic": "Azithromycin", "brand": "Zithromax", "category": "Antibiotic", "form": "Tablet", "strength": "500mg"},
    {"name": "Ciprofloxacin", "generic": "Ciprofloxacin", "brand": "Cipro", "category": "Antibiotic", "form": "Tablet", "strength": "500mg"},
    {"name": "Metronidazole", "generic": "Metronidazole", "brand": "Flagyl", "category": "Antibiotic", "form": "Tablet", "strength": "500mg"},
    
    # Antihistamines
    {"name": "Cetirizine", "generic": "Cetirizine", "brand": "Zyrtec", "category": "Antihistamine", "form": "Tablet", "strength": "10mg"},
    {"name": "Loratadine", "generic": "Loratadine", "brand": "Claritin", "category": "Antihistamine", "form": "Tablet", "strength": "10mg"},
    {"name": "Diphenhydramine", "generic": "Diphenhydramine", "brand": "Benadryl", "category": "Antihistamine", "form": "Capsule", "strength": "25mg"},
    
    # Gastrointestinal
    {"name": "Omeprazole", "generic": "Omeprazole", "brand": "Losec", "category": "Antacid", "form": "Capsule", "strength": "20mg"},
    {"name": "Loperamide", "generic": "Loperamide", "brand": "Imodium", "category": "Antidiarrheal", "form": "Capsule", "strength": "2mg"},
    {"name": "Aluminum Hydroxide", "generic": "Aluminum Hydroxide", "brand": "Kremil-S", "category": "Antacid", "form": "Tablet", "strength": "178mg"},
    {"name": "Bisacodyl", "generic": "Bisacodyl", "brand": "Dulcolax", "category": "Laxative", "form": "Tablet", "strength": "5mg"},
    
    # Respiratory
    {"name": "Salbutamol", "generic": "Salbutamol", "brand": "Ventolin", "category": "Bronchodilator", "form": "Inhaler", "strength": "100mcg"},
    {"name": "Carbocisteine", "generic": "Carbocisteine", "brand": "Solmux", "category": "Mucolytic", "form": "Capsule", "strength": "500mg"},
    {"name": "Dextromethorphan", "generic": "Dextromethorphan", "brand": "Robitussin", "category": "Cough Suppressant", "form": "Syrup", "strength": "15mg/5ml"},
    
    # Vitamins & Supplements
    {"name": "Vitamin C", "generic": "Ascorbic Acid", "brand": "Ceelin", "category": "Vitamin", "form": "Tablet", "strength": "500mg"},
    {"name": "Vitamin B Complex", "generic": "B-Complex", "brand": "Neurobion", "category": "Vitamin", "form": "Tablet", "strength": "Various"},
    {"name": "Multivitamins", "generic": "Multivitamins", "brand": "Centrum", "category": "Vitamin", "form": "Tablet", "strength": "Various"},
    {"name": "Calcium Carbonate", "generic": "Calcium Carbonate", "brand": "Caltrate", "category": "Supplement", "form": "Tablet", "strength": "600mg"},
    {"name": "Iron Supplement", "generic": "Ferrous Sulfate", "brand": "Sangobion", "category": "Supplement", "form": "Capsule", "strength": "325mg"},
    
    # Topical & External
    {"name": "Betamethasone Cream", "generic": "Betamethasone", "brand": "Celestone", "category": "Topical Steroid", "form": "Cream", "strength": "0.1%"},
    {"name": "Hydrocortisone Cream", "generic": "Hydrocortisone", "brand": "Cortaid", "category": "Topical Steroid", "form": "Cream", "strength": "1%"},
    {"name": "Povidone Iodine", "generic": "Povidone Iodine", "brand": "Betadine", "category": "Antiseptic", "form": "Solution", "strength": "10%"},
    {"name": "Hydrogen Peroxide", "generic": "Hydrogen Peroxide", "brand": "Generic", "category": "Antiseptic", "form": "Solution", "strength": "3%"},
    
    # Eye & Ear
    {"name": "Ciprofloxacin Eye Drops", "generic": "Ciprofloxacin", "brand": "Ciloxan", "category": "Ophthalmic", "form": "Eye Drops", "strength": "0.3%"},
    {"name": "Artificial Tears", "generic": "Hypromellose", "brand": "Refresh", "category": "Ophthalmic", "form": "Eye Drops", "strength": "0.3%"},
    {"name": "Ofloxacin Ear Drops", "generic": "Ofloxacin", "brand": "Floxin", "category": "Otic", "form": "Ear Drops", "strength": "0.3%"},
    
    # Cardiovascular
    {"name": "Amlodipine", "generic": "Amlodipine", "brand": "Norvasc", "category": "Antihypertensive", "form": "Tablet", "strength": "5mg"},
    {"name": "Losartan", "generic": "Losartan", "brand": "Cozaar", "category": "Antihypertensive", "form": "Tablet", "strength": "50mg"},
    {"name": "Atorvastatin", "generic": "Atorvastatin", "brand": "Lipitor", "category": "Statin", "form": "Tablet", "strength": "20mg"},
    
    # Diabetes
    {"name": "Metformin", "generic": "Metformin", "brand": "Glucophage", "category": "Antidiabetic", "form": "Tablet", "strength": "500mg"},
    {"name": "Glimepiride", "generic": "Glimepiride", "brand": "Amaryl", "category": "Antidiabetic", "form": "Tablet", "strength": "2mg"},
    
    # Emergency & First Aid
    {"name": "Epinephrine", "generic": "Epinephrine", "brand": "EpiPen", "category": "Emergency", "form": "Injection", "strength": "1mg/ml"},
    {"name": "Dextrose 5%", "generic": "Dextrose", "brand": "Generic", "category": "IV Solution", "form": "Solution", "strength": "5%"},
    {"name": "Normal Saline", "generic": "Sodium Chloride", "brand": "Generic", "category": "IV Solution", "form": "Solution", "strength": "0.9%"},
    
    # Others
    {"name": "Oral Rehydration Salts", "generic": "ORS", "brand": "Hydrite", "category": "Electrolyte", "form": "Powder", "strength": "27.9g"},
    {"name": "Activated Charcoal", "generic": "Activated Charcoal", "brand": "Charcoal", "category": "Antidote", "form": "Tablet", "strength": "250mg"},
    {"name": "Clotrimazole Cream", "generic": "Clotrimazole", "brand": "Canesten", "category": "Antifungal", "form": "Cream", "strength": "1%"},
    {"name": "Bacitracin Ointment", "generic": "Bacitracin", "brand": "Neosporin", "category": "Antibiotic Ointment", "form": "Ointment", "strength": "500units/g"},
    {"name": "Diclofenac Gel", "generic": "Diclofenac", "brand": "Voltaren", "category": "Topical NSAID", "form": "Gel", "strength": "1%"},
    {"name": "Ranitidine", "generic": "Ranitidine", "brand": "Zantac", "category": "H2 Blocker", "form": "Tablet", "strength": "150mg"},
]

SUPPLIERS = [
    "Zuellig Pharma Corporation",
    "Mercury Drug Corporation",
    "United Laboratories (Unilab)",
    "Pascual Laboratories Inc.",
    "Hizon Laboratories Inc.",
    "Cathay Drug Co. Inc.",
    "Metro Drug Inc.",
    "Philippine Pharmawealth Inc."
]

def backup_inventory():
    """Create backup of medicines and batches"""
    print("\n" + "="*80)
    print("📦 CREATING BACKUP OF INVENTORY")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Backup medicines
        cursor.execute("SELECT * FROM medicines")
        medicines = cursor.fetchall()
        
        # Backup batches
        cursor.execute("SELECT * FROM medicine_batches")
        batches = cursor.fetchall()
        
        # Convert datetime objects to strings
        for med in medicines:
            for key, value in med.items():
                if isinstance(value, (datetime, timedelta)):
                    med[key] = str(value)
        
        for batch in batches:
            for key, value in batch.items():
                if isinstance(value, (datetime, timedelta)):
                    batch[key] = str(value)
        
        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_data = {
            'medicines': medicines,
            'batches': batches,
            'backup_date': timestamp
        }
        
        backup_filename = f"inventory_backup_{timestamp}.json"
        with open(backup_filename, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        print(f"✅ Backup created: {backup_filename}")
        print(f"📊 Medicines backed up: {len(medicines)}")
        print(f"📦 Batches backed up: {len(batches)}")
        
        cursor.close()
        conn.close()
        
        return backup_filename
        
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

def delete_inventory():
    """Delete all inventory data"""
    print("\n" + "="*80)
    print("🗑️  DELETING EXISTING INVENTORY")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM medicine_batches")
        batch_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM medicines")
        medicine_count = cursor.fetchone()[0]
        
        # Delete batches first (foreign key constraint)
        cursor.execute("DELETE FROM medicine_batches")
        print(f"✅ Deleted {batch_count} medicine batches")
        
        # Delete medicines
        cursor.execute("DELETE FROM medicines")
        print(f"✅ Deleted {medicine_count} medicines")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error deleting inventory: {e}")

def insert_medicines_and_batches():
    """Insert professional medicine inventory with batches"""
    print("\n" + "="*80)
    print("💊 INSERTING PROFESSIONAL MEDICINE INVENTORY")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        total_medicines = 0
        total_batches = 0
        
        # Categories for batch distribution
        expired_count = 0
        near_expiry_30_count = 0
        near_expiry_60_count = 0
        good_stock_count = 0
        
        for med_data in MEDICINES_DATA:
            # Insert medicine
            insert_med_query = """
                INSERT INTO medicines (
                    medicine_name, generic_name, brand_name, category,
                    dosage_form, strength, quantity_in_stock, price,
                    status, date_added
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Random price based on category
            if med_data['category'] in ['Vitamin', 'Supplement']:
                price = round(random.uniform(5.00, 25.00), 2)
            elif med_data['category'] in ['Antibiotic', 'Antihypertensive']:
                price = round(random.uniform(10.00, 50.00), 2)
            elif med_data['form'] in ['Injection', 'IV Solution']:
                price = round(random.uniform(20.00, 100.00), 2)
            else:
                price = round(random.uniform(3.00, 30.00), 2)
            
            med_values = (
                med_data['name'],
                med_data['generic'],
                med_data['brand'],
                med_data['category'],
                med_data['form'],
                med_data['strength'],
                0,  # Will be calculated from batches
                price,
                'Available',
                today
            )
            
            cursor.execute(insert_med_query, med_values)
            medicine_id = cursor.lastrowid
            total_medicines += 1
            
            # Determine batch distribution for this medicine
            batch_type = random.choices(
                ['expired', 'near_30', 'near_60', 'good'],
                weights=[0.15, 0.20, 0.25, 0.40],  # 15% expired, 20% near 30 days, 25% near 60 days, 40% good
                k=1
            )[0]
            
            # Number of batches per medicine (1-4 batches)
            num_batches = random.randint(1, 4)
            total_quantity = 0
            
            for batch_num in range(num_batches):
                # Generate batch number
                batch_number = f"BATCH-{medicine_id:03d}-{batch_num+1:02d}-{random.randint(1000, 9999)}"
                
                # Quantity per batch
                if med_data['form'] in ['Injection', 'IV Solution', 'Inhaler']:
                    quantity = random.randint(10, 50)
                elif med_data['form'] in ['Syrup', 'Solution', 'Cream', 'Ointment', 'Gel']:
                    quantity = random.randint(20, 100)
                else:
                    quantity = random.randint(50, 500)
                
                # Arrival date (random in past 6 months)
                days_ago = random.randint(30, 180)
                arrival_date = today - timedelta(days=days_ago)
                
                # Expiry date based on batch type
                if batch_type == 'expired':
                    # Already expired (1-30 days ago)
                    expiry_date = today - timedelta(days=random.randint(1, 30))
                    status = 'expired'
                    expired_count += 1
                elif batch_type == 'near_30':
                    # Expires in 1-30 days
                    expiry_date = today + timedelta(days=random.randint(1, 30))
                    status = 'available'
                    near_expiry_30_count += 1
                elif batch_type == 'near_60':
                    # Expires in 31-60 days
                    expiry_date = today + timedelta(days=random.randint(31, 60))
                    status = 'available'
                    near_expiry_60_count += 1
                else:
                    # Good stock (expires in 6 months to 2 years)
                    expiry_date = today + timedelta(days=random.randint(180, 730))
                    status = 'available'
                    good_stock_count += 1
                
                # Supplier and cost
                supplier = random.choice(SUPPLIERS)
                cost_per_unit = round(price * random.uniform(0.6, 0.8), 2)
                
                # Insert batch
                insert_batch_query = """
                    INSERT INTO medicine_batches (
                        medicine_id, batch_number, quantity, expiry_date,
                        arrival_date, supplier, cost_per_unit, status,
                        notes, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                notes = f"Received from {supplier} on {arrival_date}"
                
                batch_values = (
                    medicine_id,
                    batch_number,
                    quantity,
                    expiry_date,
                    arrival_date,
                    supplier,
                    cost_per_unit,
                    status,
                    notes,
                    datetime.now()
                )
                
                cursor.execute(insert_batch_query, batch_values)
                total_batches += 1
                total_quantity += quantity
            
            # Update medicine quantity
            cursor.execute("""
                UPDATE medicines 
                SET quantity_in_stock = %s 
                WHERE medicine_id = %s
            """, (total_quantity, medicine_id))
            
            # Update status based on stock
            if total_quantity == 0:
                status = 'Out of Stock'
            elif any(batch_type == 'expired' for _ in range(num_batches)):
                status = 'Available'  # Has some expired but also available stock
            else:
                status = 'Available'
            
            cursor.execute("""
                UPDATE medicines 
                SET status = %s 
                WHERE medicine_id = %s
            """, (status, medicine_id))
        
        conn.commit()
        
        print(f"\n✅ INSERTED {total_medicines} MEDICINES")
        print(f"✅ INSERTED {total_batches} BATCHES")
        print(f"\n📊 BATCH DISTRIBUTION:")
        print(f"  ❌ Expired: {expired_count} batches")
        print(f"  ⚠️  Near expiry (1-30 days): {near_expiry_30_count} batches")
        print(f"  ⚠️  Near expiry (31-60 days): {near_expiry_60_count} batches")
        print(f"  ✅ Good stock (>60 days): {good_stock_count} batches")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error inserting inventory: {e}")
        import traceback
        traceback.print_exc()

def verify_inventory():
    """Verify inserted inventory"""
    print("\n" + "="*80)
    print("🔍 VERIFYING INVENTORY")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Total medicines
        cursor.execute("SELECT COUNT(*) FROM medicines")
        total_meds = cursor.fetchone()[0]
        print(f"\n💊 Total Medicines: {total_meds}")
        
        # Total batches
        cursor.execute("SELECT COUNT(*) FROM medicine_batches")
        total_batches = cursor.fetchone()[0]
        print(f"📦 Total Batches: {total_batches}")
        
        # By category
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM medicines
            GROUP BY category
            ORDER BY count DESC
        """)
        print(f"\n📋 Medicines by Category:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        # Stock status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM medicine_batches
            GROUP BY status
        """)
        print(f"\n📊 Batch Status:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        # Expiry analysis
        today = datetime.now().date()
        
        cursor.execute("""
            SELECT COUNT(*) FROM medicine_batches
            WHERE expiry_date < %s
        """, (today,))
        expired = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM medicine_batches
            WHERE expiry_date BETWEEN %s AND %s
        """, (today, today + timedelta(days=30)))
        near_30 = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM medicine_batches
            WHERE expiry_date BETWEEN %s AND %s
        """, (today + timedelta(days=31), today + timedelta(days=60)))
        near_60 = cursor.fetchone()[0]
        
        print(f"\n⚠️  Expiry Status:")
        print(f"  ❌ Expired: {expired} batches")
        print(f"  ⚠️  Expiring in 30 days: {near_30} batches")
        print(f"  ⚠️  Expiring in 31-60 days: {near_60} batches")
        
        # Total stock value
        cursor.execute("""
            SELECT SUM(m.quantity_in_stock * m.price)
            FROM medicines m
        """)
        total_value = cursor.fetchone()[0] or 0
        print(f"\n💰 Total Inventory Value: ₱{total_value:,.2f}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verifying inventory: {e}")

def main():
    print("\n" + "="*80)
    print("🏥 INVENTORY BACKUP & REPOPULATION SCRIPT")
    print("="*80)
    print("This script will:")
    print("1. Create backup of existing inventory")
    print("2. Delete all medicines and batches")
    print("3. Insert 45 professional medicines with multiple batches")
    print("4. Include expired, near-expiry (30 & 60 days), and good stock")
    print("="*80)
    
    confirm = input("\n⚠️  Do you want to proceed? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Operation cancelled.")
        return
    
    # Step 1: Backup
    backup_file = backup_inventory()
    if not backup_file:
        print("❌ Backup failed. Aborting.")
        return
    
    # Step 2: Delete
    delete_inventory()
    
    # Step 3: Insert
    insert_medicines_and_batches()
    
    # Step 4: Verify
    verify_inventory()
    
    print("\n" + "="*80)
    print("✅ INVENTORY REPOPULATION COMPLETE!")
    print(f"📦 Backup saved as: {backup_file}")
    print("="*80)

if __name__ == "__main__":
    main()
