# Medical Letter Generation Setup Guide

## 📋 Overview
This setup allows you to generate medical acknowledgement letters using your existing Word template with exact formatting preserved.

## 🔧 Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Update Your Word Template
Open your `medical aknowlegement letter.docx` file and replace the placeholders with these exact formats:

**Current placeholders** → **New placeholders**
- `[Name patient]` → `{{ name }}`
- `[Visit Date]` → `{{ visit_date }}`
- `[TIME]` → `{{ time }}`
- `[Issued Date]` → `{{ issued_date }}`

**Example template content:**
```
NORZAGARAY COLLEGE
Municipal Compound
Brgy. Poblacion, Norzagaray, Bulacan
Email: norzagaraycollege2007@gmail.com

MEDICAL ACKNOWLEDGEMENT LETTER

This is to certify that {{ name }} was present at the Norzagaray College Medical Clinic on {{ visit_date }} at {{ time }} for medical consultation and healthcare services.

During the aforementioned visit, the individual received proper medical attention from our licensed healthcare professionals in accordance with established medical protocols and institutional standards. The consultation was conducted within the official operating hours of the clinic facility.

This certification is issued upon official request and may be used for academic, administrative, or other legitimate purposes as deemed necessary by the concerned parties. The information contained herein is true and accurate to the best of our knowledge and records.

Issued this {{ issued_date }} at the Norzagaray College Medical Clinic, Norzagaray, Bulacan, Philippines, for whatever legal purpose this certification may serve.


________________________
Lloyd Lapig
Clinic Nurse
Norzagaray College Medical Clinic
```

### 3. Start the Flask Server
```bash
python generate_letter.py
```

The server will run on `http://localhost:5001`

### 4. Test the Integration
1. Open your iClinic system
2. Go to Patient Management
3. Select a patient with medical records
4. Click the green "Print" button in the Actions column
5. The system will generate and download a DOCX file with your exact template formatting

## 🎯 Features

### DOCX Generation
- **Endpoint**: `POST /generate-medical-letter`
- **Output**: Downloads `.docx` file with exact Word formatting
- **Maintains**: Fonts, spacing, margins, headers, footers

### PDF Generation (Optional)
- **Endpoint**: `POST /generate-medical-letter-pdf`
- **Output**: Downloads `.pdf` file for direct printing
- **Requires**: Microsoft Word installed (for docx2pdf conversion)

## 📁 File Structure
```
iClini V.2/
├── generate_letter.py          # Flask backend server
├── medical aknowlegement letter.docx  # Your Word template
├── requirements.txt            # Python dependencies
└── pages/staff/Staff-Patients.html    # Frontend integration
```

## 🔍 Troubleshooting

### Common Issues:
1. **"Template file not found"**
   - Ensure `medical aknowlegement letter.docx` is in the root directory
   - Check file name spelling exactly

2. **"Failed to generate certificate"**
   - Make sure Flask server is running (`python generate_letter.py`)
   - Check console for detailed error messages

3. **PDF conversion fails**
   - Install Microsoft Word (required for docx2pdf)
   - Or use DOCX output and convert manually

### Testing the Flask Server:
```bash
curl -X POST http://localhost:5001/generate-medical-letter \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","visit_date":"October 7, 2025","time":"2:30 PM","issued_date":"October 7, 2025"}'
```

## ✅ Success Indicators
- Flask server starts without errors
- Clicking "Print" button downloads a DOCX file
- Generated document maintains exact Word template formatting
- Patient data is correctly populated in placeholders
