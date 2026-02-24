import re

# Read the file
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'r', encoding='utf-8') as f:
    content = f.read()

# List of chart IDs to add data-chart-container attribute to their parent divs
chart_ids = [
    'revenueChart',
    'monthlyVisitsChart',
    'patientDemographicsChart',
    'medicalRecordsChart',
    'appointmentStatusChart',
    'bookingTrendsChart',
    'appointmentTypesChart',
    'consultationMetricsChart',
    'consultationPatientTypesChart',
    'stockLevelsChart',
    'suppliesStatusChart',
    'announcementCategoriesChart',
    'priorityAnalysisChart',
    'monthlyAppointmentsChart',
    'monthlyMedicineChart',
    'monthlyConsultationsChart',
    'monthlyNewPatientsChart',
    'monthlyOverviewChart'
]

# For each chart, find its parent container div and add data-chart-container attribute
for chart_id in chart_ids:
    # Pattern to find the chart's parent container (the div with bg-white rounded-2xl shadow-lg)
    pattern = rf'(<div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8[^>]*)(>(?:(?!<div class="bg-white rounded-2xl).)*?<canvas id="{chart_id}")'
    
    def add_attribute(match):
        opening_tag = match.group(1)
        rest = match.group(2)
        # Only add if not already present
        if 'data-chart-container' not in opening_tag:
            return opening_tag + ' data-chart-container' + rest
        return match.group(0)
    
    content = re.sub(pattern, add_attribute, content, flags=re.DOTALL)

# Write back
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Chart container attributes added successfully!")
print(f"✅ Processed {len(chart_ids)} charts")
