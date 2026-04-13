#!/usr/bin/env python3
"""
Simple script to query the local teaching medical records API.
Usage:
  python scripts/check_teaching_medical_record.py T3
  python scripts/check_teaching_medical_record.py 3

If `requests` is missing, install with: pip install requests
"""
import sys
import json

try:
    import requests
except Exception:
    print("The 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


def get_teaching_records(teaching_id: str, host: str = "http://127.0.0.1:5000"):
    # Accept both formats: 'T3' or '3'
    tid = str(teaching_id).upper()
    if tid.startswith('T'):
        tid = tid[1:]
    endpoint = f"{host}/api/teaching-medical-records/{tid}"
    print(f"GET {endpoint}")
    try:
        r = requests.get(endpoint, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return

    print("Status code:", r.status_code)
    content_type = r.headers.get('Content-Type','')
    if 'application/json' in content_type:
        try:
            print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        except Exception as e:
            print('Failed to decode JSON response:', e)
            print(r.text)
    else:
        print(r.text)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/check_teaching_medical_record.py <TEACHING_ID>')
        print('Example: python scripts/check_teaching_medical_record.py T3')
        sys.exit(1)
    get_teaching_records(sys.argv[1])
