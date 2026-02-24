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

# Professional announcement data
ANNOUNCEMENTS_DATA = [
    # Health & Wellness (Urgent Priority)
    {
        "title": "Annual Health and Wellness Week 2025",
        "content": "Join us for our Annual Health and Wellness Week from November 4-8, 2025. Activities include free health screenings, blood pressure monitoring, BMI assessment, fitness workshops, and nutrition counseling. All students are encouraged to participate. Registration starts October 28 at the clinic.",
        "category": "Health",
        "priority": "urgent",
        "author": "Dr. Maria Santos"
    },
    {
        "title": "Free Health Screening Program",
        "content": "The clinic is offering FREE comprehensive health screening for all students. Includes blood pressure check, blood sugar test, BMI calculation, and general physical examination. Schedule your appointment at the front desk. Limited slots available daily.",
        "category": "Health",
        "priority": "urgent",
        "author": "Nurse Jennifer Cruz"
    },
    {
        "title": "Mental Health Awareness Campaign",
        "content": "October is Mental Health Awareness Month. The clinic offers FREE confidential counseling sessions with licensed psychologists. Topics covered: stress management, anxiety, depression, academic pressure. Walk-in or by appointment. Your mental health matters!",
        "category": "Mental Health",
        "priority": "urgent",
        "author": "Dr. Robert Kim"
    },
    
    # Vaccination Programs (High Priority)
    {
        "title": "Flu Vaccination Drive 2025",
        "content": "Annual influenza vaccination program will run from November 1-15, 2025. Protect yourself from seasonal flu! Free for all enrolled students. Bring your student ID and health card. Available Monday-Friday, 9:00 AM - 4:00 PM at the clinic.",
        "category": "Vaccination",
        "priority": "urgent",
        "author": "Nurse Jennifer Cruz"
    },
    {
        "title": "COVID-19 Booster Shots Available",
        "content": "COVID-19 booster doses are now available at the clinic. Eligible students who received their last dose 6 months ago can get their booster shot. Walk-ins welcome. Bring vaccination card and valid ID. Moderna and Pfizer vaccines available.",
        "category": "Vaccination",
        "priority": "urgent",
        "author": "Dr. Maria Santos"
    },
    {
        "title": "Hepatitis B Vaccination Program",
        "content": "Free Hepatitis B vaccination for first-year students. Three-dose series required for complete protection. First dose available now. Schedule: November 5, 12, and 19. Register at the clinic. Parental consent required for minors.",
        "category": "Vaccination",
        "priority": "important",
        "author": "Nurse Anna Reyes"
    },
    {
        "title": "Measles-Mumps-Rubella (MMR) Catch-up Vaccination",
        "content": "MMR catch-up vaccination program for students with incomplete immunization records. Free for all students. Bring your immunization card for verification. Available every Wednesday and Friday, 10:00 AM - 3:00 PM.",
        "category": "Vaccination",
        "priority": "important",
        "author": "Dr. Lisa Wong"
    },
    
    # Clinic Operations (Medium Priority)
    {
        "title": "Extended Clinic Hours Starting November",
        "content": "Great news! Starting November 1, 2025, clinic hours will be extended until 7:00 PM on weekdays to better serve our students. Weekend hours remain 9:00 AM - 1:00 PM. Emergency services available 24/7 through campus security.",
        "category": "General",
        "priority": "important",
        "author": "Admin Office"
    },
    {
        "title": "New Online Appointment System",
        "content": "Book your clinic appointments online! Access the new appointment system through the student portal. Choose your preferred date and time. Receive SMS confirmation. Walk-ins still welcome but appointments get priority. Make healthcare convenient!",
        "category": "General",
        "priority": "important",
        "author": "IT Department"
    },
    {
        "title": "Clinic Closure for Maintenance",
        "content": "The clinic will be closed on November 15, 2025 (Saturday) for scheduled maintenance and equipment calibration. Emergency services will be available through campus security. Regular operations resume November 18. Thank you for your understanding.",
        "category": "General",
        "priority": "urgent",
        "author": "Admin Office"
    },
    {
        "title": "New Medical Equipment Available",
        "content": "The clinic has acquired new state-of-the-art medical equipment including digital X-ray machine, ECG monitor, and automated blood analyzer. These upgrades will improve diagnostic accuracy and reduce waiting time. Services available starting November 1.",
        "category": "General",
        "priority": "standard",
        "author": "Dr. Maria Santos"
    },
    
    # Dental Services
    {
        "title": "Free Dental Check-up Month",
        "content": "November is Dental Health Month! Free dental check-ups, cleaning, and fluoride treatment for all students. Prevent cavities and maintain oral health. Schedule: Every Monday, Wednesday, Friday, 1:00 PM - 5:00 PM. Book your slot now!",
        "category": "Dental",
        "priority": "urgent",
        "author": "Dr. Lisa Wong"
    },
    {
        "title": "Dental Emergency Services",
        "content": "Experiencing dental pain? The clinic now offers emergency dental services. Available for tooth extraction, filling, and pain management. Walk-ins accepted for emergencies. Regular dental services by appointment only.",
        "category": "Dental",
        "priority": "important",
        "author": "Dr. Lisa Wong"
    },
    {
        "title": "Orthodontic Consultation Available",
        "content": "Interested in braces or teeth alignment? Free orthodontic consultation every Thursday, 2:00 PM - 5:00 PM. Dr. Wong will assess your dental needs and provide treatment recommendations. Limited slots - book early!",
        "category": "Dental",
        "priority": "standard",
        "author": "Dr. Lisa Wong"
    },
    
    # Emergency & Safety
    {
        "title": "Update Emergency Contact Information",
        "content": "IMPORTANT: Please update your emergency contact information in your student profile. Accurate contact details help us reach your family quickly during medical emergencies. Update online through student portal or visit the clinic.",
        "category": "Emergency",
        "priority": "urgent",
        "author": "Registration Office"
    },
    {
        "title": "First Aid Training for Students",
        "content": "Learn life-saving skills! Free First Aid and CPR training for students. Topics: Basic life support, wound care, choking response, emergency procedures. Certificate provided. Schedule: November 10 & 17, 2:00 PM - 5:00 PM. Register at clinic.",
        "category": "Emergency",
        "priority": "important",
        "author": "Nurse Jennifer Cruz"
    },
    {
        "title": "Emergency Hotline Numbers",
        "content": "Save these numbers: Clinic Emergency: (02) 8888-1234, Campus Security: (02) 8888-5678, Ambulance Hotline: 911. Available 24/7. For medical emergencies after clinic hours, contact campus security who will coordinate with emergency services.",
        "category": "Emergency",
        "priority": "urgent",
        "author": "Admin Office"
    },
    {
        "title": "Fire and Earthquake Drill Reminder",
        "content": "Campus-wide emergency drill scheduled for November 8, 2025, 10:00 AM. Clinic staff will demonstrate emergency evacuation procedures. All students must participate. Assembly point: Main quadrangle. Bring your emergency kit if available.",
        "category": "Emergency",
        "priority": "important",
        "author": "Safety Office"
    },
    
    # Health Education & Awareness
    {
        "title": "Diabetes Awareness Seminar",
        "content": "World Diabetes Day Seminar on November 14, 2025. Learn about diabetes prevention, symptoms, management, and healthy lifestyle. Free blood sugar screening after seminar. Venue: Clinic Conference Room, 3:00 PM - 5:00 PM. Snacks provided!",
        "category": "Health",
        "priority": "important",
        "author": "Dr. Robert Kim"
    },
    {
        "title": "Nutrition and Healthy Eating Workshop",
        "content": "Join our Nutrition Workshop: Eating Right for Student Life. Topics: Balanced diet, meal planning on a budget, healthy snacks, weight management. Free nutrition consultation. November 12, 2025, 2:00 PM - 4:00 PM. Register at clinic.",
        "category": "Health",
        "priority": "important",
        "author": "Nutritionist Sarah Lee"
    },
    {
        "title": "Stress Management Workshop",
        "content": "Feeling overwhelmed? Join our Stress Management Workshop. Learn relaxation techniques, time management, study-life balance, and coping strategies. Interactive session with Q&A. November 20, 2025, 3:00 PM - 5:00 PM. Free for all students.",
        "category": "Mental Health",
        "priority": "important",
        "author": "Dr. Robert Kim"
    },
    {
        "title": "Sleep Hygiene and Wellness Talk",
        "content": "Can't sleep well? Attend our Sleep Hygiene seminar. Topics: Importance of sleep, sleep disorders, tips for better sleep, managing insomnia. Free sleep assessment. November 22, 2025, 4:00 PM - 5:30 PM. Clinic Conference Room.",
        "category": "Health",
        "priority": "standard",
        "author": "Dr. Maria Santos"
    },
    {
        "title": "Reproductive Health Education Program",
        "content": "Comprehensive reproductive health education for students. Topics: Sexual health, family planning, STI prevention, healthy relationships. Confidential and judgment-free. November 25, 2025, 3:00 PM - 5:00 PM. Separate sessions for male and female students.",
        "category": "Health",
        "priority": "important",
        "author": "Dr. Anna Reyes"
    },
    
    # Seasonal & Special Programs
    {
        "title": "Rainy Season Health Advisory",
        "content": "Rainy season is here! Protect yourself from common illnesses: flu, colds, leptospirosis, dengue. Tips: Stay dry, avoid floodwater, boost immunity, get vaccinated. Free flu shots available at clinic. Stay healthy this rainy season!",
        "category": "Health",
        "priority": "urgent",
        "author": "Dr. Maria Santos"
    },
    {
        "title": "Dengue Awareness and Prevention",
        "content": "Dengue cases rising! Know the symptoms: high fever, severe headache, pain behind eyes, joint pain, rash. Seek immediate medical attention if suspected. Prevention: Remove stagnant water, use mosquito repellent, wear long sleeves.",
        "category": "Health",
        "priority": "urgent",
        "author": "Nurse Jennifer Cruz"
    },
    {
        "title": "Heat Stroke Prevention Tips",
        "content": "Summer heat advisory! Prevent heat-related illnesses: Stay hydrated, avoid prolonged sun exposure, wear light clothing, take breaks in shade. Symptoms of heat stroke: dizziness, nausea, confusion. Seek help immediately if experiencing symptoms.",
        "category": "Health",
        "priority": "important",
        "author": "Dr. Robert Kim"
    },
    
    # Sports & Fitness
    {
        "title": "Sports Physical Examination",
        "content": "Mandatory sports physical exam for all student-athletes. Includes cardiovascular screening, musculoskeletal assessment, and medical clearance. Schedule: November 5-9, 2025, 9:00 AM - 12:00 PM. Bring athletic clearance form. No exam, no play!",
        "category": "Health",
        "priority": "urgent",
        "author": "Dr. Maria Santos"
    },
    {
        "title": "Injury Prevention for Athletes",
        "content": "Sports injury prevention workshop for student-athletes. Topics: Proper warm-up, stretching techniques, injury recognition, RICE protocol. Conducted by sports medicine specialist. November 16, 2025, 4:00 PM - 6:00 PM. Gym venue.",
        "category": "Health",
        "priority": "important",
        "author": "Dr. Lisa Wong"
    },
    {
        "title": "Fitness Assessment Program",
        "content": "Free fitness assessment for all students! Includes body composition analysis, cardiovascular endurance test, flexibility assessment, and personalized fitness recommendations. Schedule your assessment at the clinic. Limited slots daily.",
        "category": "Health",
        "priority": "standard",
        "author": "Fitness Coordinator"
    },
    
    # Medical Records & Documentation
    {
        "title": "Medical Certificate Processing",
        "content": "Need a medical certificate? Processing time: Same day for consultations, 24 hours for laboratory results. Requirements: Valid ID, consultation receipt. Fee: ₱50. Available Monday-Friday, 9:00 AM - 5:00 PM. Rush processing available for emergencies.",
        "category": "General",
        "priority": "standard",
        "author": "Admin Office"
    },
    {
        "title": "Health Records Digitization",
        "content": "The clinic is digitizing all health records for better accessibility and security. Students can now access their medical history online through the student portal. Update your health profile regularly. Contact clinic for assistance.",
        "category": "General",
        "priority": "important",
        "author": "IT Department"
    },
    {
        "title": "Annual Health Card Renewal",
        "content": "Time to renew your health cards! Annual health card renewal for all students. Bring: 1 ID photo, student ID, previous health card. Fee: ₱100. Includes basic health screening. Process at clinic, November 1-30, 2025.",
        "category": "General",
        "priority": "important",
        "author": "Registration Office"
    },
    
    # Special Services
    {
        "title": "Free Eye Screening Program",
        "content": "Vision problems affecting your studies? Free eye screening program! Includes visual acuity test, color blindness test, and eye health assessment. Referral to ophthalmologist if needed. November 18-22, 2025, 10:00 AM - 3:00 PM.",
        "category": "Health",
        "priority": "important",
        "author": "Dr. Anna Reyes"
    },
    {
        "title": "Hearing Test and Ear Care",
        "content": "Free hearing screening available! Protect your hearing health. Includes audiometry test and ear examination. Learn about hearing protection and ear care. November 24, 2025, 1:00 PM - 4:00 PM. Walk-ins welcome.",
        "category": "Health",
        "priority": "standard",
        "author": "Dr. Robert Kim"
    },
    {
        "title": "Smoking Cessation Program",
        "content": "Want to quit smoking? Join our Smoking Cessation Program. Free counseling, nicotine replacement therapy, and support group sessions. Confidential service. Schedule: Every Tuesday, 3:00 PM - 5:00 PM. Take the first step to a healthier you!",
        "category": "Health",
        "priority": "important",
        "author": "Dr. Maria Santos"
    },
    {
        "title": "Weight Management Program",
        "content": "Achieve your healthy weight goals! Comprehensive weight management program includes nutrition counseling, exercise planning, and regular monitoring. Individual and group sessions available. Register at clinic. Program starts November 10, 2025.",
        "category": "Health",
        "priority": "standard",
        "author": "Nutritionist Sarah Lee"
    },
    
    # Policy Updates
    {
        "title": "Updated Health and Safety Protocols",
        "content": "New health and safety protocols effective November 1, 2025. Key changes: Mask optional in open areas, mandatory in clinic. Hand sanitizers at all entrances. Social distancing in waiting area. Review full guidelines on bulletin board.",
        "category": "General",
        "priority": "urgent",
        "author": "Admin Office"
    },
    {
        "title": "Medicine Dispensing Policy",
        "content": "Updated medicine dispensing policy: Prescription required for antibiotics and controlled medications. Over-the-counter medicines available for minor ailments. Bring valid ID and student card. Free for enrolled students. Policy effective immediately.",
        "category": "General",
        "priority": "important",
        "author": "Pharmacist John Doe"
    },
    {
        "title": "Clinic Visitor Policy",
        "content": "For patient safety and privacy: Maximum 1 companion per patient. Visitors must register at front desk. Visiting hours: 9:00 AM - 5:00 PM. No visitors for contagious disease patients. Thank you for cooperation.",
        "category": "General",
        "priority": "standard",
        "author": "Admin Office"
    },
    
    # Gratitude & Recognition
    {
        "title": "Thank You for Your Cooperation",
        "content": "The clinic staff extends heartfelt thanks to all students for following health protocols and maintaining cleanliness. Your cooperation helps us provide better healthcare services. Together, we keep our campus healthy and safe!",
        "category": "General",
        "priority": "standard",
        "author": "Dr. Maria Santos"
    },
]

def backup_announcements():
    """Create backup of existing announcements"""
    print("\n" + "="*80)
    print("📦 CREATING BACKUP OF ANNOUNCEMENTS")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM announcements")
        announcements = cursor.fetchall()
        
        # Convert datetime objects to strings
        for ann in announcements:
            for key, value in ann.items():
                if isinstance(value, (datetime, timedelta)):
                    ann[key] = str(value)
        
        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"announcements_backup_{timestamp}.json"
        
        with open(backup_filename, 'w') as f:
            json.dump(announcements, f, indent=2, default=str)
        
        print(f"✅ Backup created: {backup_filename}")
        print(f"📊 Announcements backed up: {len(announcements)}")
        
        cursor.close()
        conn.close()
        
        return backup_filename
        
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

def delete_announcements():
    """Delete all existing announcements"""
    print("\n" + "="*80)
    print("🗑️  DELETING EXISTING ANNOUNCEMENTS")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM announcements")
        count = cursor.fetchone()[0]
        
        cursor.execute("DELETE FROM announcements")
        conn.commit()
        
        print(f"✅ Deleted {count} announcements")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error deleting announcements: {e}")

def insert_announcements():
    """Insert professional announcements"""
    print("\n" + "="*80)
    print("📢 INSERTING PROFESSIONAL ANNOUNCEMENTS")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        total_inserted = 0
        
        # Shuffle announcements for variety
        announcements = ANNOUNCEMENTS_DATA.copy()
        random.shuffle(announcements)
        
        # Insert 37 announcements (between 35-39)
        for i, ann_data in enumerate(announcements[:37], 1):
            # Random creation date (past 60 days)
            days_ago = random.randint(1, 60)
            created_date = today - timedelta(days=days_ago)
            
            # Expiration date based on priority
            if ann_data['priority'] == 'urgent':
                # Urgent priority: expires in 30-60 days
                expiry_days = random.randint(30, 60)
            elif ann_data['priority'] == 'important':
                # Important priority: expires in 15-45 days
                expiry_days = random.randint(15, 45)
            else:
                # Standard priority: expires in 7-30 days
                expiry_days = random.randint(7, 30)
            
            expiration_date = today + timedelta(days=expiry_days)
            
            # Random expiration time
            expiration_time = f"{random.randint(0, 23):02d}:{random.choice([0, 30]):02d}:00"
            
            # Determine if active (90% active, 10% inactive for variety)
            is_active = random.choices([True, False], weights=[0.9, 0.1])[0]
            
            insert_query = """
                INSERT INTO announcements (
                    title, content, category, priority, author,
                    expiration_date, expiration_time, created_at, is_active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                ann_data['title'],
                ann_data['content'],
                ann_data['category'],
                ann_data['priority'],
                ann_data['author'],
                expiration_date,
                expiration_time,
                created_date,
                is_active
            )
            
            cursor.execute(insert_query, values)
            total_inserted += 1
            
            if i % 10 == 0:
                print(f"  ✅ Inserted {i} announcements...")
        
        conn.commit()
        
        print(f"\n✅ TOTAL ANNOUNCEMENTS INSERTED: {total_inserted}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error inserting announcements: {e}")
        import traceback
        traceback.print_exc()

def verify_announcements():
    """Verify inserted announcements"""
    print("\n" + "="*80)
    print("🔍 VERIFYING ANNOUNCEMENTS")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Total count
        cursor.execute("SELECT COUNT(*) FROM announcements")
        total = cursor.fetchone()[0]
        print(f"\n📢 Total Announcements: {total}")
        
        # By category
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM announcements
            GROUP BY category
            ORDER BY count DESC
        """)
        print(f"\n📋 Announcements by Category:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        # By priority
        cursor.execute("""
            SELECT priority, COUNT(*) as count
            FROM announcements
            GROUP BY priority
        """)
        print(f"\n⚡ Announcements by Priority:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        # Active vs Inactive
        cursor.execute("""
            SELECT is_active, COUNT(*) as count
            FROM announcements
            GROUP BY is_active
        """)
        print(f"\n📊 Status:")
        for row in cursor.fetchall():
            status = "Active" if row[0] else "Inactive"
            print(f"  - {status}: {row[1]}")
        
        # Expiring soon
        today = datetime.now().date()
        cursor.execute("""
            SELECT COUNT(*) FROM announcements
            WHERE expiration_date BETWEEN %s AND %s
        """, (today, today + timedelta(days=7)))
        expiring_soon = cursor.fetchone()[0]
        print(f"\n⚠️  Expiring in 7 days: {expiring_soon} announcements")
        
        # By author
        cursor.execute("""
            SELECT author, COUNT(*) as count
            FROM announcements
            GROUP BY author
            ORDER BY count DESC
            LIMIT 5
        """)
        print(f"\n👤 Top Authors:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verifying announcements: {e}")

def main():
    print("\n" + "="*80)
    print("📢 ANNOUNCEMENTS BACKUP & REPOPULATION SCRIPT")
    print("="*80)
    print("This script will:")
    print("1. Create backup of existing announcements")
    print("2. Delete all existing announcements")
    print("3. Insert 37 professional announcements")
    print("4. Include various categories and priorities")
    print("="*80)
    
    confirm = input("\n⚠️  Do you want to proceed? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Operation cancelled.")
        return
    
    # Step 1: Backup
    backup_file = backup_announcements()
    if not backup_file:
        print("❌ Backup failed. Aborting.")
        return
    
    # Step 2: Delete
    delete_announcements()
    
    # Step 3: Insert
    insert_announcements()
    
    # Step 4: Verify
    verify_announcements()
    
    print("\n" + "="*80)
    print("✅ ANNOUNCEMENTS REPOPULATION COMPLETE!")
    print(f"📦 Backup saved as: {backup_file}")
    print("="*80)

if __name__ == "__main__":
    main()
