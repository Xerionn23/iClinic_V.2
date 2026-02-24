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

# Professional medical data templates
CHIEF_COMPLAINTS = [
    "Headache and dizziness",
    "Fever and body aches",
    "Cough and cold symptoms",
    "Stomach pain and nausea",
    "Sore throat and difficulty swallowing",
    "Allergic reaction - skin rash",
    "Chest pain and shortness of breath",
    "Back pain and muscle strain",
    "Toothache and gum swelling",
    "Eye irritation and redness",
    "Ear pain and hearing difficulty",
    "Fatigue and weakness",
    "Abdominal cramps and diarrhea",
    "Migraine and light sensitivity",
    "Sprained ankle from sports injury",
    "Asthma attack symptoms",
    "Urinary tract infection symptoms",
    "Skin infection and wound care",
    "Anxiety and stress symptoms",
    "Menstrual cramps and discomfort"
]

DIAGNOSES = [
    "Acute Upper Respiratory Tract Infection",
    "Viral Fever",
    "Acute Gastroenteritis",
    "Tension Headache",
    "Allergic Rhinitis",
    "Acute Pharyngitis",
    "Contact Dermatitis",
    "Muscle Strain",
    "Dental Caries",
    "Conjunctivitis",
    "Otitis Media",
    "Acute Bronchitis",
    "Migraine",
    "Ankle Sprain",
    "Asthma Exacerbation",
    "Urinary Tract Infection",
    "Superficial Wound",
    "Anxiety Disorder",
    "Dysmenorrhea",
    "Hypertension - Follow up"
]

TREATMENTS = [
    "Rest, hydration, and prescribed medication",
    "Antipyretics and analgesics administered",
    "Oral rehydration therapy and dietary advice",
    "Pain management and stress reduction techniques",
    "Antihistamines and allergen avoidance counseling",
    "Throat gargles and anti-inflammatory medication",
    "Topical corticosteroid cream application",
    "Hot compress and muscle relaxants",
    "Dental referral and temporary pain relief",
    "Eye drops and hygiene instructions",
    "Antibiotic ear drops prescribed",
    "Bronchodilators and breathing exercises",
    "Migraine medication and rest in dark room",
    "RICE protocol (Rest, Ice, Compression, Elevation)",
    "Nebulization and bronchodilator therapy",
    "Antibiotics and increased fluid intake",
    "Wound cleaning, dressing, and tetanus prophylaxis",
    "Counseling and relaxation techniques",
    "NSAIDs and heat therapy",
    "Blood pressure monitoring and lifestyle modification"
]

PRESCRIBED_MEDICINES = [
    "Paracetamol 500mg, 1 tab every 6 hours",
    "Ibuprofen 400mg, 1 tab every 8 hours",
    "Cetirizine 10mg, 1 tab once daily",
    "Amoxicillin 500mg, 1 cap every 8 hours for 7 days",
    "Loperamide 2mg, 1 cap after each loose stool",
    "Salbutamol inhaler, 2 puffs as needed",
    "Mefenamic Acid 500mg, 1 tab every 8 hours",
    "Carbocisteine 500mg, 1 cap every 8 hours",
    "Omeprazole 20mg, 1 cap before breakfast",
    "Betamethasone cream, apply twice daily",
    "Ciprofloxacin eye drops, 1 drop every 4 hours",
    "Loratadine 10mg, 1 tab once daily",
    "Metronidazole 500mg, 1 tab every 8 hours",
    "Vitamin C 500mg, 1 tab once daily",
    "Multivitamins, 1 tab once daily"
]

def backup_medical_records():
    """Create a backup of existing medical records"""
    print("\n" + "="*60)
    print("📦 CREATING BACKUP OF MEDICAL RECORDS")
    print("="*60)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all medical records
        cursor.execute("SELECT * FROM medical_records")
        records = cursor.fetchall()
        
        # Convert datetime objects to strings for JSON serialization
        for record in records:
            for key, value in record.items():
                if isinstance(value, (datetime, timedelta)):
                    record[key] = str(value)
        
        # Save to JSON file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"medical_records_backup_{timestamp}.json"
        
        with open(backup_filename, 'w') as f:
            json.dump(records, f, indent=2, default=str)
        
        print(f"✅ Backup created successfully: {backup_filename}")
        print(f"📊 Total records backed up: {len(records)}")
        
        cursor.close()
        conn.close()
        
        return backup_filename
        
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

def get_students():
    """Fetch all students from database"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Check which column names the table uses
        cursor.execute("SHOW COLUMNS FROM students")
        columns = [col['Field'] for col in cursor.fetchall()]
        
        # Determine column names
        if 'first_name' in columns:
            fname_col = 'first_name'
            lname_col = 'last_name'
            gender_col = 'gender'
            age_col = 'age'
            course_col = 'course'
        else:
            fname_col = 'std_Firstname'
            lname_col = 'std_Surname'
            gender_col = 'std_Gender'
            age_col = 'std_Age'
            course_col = 'std_Course'
        
        query = f"""
            SELECT student_number, 
                   {fname_col} as first_name, 
                   {lname_col} as last_name, 
                   {gender_col} as gender, 
                   {age_col} as age, 
                   {course_col} as course
            FROM students
            WHERE is_active = TRUE
            ORDER BY student_number
        """
        
        cursor.execute(query)
        students = cursor.fetchall()
        
        print(f"ℹ️  Using columns: {fname_col}, {lname_col}, {gender_col}, {age_col}, {course_col}")
        
        cursor.close()
        conn.close()
        
        return students
        
    except Exception as e:
        print(f"❌ Error fetching students: {e}")
        return []

def delete_medical_records():
    """Delete all existing medical records"""
    print("\n" + "="*60)
    print("🗑️  DELETING EXISTING MEDICAL RECORDS")
    print("="*60)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Get count before deletion
        cursor.execute("SELECT COUNT(*) FROM medical_records")
        count_before = cursor.fetchone()[0]
        
        # Delete all records
        cursor.execute("DELETE FROM medical_records")
        conn.commit()
        
        print(f"✅ Deleted {count_before} medical records")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error deleting records: {e}")

def generate_vital_signs():
    """Generate realistic vital signs"""
    return {
        'bp_systolic': random.randint(110, 140),
        'bp_diastolic': random.randint(70, 90),
        'pulse_rate': random.randint(60, 100),
        'temperature': round(random.uniform(36.5, 37.5), 1),
        'respiratory_rate': random.randint(12, 20),
        'weight': round(random.uniform(45, 85), 2),
        'height': round(random.uniform(150, 180), 2)
    }

def calculate_bmi(weight, height):
    """Calculate BMI"""
    height_m = height / 100
    return round(weight / (height_m ** 2), 1)

def insert_medical_records(students):
    """Insert new professional medical records spread across Jan-Oct 2025"""
    print("\n" + "="*60)
    print("📝 INSERTING NEW MEDICAL RECORDS")
    print("="*60)
    
    # Records per month: [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct]
    records_per_month = [10, 21, 14, 15, 56, 23, 18, 32, 27, 19]
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if medical_records uses student_id or student_number
        cursor.execute("SHOW COLUMNS FROM medical_records LIKE 'student_number'")
        uses_student_number = cursor.fetchone() is not None
        
        if uses_student_number:
            print("ℹ️  Medical records table uses student_number")
            student_field = 'student_number'
        else:
            print("ℹ️  Medical records table uses student_id")
            student_field = 'student_id'
        
        # Get staff ID (assuming first staff member)
        cursor.execute("SELECT id FROM users WHERE role = 'staff' LIMIT 1")
        staff_result = cursor.fetchone()
        staff_id = staff_result[0] if staff_result else 1
        
        total_records = 0
        
        for month_index, num_records in enumerate(records_per_month, start=1):
            month = month_index
            print(f"\n📅 Month {month} (2025-{month:02d}): Generating {num_records} records...")
            
            for i in range(num_records):
                # Select random student
                student = random.choice(students)
                
                # Generate random date in the month
                day = random.randint(1, 28)  # Safe for all months
                visit_date = f"2025-{month:02d}-{day:02d}"
                
                # Generate random time during clinic hours (8 AM - 5 PM)
                hour = random.randint(8, 16)
                minute = random.choice([0, 15, 30, 45])
                visit_time = f"{hour:02d}:{minute:02d}:00"
                
                # Select random medical data
                complaint = random.choice(CHIEF_COMPLAINTS)
                diagnosis = random.choice(DIAGNOSES)
                treatment = random.choice(TREATMENTS)
                medicine = random.choice(PRESCRIBED_MEDICINES)
                
                # Generate vital signs
                vitals = generate_vital_signs()
                bmi = calculate_bmi(vitals['weight'], vitals['height'])
                
                # Create medical history
                medical_history = random.choice([
                    "No significant medical history",
                    "History of allergic rhinitis",
                    "Previous asthma diagnosis",
                    "Hypertension - controlled",
                    "No known allergies"
                ])
                
                # Insert record with appropriate student identifier
                insert_query = f"""
                    INSERT INTO medical_records (
                        {student_field}, visit_date, visit_time, chief_complaint,
                        medical_history, symptoms, treatment, prescribed_medicine,
                        blood_pressure_systolic, blood_pressure_diastolic,
                        pulse_rate, temperature, respiratory_rate,
                        weight, height, bmi, staff_id, notes,
                        created_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """
                
                values = (
                    student['student_number'],
                    visit_date,
                    visit_time,
                    complaint,
                    medical_history,
                    diagnosis,
                    treatment,
                    medicine,
                    vitals['bp_systolic'],
                    vitals['bp_diastolic'],
                    vitals['pulse_rate'],
                    vitals['temperature'],
                    vitals['respiratory_rate'],
                    vitals['weight'],
                    vitals['height'],
                    bmi,
                    staff_id,
                    f"Patient seen in clinic. {diagnosis} diagnosed and treated accordingly.",
                    f"{visit_date} {visit_time}"
                )
                
                cursor.execute(insert_query, values)
                total_records += 1
            
            conn.commit()
            print(f"✅ Inserted {num_records} records for month {month}")
        
        print(f"\n{'='*60}")
        print(f"✅ TOTAL RECORDS INSERTED: {total_records}")
        print(f"{'='*60}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error inserting records: {e}")
        conn.rollback()

def verify_records():
    """Verify the inserted records"""
    print("\n" + "="*60)
    print("🔍 VERIFYING INSERTED RECORDS")
    print("="*60)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Count records per month
        for month in range(1, 11):
            cursor.execute("""
                SELECT COUNT(*) FROM medical_records
                WHERE MONTH(visit_date) = %s AND YEAR(visit_date) = 2025
            """, (month,))
            count = cursor.fetchone()[0]
            month_name = datetime(2025, month, 1).strftime("%B")
            print(f"📊 {month_name} 2025: {count} records")
        
        # Total count
        cursor.execute("SELECT COUNT(*) FROM medical_records")
        total = cursor.fetchone()[0]
        print(f"\n{'='*60}")
        print(f"✅ TOTAL MEDICAL RECORDS: {total}")
        print(f"{'='*60}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verifying records: {e}")

def main():
    print("\n" + "="*60)
    print("🏥 MEDICAL RECORDS BACKUP & REPOPULATION SCRIPT")
    print("="*60)
    print("This script will:")
    print("1. Create a backup of existing medical records")
    print("2. Delete all existing medical records")
    print("3. Insert new professional medical records (Jan-Oct 2025)")
    print("="*60)
    
    # Ask for confirmation
    confirm = input("\n⚠️  Do you want to proceed? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Operation cancelled.")
        return
    
    # Step 1: Backup
    backup_file = backup_medical_records()
    if not backup_file:
        print("❌ Backup failed. Aborting operation.")
        return
    
    # Step 2: Get students
    print("\n" + "="*60)
    print("👥 FETCHING STUDENTS FROM DATABASE")
    print("="*60)
    students = get_students()
    print(f"✅ Found {len(students)} active students")
    
    if not students:
        print("❌ No students found. Aborting operation.")
        return
    
    # Step 3: Delete existing records
    delete_medical_records()
    
    # Step 4: Insert new records
    insert_medical_records(students)
    
    # Step 5: Verify
    verify_records()
    
    print("\n" + "="*60)
    print("✅ OPERATION COMPLETED SUCCESSFULLY!")
    print(f"📦 Backup saved as: {backup_file}")
    print("="*60)

if __name__ == "__main__":
    main()
