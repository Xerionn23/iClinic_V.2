# President/Deans Report Dashboard - Database Integration Plan

## 📊 Current Status
The DEANS_REPORT.html currently has **hardcoded data**. We need to connect it to the database.

## 🎯 What President/Deans Need to See

### 1. **KPI Cards** (Top Statistics)
- **Total Students**: Count of active students from `students` table
- **Clinic Visits**: Total medical records from `medical_records` table
- **Health Alerts**: Cases with temperature ≥ 38°C or critical symptoms
- **Critical Cases**: Recent urgent cases (last 7 days, temp ≥ 39°C)

### 2. **Student Health Analytics** (Doughnut Chart)
- **Critical**: Temperature ≥ 39°C or emergency complaints
- **Moderate**: Temperature ≥ 38°C or moderate symptoms
- **Minor**: All other cases
- Data source: `medical_records` table with severity classification

### 3. **Monthly Clinic Visits Trend** (Line Chart)
- Last 6 months of clinic visits
- Shows trend over time
- Data source: `medical_records` grouped by month

### 4. **Health Reports by Department** (Bar Chart)
- Number of clinic visits per department
- Top 10 departments
- Data source: `medical_records` JOIN `students` on department

### 5. **Recent Student Reports** (List)
- Latest 20 medical records
- Shows: Student name, condition, severity, date, nurse name
- Color-coded by severity (red=critical, yellow=moderate, green=minor)
- Data source: `medical_records` JOIN `students` JOIN `users`

## 🔌 API Endpoints Created

### 1. `/api/deans-president/dashboard-stats`
Returns:
```json
{
  "success": true,
  "kpi": {
    "totalStudents": 2847,
    "clinicVisits": 456,
    "healthAlerts": 12,
    "criticalCases": 3
  },
  "severityData": [
    {"severity": "critical", "count": 15},
    {"severity": "moderate", "count": 45},
    {"severity": "minor", "count": 396}
  ],
  "monthlyVisits": [
    {"month": "2025-05", "visits": 78},
    {"month": "2025-06", "visits": 82},
    ...
  ],
  "departmentReports": [
    {"department": "College of Computer Studies", "count": 125},
    {"department": "College of Education", "count": 98},
    ...
  ]
}
```

### 2. `/api/deans-president/recent-reports`
Returns:
```json
{
  "success": true,
  "reports": [
    {
      "id": 1,
      "studentName": "Joseph Flynn",
      "condition": "Severe headache and fever",
      "date": "2025-10-25",
      "temperature": 38.5,
      "nurseName": "Lloyd Lapig",
      "department": "College of Computer Studies",
      "severity": "moderate"
    },
    ...
  ]
}
```

## 📝 Frontend Changes Needed

### 1. **Alpine.js Data Object**
Replace hardcoded data with:
```javascript
{
  loading: true,
  error: null,
  kpiData: {
    totalStudents: 0,
    clinicVisits: 0,
    healthAlerts: 0,
    criticalCases: 0
  },
  recentStudentReports: [],
  severityChart: null,
  monthlyVisitsChart: null,
  departmentChart: null
}
```

### 2. **Load Data Function**
```javascript
async loadDashboardData() {
  try {
    this.loading = true;
    const response = await fetch('/api/deans-president/dashboard-stats');
    const data = await response.json();
    
    if (data.success) {
      this.kpiData = data.kpi;
      this.initSeverityChart(data.severityData);
      this.initMonthlyVisitsChart(data.monthlyVisits);
      this.initDepartmentChart(data.departmentReports);
    }
  } catch (error) {
    this.error = error.message;
  } finally {
    this.loading = false;
  }
}
```

### 3. **Chart Initialization**
- **Severity Doughnut Chart**: Uses Chart.js with severity data
- **Monthly Visits Line Chart**: Shows 6-month trend
- **Department Bar Chart**: Top departments by visit count

### 4. **Auto-refresh**
- Refresh data every 30 seconds
- Manual refresh button
- Loading states during refresh

## 🎨 Visual Enhancements

### Color Coding
- **Critical**: Red (#ef4444)
- **Moderate**: Yellow/Orange (#f59e0b)
- **Minor**: Green (#10b981)

### Loading States
- Skeleton loaders for cards
- Spinner for charts
- Smooth transitions

### Empty States
- "No data available" messages
- Helpful icons and text
- Call-to-action if needed

## ✅ Implementation Steps

1. ✅ Create API endpoints in app.py
2. ⏳ Update HTML with database connectivity
3. ⏳ Replace hardcoded data with API calls
4. ⏳ Initialize Chart.js with real data
5. ⏳ Add loading and error states
6. ⏳ Implement auto-refresh
7. ⏳ Test with real database data

## 🔐 Security
- Session-based authentication required
- Role validation (president/deans only)
- SQL injection prevention (parameterized queries)
- Error handling and logging

## 📊 Benefits
- **Real-time data**: Always up-to-date
- **Accurate insights**: Based on actual clinic records
- **Better decisions**: Data-driven management
- **Professional**: Dynamic charts and statistics
- **Scalable**: Works with growing data

Next: Implement the frontend changes to connect to these APIs!
