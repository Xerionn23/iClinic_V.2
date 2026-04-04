#!/usr/bin/env python3
"""
Realistic Medical Records Dummy Data Generator for iClinic V.2
===============================================================

Generates 1-3 realistic medical records per patient (not too many as requested).
Creates believable medical data that follows proper clinical workflow.

Features:
- Realistic chief complaints matched with appropriate diagnoses
- Logical vital signs based on patient demographics
- Consistent treatment plans matched to diagnoses
- Proper medicine prescriptions
- Visits distributed across Aug 2024 - Mar 2025 (recent realistic timeframe)
- Staff assignments from existing nurse accounts
"""

import mysql.connector
from datetime import datetime, timedelta, time
import random
from typing import List, Dict, Any, Tuple
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'iclinic_db',
    'autocommit': True
}

# ============ REALISTIC MEDICAL DATA TEMPLATES ============

# Chief Complaints mapped to likely diagnoses
CHIEF_COMPLAINTS = {
    "Headache and dizziness": ["Tension Headache", "Migraine", "Hypertension"],
    "Fever and body aches": ["Viral Fever", "Acute Upper Respiratory Tract Infection", "Influenza"],
    "Cough and cold symptoms": ["Acute Upper Respiratory Tract Infection", "Acute Bronchitis", "Allergic Rhinitis"],
    "Stomach pain and nausea": ["Acute Gastroenteritis", "Gastritis", "Dyspepsia"],
    "Sore throat and difficulty swallowing": ["Acute Pharyngitis", "Tonsillitis", "Viral Upper Respiratory Infection"],
    "Skin rash and itching": ["Contact Dermatitis", "Urticaria", "Allergic Reaction"],
    "Chest tightness and shortness of breath": ["Asthma Exacerbation", "Acute Bronchitis", "Anxiety Episode"],
    "Back pain after lifting": ["Muscle Strain (Lumbar)", "Mechanical Back Pain", "Sprain"],
    "Toothache with gum swelling": ["Dental Caries", "Gingivitis", "Periapical Abscess"],
    "Red, watery eyes": ["Conjunctivitis (Viral)", "Conjunctivitis (Bacterial)", "Allergic Conjunctivitis"],
    "Ear pain and decreased hearing": ["Acute Otitis Media", "Otitis Externa", "Ear Wax Impaction"],
    "Fatigue and general weakness": ["Viral Illness", "Iron Deficiency Anemia", "Stress-related Fatigue"],
    "Loose stools with abdominal cramps": ["Acute Gastroenteritis", "Food Poisoning", "Irritable Bowel Syndrome"],
    "Severe headache with light sensitivity": ["Migraine", "Tension Headache", "Viral Illness"],
    "Ankle swelling after sports": ["Ankle Sprain (Grade 1)", "Ankle Sprain (Grade 2)", "Soft Tissue Injury"],
    "Wheezing and breathing difficulty": ["Asthma Exacerbation", "Allergic Reaction", "Acute Bronchitis"],
    "Burning sensation during urination": ["Urinary Tract Infection", "Urethritis", "Cystitis"],
    "Cut wound on hand": ["Superficial Laceration", "Contaminated Wound", "Clean Laceration"],
    "Palpitations and nervousness": ["Anxiety Episode", "Stress Response", "Panic Attack"],
    "Menstrual cramps": ["Dysmenorrhea (Primary)", "Dysmenorrhea (Secondary)", "Menstrual Pain"]
}

# Diagnoses with matched treatments
DIAGNOSIS_TREATMENTS = {
    "Tension Headache": {
        "treatment": "Rest in quiet environment, apply cold compress, stress management counseling",
        "medicines": ["Paracetamol 500mg 1 tab every 6 hours PRN for pain", "Ibuprofen 400mg 1 tab every 8 hours PRN"],
        "classification": "minor",
        "follow_up": "Return if headache persists >3 days or worsens"
    },
    "Migraine": {
        "treatment": "Rest in dark quiet room, cold compress on forehead, avoid triggers",
        "medicines": ["Paracetamol 500mg 1 tab every 6 hours PRN", "Metoclopramide 10mg 1 tab for nausea PRN"],
        "classification": "minor",
        "follow_up": "Follow up if not improved in 24 hours"
    },
    "Hypertension": {
        "treatment": "BP monitoring, lifestyle modification counseling, reduce salt intake",
        "medicines": ["Amlodipine 5mg 1 tab daily", "Losartan 50mg 1 tab daily"],
        "classification": "major",
        "follow_up": "Follow up in 1 week for BP recheck, cardiology referral if needed"
    },
    "Viral Fever": {
        "treatment": "Increase fluid intake, rest, tepid sponging for fever >38.5°C",
        "medicines": ["Paracetamol 500mg 1 tab every 6 hours PRN for fever", "Vitamin C 500mg 1 tab daily"],
        "classification": "minor",
        "follow_up": "Return if fever persists >3 days or rash develops"
    },
    "Acute Upper Respiratory Tract Infection": {
        "treatment": "Increase fluid intake, warm salt water gargle, rest",
        "medicines": ["Paracetamol 500mg 1 tab every 6 hours PRN", "Salbutamol inhaler 2 puffs PRN for wheezing", "Carbocisteine 500mg 1 cap TID"],
        "classification": "minor",
        "follow_up": "Return if fever >3 days or breathing difficulty develops"
    },
    "Influenza": {
        "treatment": "Bed rest, increased fluid intake, isolation precautions",
        "medicines": ["Paracetamol 500mg 1 tab every 6 hours PRN", "Oseltamivir 75mg 1 cap BID for 5 days (if within 48hrs)"],
        "classification": "minor",
        "follow_up": "Return immediately if breathing difficulty or chest pain"
    },
    "Acute Bronchitis": {
        "treatment": "Hydration, rest, steam inhalation, avoid irritants",
        "medicines": ["Carbocisteine 500mg 1 cap TID", "Salbutamol inhaler 2 puffs PRN", "Paracetamol 500mg PRN for fever"],
        "classification": "minor",
        "follow_up": "Return if cough persists >2 weeks or fever returns"
    },
    "Allergic Rhinitis": {
        "treatment": "Allergen avoidance counseling, nasal saline rinse",
        "medicines": ["Cetirizine 10mg 1 tab daily", "Fluticasone nasal spray 1 spray each nostril BID"],
        "classification": "minor",
        "follow_up": "Follow up if symptoms not controlled in 1 week"
    },
    "Acute Gastroenteritis": {
        "treatment": "Oral rehydration solution, BRAT diet, strict hand hygiene",
        "medicines": ["Oral Rehydration Salts 1 sachet in 200ml water after each stool", "Loperamide 2mg 1 tab PRN (max 4/day)"],
        "classification": "minor",
        "follow_up": "Return if signs of dehydration or bloody stools"
    },
    "Gastritis": {
        "treatment": "Avoid spicy/acidic foods, eat small frequent meals, stress management",
        "medicines": ["Omeprazole 20mg 1 cap before breakfast", "Antacid 1-2 tabs PRN for pain"],
        "classification": "minor",
        "follow_up": "Return if vomiting blood or black stools"
    },
    "Dyspepsia": {
        "treatment": "Dietary modification, avoid late meals, elevate head of bed",
        "medicines": ["Omeprazole 20mg daily", "Simethicone 40mg 1 tab after meals"],
        "classification": "minor",
        "follow_up": "Follow up in 2 weeks, consider H. pylori testing if persistent"
    },
    "Acute Pharyngitis": {
        "treatment": "Warm salt water gargle, increase fluids, voice rest",
        "medicines": ["Paracetamol 500mg 1 tab every 6 hours PRN", "Chlorhexidine gargle 15ml BID"],
        "classification": "minor",
        "follow_up": "Return if throat culture positive for strep or fever persists >3 days"
    },
    "Tonsillitis": {
        "treatment": "Soft diet, warm salt gargle, hydration",
        "medicines": ["Amoxicillin 500mg 1 cap TID for 7 days", "Paracetamol 500mg PRN for pain/fever"],
        "classification": "minor",
        "follow_up": "Return if no improvement in 48 hours or airway obstruction"
    },
    "Viral Upper Respiratory Infection": {
        "treatment": "Symptomatic treatment, hydration, rest",
        "medicines": ["Paracetamol 500mg PRN", "Saline nasal spray PRN"],
        "classification": "minor",
        "follow_up": "Return if symptoms worsen or persist >10 days"
    },
    "Contact Dermatitis": {
        "treatment": "Identify and avoid trigger, gentle skin care, cool compress",
        "medicines": ["Cetirizine 10mg 1 tab daily", "Betamethasone 0.1% cream apply TID to affected area"],
        "classification": "minor",
        "follow_up": "Return if rash spreads or signs of infection"
    },
    "Urticaria": {
        "treatment": "Avoid suspected allergens, cool bath, loose clothing",
        "medicines": ["Cetirizine 10mg 1 tab daily", "Calamine lotion apply PRN"],
        "classification": "minor",
        "follow_up": "Return immediately if breathing difficulty or facial swelling"
    },
    "Allergic Reaction": {
        "treatment": "Remove allergen, monitor for anaphylaxis signs",
        "medicines": ["Diphenhydramine 25mg 1 tab every 8 hours", "Hydrocortisone 1% cream apply BID"],
        "classification": "minor",
        "follow_up": "Return immediately if any breathing difficulty"
    },
    "Asthma Exacerbation": {
        "treatment": "Nebulization, breathing exercises, trigger avoidance education",
        "medicines": ["Salbutamol neb 2.5mg every 20min x 3 doses", "Prednisone 20mg 1 tab daily for 5 days"],
        "classification": "major",
        "follow_up": "Follow up in 3 days, pulmonology referral if frequent attacks"
    },
    "Anxiety Episode": {
        "treatment": "Breathing exercises, counseling, stress management techniques",
        "medicines": ["None - non-pharmacological management", "Propranolol 10mg PRN for physical symptoms"],
        "classification": "minor",
        "follow_up": "Counseling referral, return if panic attacks frequent"
    },
    "Muscle Strain (Lumbar)": {
        "treatment": "Rest, avoid heavy lifting, proper body mechanics education",
        "medicines": ["Ibuprofen 400mg 1 tab every 8 hours with meals", "Muscle relaxant PRN"],
        "classification": "minor",
        "follow_up": "Return if pain radiates to leg or bowel/bladder changes"
    },
    "Mechanical Back Pain": {
        "treatment": "Continue light activity, heat therapy, stretching exercises",
        "medicines": ["Paracetamol 500mg PRN", "Ibuprofen 400mg TID with meals for 3 days"],
        "classification": "minor",
        "follow_up": "Physical therapy referral if not improved in 1 week"
    },
    "Sprain": {
        "treatment": "RICE protocol (Rest, Ice, Compression, Elevation)",
        "medicines": ["Ibuprofen 400mg every 8 hours with meals", "Paracetamol PRN for breakthrough pain"],
        "classification": "minor",
        "follow_up": "Return if swelling worsens or numbness develops"
    },
    "Dental Caries": {
        "treatment": "Temporary pain relief, dental referral for definitive treatment",
        "medicines": ["Paracetamol 500mg PRN for pain", "Chlorhexidine mouthwash BID"],
        "classification": "minor",
        "follow_up": "Dental clinic referral within 1 week"
    },
    "Gingivitis": {
        "treatment": "Oral hygiene instructions, soft toothbrush recommendation",
        "medicines": ["Chlorhexidine mouthwash 15ml BID for 7 days", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Dental follow up for professional cleaning"
    },
    "Periapical Abscess": {
        "treatment": "Pain management, antibiotic therapy, urgent dental referral",
        "medicines": ["Amoxicillin 500mg TID for 7 days", "Metronidazole 400mg TID for 5 days", "Paracetamol PRN"],
        "classification": "major",
        "follow_up": "Dental referral within 24-48 hours"
    },
    "Conjunctivitis (Viral)": {
        "treatment": "Cold compress, artificial tears, strict hand hygiene",
        "medicines": ["Artificial tears 1 drop every 4 hours", "Paracetamol PRN for discomfort"],
        "classification": "minor",
        "follow_up": "Return if vision changes or severe pain"
    },
    "Conjunctivitis (Bacterial)": {
        "treatment": "Warm compress, eyelid hygiene, avoid contact lenses",
        "medicines": ["Erythromycin ophthalmic ointment apply to conjunctiva TID", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Return if no improvement in 3 days"
    },
    "Allergic Conjunctivitis": {
        "treatment": "Cold compress, allergen avoidance, preservative-free artificial tears",
        "medicines": ["Olopatadine 0.1% eye drops 1 drop BID", "Artificial tears PRN"],
        "classification": "minor",
        "follow_up": "Allergist referral if recurrent"
    },
    "Acute Otitis Media": {
        "treatment": "Pain management, watchful waiting or antibiotics",
        "medicines": ["Amoxicillin 80mg/kg/day divided TID for 5 days", "Paracetamol PRN for pain/fever"],
        "classification": "minor",
        "follow_up": "Return if no improvement in 48 hours or ear discharge"
    },
    "Otitis Externa": {
        "treatment": "Keep ear dry, avoid swimming, ear wick if severe edema",
        "medicines": ["Ciprofloxacin 0.3% ear drops 4 drops BID for 7 days", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Return if no improvement in 3 days"
    },
    "Ear Wax Impaction": {
        "treatment": "Cerumenolytic drops, irrigation after 3-5 days if needed",
        "medicines": ["Carbamide peroxide 6.5% ear drops 5 drops BID for 4 days"],
        "classification": "minor",
        "follow_up": "Return for ear irrigation if not resolved"
    },
    "Iron Deficiency Anemia": {
        "treatment": "Dietary counseling, iron-rich foods, vitamin C with meals",
        "medicines": ["Ferrous sulfate 325mg 1 tab daily", "Vitamin C 500mg daily"],
        "classification": "minor",
        "follow_up": "CBC recheck in 4 weeks, hematology referral if no response"
    },
    "Stress-related Fatigue": {
        "treatment": "Sleep hygiene counseling, stress management, regular exercise",
        "medicines": ["Multivitamins 1 tab daily", "None - lifestyle modifications"],
        "classification": "minor",
        "follow_up": "Counseling referral if persistent"
    },
    "Food Poisoning": {
        "treatment": "Oral rehydration, rest, BRAT diet as tolerated",
        "medicines": ["Oral Rehydration Salts after each loose stool", "Paracetamol PRN for fever"],
        "classification": "minor",
        "follow_up": "Return if bloody diarrhea or severe dehydration"
    },
    "Irritable Bowel Syndrome": {
        "treatment": "Dietary modification, stress management, fiber intake adjustment",
        "medicines": ["Hyoscine butylbromide 10mg PRN for cramps", "Loperamide 2mg PRN (max 4/day)"],
        "classification": "minor",
        "follow_up": "Gastroenterology referral if persistent symptoms"
    },
    "Ankle Sprain (Grade 1)": {
        "treatment": "RICE protocol, early mobilization as tolerated",
        "medicines": ["Ibuprofen 400mg TID with meals for 5 days", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Physical therapy if not resolved in 2 weeks"
    },
    "Ankle Sprain (Grade 2)": {
        "treatment": "RICE protocol, ankle brace, protected weight bearing",
        "medicines": ["Ibuprofen 400mg TID with meals for 7 days", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Orthopedic referral if not improved in 1 week"
    },
    "Soft Tissue Injury": {
        "treatment": "RICE protocol, protection of injured area",
        "medicines": ["Diclofenac 50mg TID with meals", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Return if not improved in 1 week"
    },
    "Urinary Tract Infection": {
        "treatment": "Increase fluid intake, cranberry juice, complete antibiotic course",
        "medicines": ["Cefuroxime 250mg BID for 7 days", "Phenazopyridine 200mg TID for 2 days (for dysuria)"],
        "classification": "minor",
        "follow_up": "Urine culture if recurrent, return if fever develops"
    },
    "Urethritis": {
        "treatment": "Abstain from sexual activity, partner treatment if STI suspected",
        "medicines": ["Azithromycin 1g single dose", "Doxycycline 100mg BID for 7 days"],
        "classification": "minor",
        "follow_up": "STI screening, return if symptoms persist"
    },
    "Cystitis": {
        "treatment": "Hydration, avoid bladder irritants, antibiotic therapy",
        "medicines": ["Nitrofurantoin 100mg BID for 5 days", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Return if fever, back pain, or vomiting develops"
    },
    "Superficial Laceration": {
        "treatment": "Irrigation, antiseptic cleaning, sterile dressing",
        "medicines": ["Povidone-iodine for cleaning", "Paracetamol PRN for pain"],
        "classification": "minor",
        "follow_up": "Return in 2-3 days for dressing change"
    },
    "Contaminated Wound": {
        "treatment": "Thorough irrigation, debridement if needed, dressing",
        "medicines": ["Amoxicillin-clavulanate 625mg TID for 7 days", "Tetanus toxoid if indicated"],
        "classification": "minor",
        "follow_up": "Return in 2 days, tetanus prophylaxis confirmed"
    },
    "Clean Laceration": {
        "treatment": "Sterile dressing, adhesive strips if appropriate",
        "medicines": ["Paracetamol PRN", "Antibiotic ointment apply BID"],
        "classification": "minor",
        "follow_up": "Return if signs of infection"
    },
    "Panic Attack": {
        "treatment": "Breathing exercises, grounding techniques, counseling referral",
        "medicines": ["None - cognitive behavioral therapy recommended"],
        "classification": "minor",
        "follow_up": "Psychiatry referral if recurrent"
    },
    "Stress Response": {
        "treatment": "Stress management, adequate sleep, exercise",
        "medicines": ["None - lifestyle modifications recommended"],
        "classification": "minor",
        "follow_up": "Counseling services referral"
    },
    "Dysmenorrhea (Primary)": {
        "treatment": "Heat therapy, exercise, relaxation techniques",
        "medicines": ["Mefenamic acid 500mg 1 tab TID during menses", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Return if not controlled or new symptoms"
    },
    "Dysmenorrhea (Secondary)": {
        "treatment": "Pain management, gynecology evaluation",
        "medicines": ["Mefenamic acid 500mg TID", "Combined oral contraceptives (if appropriate)"],
        "classification": "minor",
        "follow_up": "Gynecology referral for evaluation"
    },
    "Menstrual Pain": {
        "treatment": "Heat application, rest, pain management",
        "medicines": ["Ibuprofen 400mg TID with meals", "Paracetamol PRN"],
        "classification": "minor",
        "follow_up": "Return if severe or persistent"
    }
}

# Medical history options
MEDICAL_HISTORY_OPTIONS = [
    "No known medical conditions",
    "Allergic rhinitis - well controlled",
    "History of asthma - childhood, now resolved",
    "Previous dengue fever (2022)",
    "Hypertension - on maintenance medication",
    "Hypothyroidism - on levothyroxine",
    "History of peptic ulcer disease",
    "No significant past medical history",
    "Previous surgery: appendectomy (2020)",
    "Diabetes mellitus type 2 - controlled",
    "History of kidney stones",
    "Migraine since adolescence",
    "Anxiety disorder - on follow up",
    "No known allergies",
    "History of tuberculosis - completed treatment",
    "Previous fracture: left arm (childhood)"
]

# Food allergies
FOOD_ALLERGIES = [
    "None known",
    "Shellfish",
    "Peanuts",
    "Dairy products",
    "Seafood",
    "None reported",
    "Eggs",
    "None known"
]

# Medicine allergies
MEDICINE_ALLERGIES = [
    "None known",
    "Penicillin - develops rash",
    "Sulfa drugs",
    "NSAIDs - causes gastric upset",
    "None reported",
    "Codeine - causes drowsiness",
    "Iodine contrast media"
]

# Current medication (most will be "None")
CURRENT_MEDS_OPTIONS = [
    "None",
    "Maintenance medications for hypertension",
    "Oral contraceptives",
    "Vitamins and supplements",
    "None at present",
    "Allergy medication as needed"
]

# Staff names for assignment
STAFF_ASSIGNMENTS = [
    (1, "Nurse Green"),
    (2, "Nurse Lloyd"),
    (3, "Nurse Lapig")
]


def get_db_connection():
    """Get database connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        sys.exit(1)


def fetch_patients_unified(conn) -> List[Dict[str, Any]]:
    """Fetch all patients from patients_unified table"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT patient_id, role, source_id, identifier, 
               first_name, middle_name, last_name, suffix,
               gender, age, birthdate, email, contact_number,
               department, course, level, position,
               blood_type, allergies, medical_conditions,
               is_active
        FROM patients_unified 
        WHERE is_active = 1
        ORDER BY role, last_name, first_name
    """)
    patients = cursor.fetchall()
    cursor.close()
    return patients


def get_medical_record_table(role: str) -> str:
    """Get the appropriate medical records table based on patient role"""
    role_lower = role.lower().strip()
    if role_lower in ['student', 'students']:
        return 'medical_records'
    elif role_lower in ['teaching staff', 'teaching_staff', 'teaching']:
        return 'teaching_medical_records'
    elif role_lower in ['non-teaching staff', 'non_teaching_staff', 'non teaching staff', 'nonteaching']:
        return 'non_teaching_medical_records'
    elif role_lower in ['dean', 'deans']:
        return 'dean_medical_records'
    elif role_lower in ['visitor', 'visitors']:
        return 'visitor_medical_records'
    else:
        return 'medical_records'


def get_patient_id_field(role: str) -> str:
    """Get the patient ID field name based on role"""
    role_lower = role.lower().strip()
    if role_lower in ['student', 'students']:
        return 'student_id'
    elif role_lower in ['teaching staff', 'teaching_staff', 'teaching']:
        return 'teaching_id'
    elif role_lower in ['non-teaching staff', 'non_teaching_staff', 'non teaching staff', 'nonteaching']:
        return 'non_teaching_id'
    elif role_lower in ['dean', 'deans']:
        return 'dean_id'
    elif role_lower in ['visitor', 'visitors']:
        return 'visitor_id'
    else:
        return 'student_id'


def generate_vital_signs(age: int, gender: str) -> Dict[str, Any]:
    """Generate realistic vital signs based on age and gender"""
    # Base vital signs
    if age < 18:
        # Younger patients
        bp_sys = random.randint(100, 120)
        bp_dia = random.randint(60, 75)
        pulse = random.randint(70, 90)
        temp = round(random.uniform(36.5, 37.2), 1)
        resp = random.randint(16, 22)
    elif age < 40:
        # Young adults
        bp_sys = random.randint(110, 130)
        bp_dia = random.randint(70, 85)
        pulse = random.randint(65, 85)
        temp = round(random.uniform(36.4, 37.3), 1)
        resp = random.randint(14, 20)
    elif age < 60:
        # Middle age
        bp_sys = random.randint(115, 140)
        bp_dia = random.randint(70, 90)
        pulse = random.randint(65, 85)
        temp = round(random.uniform(36.5, 37.3), 1)
        resp = random.randint(12, 20)
    else:
        # Older adults
        bp_sys = random.randint(120, 150)
        bp_dia = random.randint(70, 90)
        pulse = random.randint(60, 80)
        temp = round(random.uniform(36.3, 37.2), 1)
        resp = random.randint(12, 18)
    
    # Weight and height based on gender
    if gender and gender.lower() == 'male':
        weight = round(random.uniform(55, 85), 2)
        height = round(random.uniform(160, 180), 2)
    else:
        weight = round(random.uniform(45, 70), 2)
        height = round(random.uniform(150, 170), 2)
    
    # Calculate BMI
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1)
    
    return {
        'bp_systolic': bp_sys,
        'bp_diastolic': bp_dia,
        'pulse_rate': pulse,
        'temperature': temp,
        'respiratory_rate': resp,
        'weight': weight,
        'height': height,
        'bmi': bmi
    }


def generate_visit_datetime() -> Tuple[datetime, time]:
    """Generate realistic visit date and time
    
    Distributes visits across Aug 2024 - Mar 2025
    Clinic hours: 8:00 AM - 5:00 PM
    """
    # Date range: Aug 2024 - Mar 2025
    start_date = datetime(2024, 8, 1)
    end_date = datetime(2025, 3, 31)
    
    # Generate random date
    days_range = (end_date - start_date).days
    random_days = random.randint(0, days_range)
    visit_date = start_date + timedelta(days=random_days)
    
    # Generate clinic hours time (8 AM - 5 PM)
    # More visits in morning (peak at 9-11 AM) and afternoon (2-4 PM)
    hour_weights = [0.5, 0.8, 1.0, 1.0, 0.9, 0.7, 0.6, 0.8, 0.9, 1.0]
    hour = random.choices(range(8, 18), weights=hour_weights)[0]
    minute = random.choice([0, 15, 30, 45])
    
    visit_time = time(hour, minute)
    
    return visit_date, visit_time


def generate_medical_record(patient: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a realistic medical record for a patient"""
    
    # Select chief complaint
    chief_complaint = random.choice(list(CHIEF_COMPLAINTS.keys()))
    
    # Select matching diagnosis
    possible_diagnoses = CHIEF_COMPLAINTS[chief_complaint]
    diagnosis = random.choice(possible_diagnoses)
    
    # Get treatment info for this diagnosis
    treatment_info = DIAGNOSIS_TREATMENTS.get(diagnosis, {
        "treatment": "Symptomatic treatment and rest",
        "medicines": ["Paracetamol 500mg PRN"],
        "classification": "minor",
        "follow_up": "Return if symptoms persist"
    })
    
    # Generate visit date/time
    visit_date, visit_time = generate_visit_datetime()
    
    # Generate vital signs
    vitals = generate_vital_signs(
        patient.get('age') or random.randint(18, 50),
        patient.get('gender') or 'Unknown'
    )
    
    # Generate other fields
    medical_history = random.choice(MEDICAL_HISTORY_OPTIONS)
    food_allergies = random.choice(FOOD_ALLERGIES)
    medicine_allergies = random.choice(MEDICINE_ALLERGIES)
    
    # Fever duration (only if fever-related complaint)
    fever_complaints = ["Fever", "fever", "Viral", "Influenza"]
    if any(fc in chief_complaint for fc in fever_complaints):
        fever_duration = random.choice(["1 day", "2 days", "3 days", "<24 hours", ">3 days"])
    else:
        fever_duration = "N/A"
    
    # Current medication
    current_medication = random.choice(CURRENT_MEDS_OPTIONS)
    
    # Medication schedule (morning/afternoon/evening)
    med_schedules = [
        "After meals",
        "Every 8 hours",
        "Every 6 hours as needed",
        "Before bedtime",
        "Morning and evening",
        "As directed on label"
    ]
    medication_schedule = random.choice(med_schedules)
    
    # Select staff
    staff = random.choice(STAFF_ASSIGNMENTS)
    
    # Generate notes
    notes = f"Patient {patient['first_name']} {patient['last_name']} seen for {chief_complaint.lower()}. "
    notes += f"Diagnosed with {diagnosis}. "
    notes += f"{treatment_info['treatment']}. "
    notes += f"Patient counseled on {treatment_info['follow_up']}."
    
    # Endorsement required for major classifications
    classification = treatment_info['classification']
    endorsement_required = classification == 'major'
    endorsement_status = 'not_required' if not endorsement_required else 'pending'
    
    return {
        'patient_id': patient['patient_id'],
        'source_id': patient['source_id'],
        'role': patient['role'],
        'visit_date': visit_date.date(),
        'visit_time': visit_time,
        'chief_complaint': chief_complaint,
        'medical_history': medical_history,
        'symptoms': diagnosis,  # Using diagnosis as symptoms field
        'food_allergies': food_allergies,
        'medicine_allergies': medicine_allergies,
        'fever_duration': fever_duration,
        'current_medication': current_medication,
        'medication_schedule': medication_schedule,
        'treatment': treatment_info['treatment'],
        'prescribed_medicine': random.choice(treatment_info['medicines']),
        'blood_pressure_systolic': vitals['bp_systolic'],
        'blood_pressure_diastolic': vitals['bp_diastolic'],
        'pulse_rate': vitals['pulse_rate'],
        'temperature': vitals['temperature'],
        'respiratory_rate': vitals['respiratory_rate'],
        'weight': vitals['weight'],
        'height': vitals['height'],
        'bmi': vitals['bmi'],
        'staff_id': staff[0],
        'staff_name': staff[1],
        'notes': notes,
        'illness_classification_suggested': classification,
        'illness_classification_final': classification,
        'endorsement_required': endorsement_required,
        'endorsement_status': endorsement_status
    }


def insert_medical_record(conn, record: Dict[str, Any], patient_role: str):
    """Insert a medical record into the appropriate table"""
    
    table = get_medical_record_table(patient_role)
    id_field = get_patient_id_field(patient_role)
    
    cursor = conn.cursor()
    
    query = f"""
        INSERT INTO {table} (
            {id_field}, visit_date, visit_time, chief_complaint,
            medical_history, symptoms, food_allergies, medicine_allergies,
            fever_duration, current_medication, medication_schedule,
            treatment, prescribed_medicine,
            blood_pressure_systolic, blood_pressure_diastolic,
            pulse_rate, temperature, respiratory_rate,
            weight, height, bmi,
            staff_id, staff_name, notes,
            illness_classification_suggested, illness_classification_final,
            endorsement_required, endorsement_status,
            created_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    
    values = (
        record['source_id'],
        record['visit_date'],
        record['visit_time'],
        record['chief_complaint'],
        record['medical_history'],
        record['symptoms'],
        record['food_allergies'],
        record['medicine_allergies'],
        record['fever_duration'],
        record['current_medication'],
        record['medication_schedule'],
        record['treatment'],
        record['prescribed_medicine'],
        record['blood_pressure_systolic'],
        record['blood_pressure_diastolic'],
        record['pulse_rate'],
        record['temperature'],
        record['respiratory_rate'],
        record['weight'],
        record['height'],
        record['bmi'],
        record['staff_id'],
        record['staff_name'],
        record['notes'],
        record['illness_classification_suggested'],
        record['illness_classification_final'],
        record['endorsement_required'],
        record['endorsement_status'],
        datetime.now()
    )
    
    try:
        cursor.execute(query, values)
        record_id = cursor.lastrowid
        cursor.close()
        return record_id
    except mysql.connector.Error as err:
        print(f"❌ Error inserting record: {err}")
        cursor.close()
        return None


def count_existing_records(conn, role: str) -> int:
    """Count existing medical records for a role"""
    table = get_medical_record_table(role)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    except:
        cursor.close()
        return 0


def main():
    print("=" * 70)
    print("🏥 REALISTIC MEDICAL RECORDS DUMMY DATA GENERATOR")
    print("=" * 70)
    print("\nThis script will generate 1-3 realistic medical records per patient")
    print("with proper clinical data matching complaints, diagnoses, and treatments.")
    print("\nFeatures:")
    print("  • Realistic chief complaints matched to diagnoses")
    print("  • Age-appropriate vital signs")
    print("  • Consistent treatment plans")
    print("  • Visits distributed Aug 2024 - Mar 2025")
    print("  • 1-3 records per patient (not too many)")
    print("=" * 70)
    
    # Connect to database
    print("\n📡 Connecting to database...")
    conn = get_db_connection()
    print("✅ Connected to iclinic_db")
    
    # Fetch patients
    print("\n👥 Fetching patients from patients_unified...")
    patients = fetch_patients_unified(conn)
    print(f"✅ Found {len(patients)} active patients")
    
    if not patients:
        print("❌ No patients found. Exiting.")
        conn.close()
        return
    
    # Show patient breakdown by role
    role_counts = {}
    for p in patients:
        role = p['role']
        role_counts[role] = role_counts.get(role, 0) + 1
    
    print("\n📊 Patient breakdown:")
    for role, count in sorted(role_counts.items()):
        print(f"   • {role}: {count}")
    
    # Check existing records
    print("\n🔍 Checking existing medical records...")
    total_existing = 0
    for role in role_counts.keys():
        count = count_existing_records(conn, role)
        total_existing += count
        if count > 0:
            print(f"   • {role}: {count} existing records")
    
    if total_existing > 0:
        print(f"\n⚠️  Found {total_existing} existing medical records")
        response = input("   Do you want to add more records? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Operation cancelled.")
            conn.close()
            return
    
    # Generate records
    print("\n📝 Generating medical records...")
    print("-" * 70)
    
    total_created = 0
    records_per_patient_dist = {1: 0, 2: 0, 3: 0}
    
    for patient in patients:
        # Decide how many records for this patient (1-3, weighted toward fewer)
        num_records = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        records_per_patient_dist[num_records] += 1
        
        patient_name = f"{patient['first_name']} {patient['last_name']}"
        
        for i in range(num_records):
            record = generate_medical_record(patient)
            record_id = insert_medical_record(conn, record, patient['role'])
            
            if record_id:
                total_created += 1
                if i == 0:  # Only print first record per patient to reduce output
                    print(f"✅ {patient_name} ({patient['role']}) - {num_records} record(s)")
    
    print("-" * 70)
    
    # Summary
    print(f"\n{'=' * 70}")
    print("📊 GENERATION SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total patients processed: {len(patients)}")
    print(f"Total medical records created: {total_created}")
    print(f"\nRecords per patient distribution:")
    print(f"   • 1 record:  {records_per_patient_dist[1]} patients")
    print(f"   • 2 records: {records_per_patient_dist[2]} patients")
    print(f"   • 3 records: {records_per_patient_dist[3]} patients")
    
    # Show records by role
    print(f"\nRecords by patient role:")
    for role in sorted(role_counts.keys()):
        count = count_existing_records(conn, role)
        print(f"   • {role}: {count} total records")
    
    print(f"\n{'=' * 70}")
    print("✅ DUMMY DATA GENERATION COMPLETE!")
    print(f"{'=' * 70}")
    
    conn.close()


if __name__ == "__main__":
    main()
