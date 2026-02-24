import requests
import json

try:
    # Test the /api/visits endpoint
    response = requests.get('http://127.0.0.1:5000/api/visits')
    
    if response.status_code == 200:
        data = response.json()
        print('\n' + '='*70)
        print('📊 /api/visits ENDPOINT RESPONSE')
        print('='*70)
        print(f'Total records returned: {len(data)}')
        print('='*70)
        
        # Count by patient type
        type_counts = {}
        for record in data:
            patient_type = record.get('patient_type', 'Unknown')
            type_counts[patient_type] = type_counts.get(patient_type, 0) + 1
        
        print('\nBreakdown by Patient Type:')
        print('-'*70)
        for ptype, count in sorted(type_counts.items()):
            print(f'  {ptype:<30} : {count:>3} records')
        print('-'*70)
        print(f'  {"TOTAL":<30} : {len(data):>3} records')
        print('='*70)
        
        # Show first 3 records
        print('\nFirst 3 records:')
        for i, record in enumerate(data[:3], 1):
            print(f'\n{i}. {record.get("patient_type")} - {record.get("patient_name")}')
            print(f'   Visit Date: {record.get("visit_date")}')
            print(f'   Complaint: {record.get("chief_complaint")}')
        
    else:
        print(f'❌ Error: Status code {response.status_code}')
        print(response.text)
        
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
