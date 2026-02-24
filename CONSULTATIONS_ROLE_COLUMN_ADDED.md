# Consultations Table - Role Column Implementation

## Feature Added
Added a new **Role** column to the consultations table to identify the type of patient for each consultation record.

## Patient Role Types
The system now displays color-coded badges for different patient types:

1. **Student** - Blue badge (`bg-blue-100 text-blue-800`)
2. **Teaching Staff** - Green badge (`bg-green-100 text-green-800`)
3. **Non-Teaching Staff** - Purple badge (`bg-purple-100 text-purple-800`)
4. **Visitor** - Orange badge (`bg-orange-100 text-orange-800`)

## Implementation Details

### Frontend Changes (Staff-Consultations.html)

#### 1. Table Header
Added new column header between "Patient Name" and "Chief Complaint":
```html
<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
```

#### 2. Table Body
Added color-coded role badge with dynamic styling:
```html
<td class="px-6 py-4 whitespace-nowrap">
    <span x-text="consultation.role || 'Student'" 
          :class="{
              'bg-blue-100 text-blue-800': consultation.role === 'Student' || !consultation.role,
              'bg-green-100 text-green-800': consultation.role === 'Teaching Staff',
              'bg-purple-100 text-purple-800': consultation.role === 'Non-Teaching Staff',
              'bg-orange-100 text-orange-800': consultation.role === 'Visitor'
          }"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
    </span>
</td>
```

#### 3. Data Mapping
Updated the consultation data mapping to include role:
```javascript
this.consultations = records.map(record => ({
    id: record.id,
    patient: record.patient_name || 'Unknown Patient',
    patientId: record.patient_id ? `STU-${record.patient_id}` : 'N/A',
    role: record.patient_role || 'Student',  // ✅ NEW FIELD
    date: this.formatDate(record.visit_date),
    time: this.formatTimeOnly(record.visit_time) || 'N/A',
    // ... other fields
}));
```

### Backend Changes (app.py)

#### 1. Role Determination Logic
Added patient role identification in `/api/test-all-medical-records` endpoint:
```python
# Determine patient role - medical_records are for students
patient_role = 'Student'
```

**Note**: Currently, all medical records are from students. In the future, this can be enhanced to:
- Check `visitor_medical_records` table for Visitors
- Check `users` table with position field for Teaching Staff / Non-Teaching Staff

#### 2. API Response
Added `patient_role` field to the API response:
```python
result.append({
    # ... other fields
    'patient_name': patient_name,
    'patient_role': patient_role,  # ✅ NEW FIELD
    'patient_course': r[31] if r[31] else 'Unknown Course',
    'patient_level': r[32] if r[32] else 'Unknown Level',
    # ... timestamps
})
```

## Visual Design

### Color Scheme
- **Blue** (Student): Professional, academic feel
- **Green** (Teaching Staff): Authority, expertise
- **Purple** (Non-Teaching Staff): Support, administrative
- **Orange** (Visitor): Temporary, walk-in patients

### Badge Style
- Rounded pill shape (`rounded-full`)
- Small text (`text-xs`)
- Medium font weight (`font-medium`)
- Proper padding (`px-2.5 py-0.5`)
- Inline flex display for proper alignment

## Future Enhancements

### Multi-Table Patient Detection
To support all patient types, the backend can be enhanced to:

```python
# Determine patient role based on source table
patient_role = 'Student'  # Default

# Check if patient exists in visitors table
cursor.execute("SELECT id FROM visitors WHERE id = %s", (patient_id,))
if cursor.fetchone():
    patient_role = 'Visitor'
else:
    # Check if patient exists in users table (staff)
    cursor.execute("SELECT position FROM users WHERE id = %s", (patient_id,))
    user = cursor.fetchone()
    if user:
        position = user[0]
        if 'Teaching' in position or 'Faculty' in position:
            patient_role = 'Teaching Staff'
        else:
            patient_role = 'Non-Teaching Staff'
```

### Filter by Role
Add a dropdown filter to show consultations by patient type:
```html
<select x-model="selectedRole">
    <option value="">All Roles</option>
    <option value="Student">Students</option>
    <option value="Teaching Staff">Teaching Staff</option>
    <option value="Non-Teaching Staff">Non-Teaching Staff</option>
    <option value="Visitor">Visitors</option>
</select>
```

## Benefits

1. **Clear Patient Identification** - Staff can immediately see what type of patient they're dealing with
2. **Better Organization** - Easy to filter and sort consultations by patient type
3. **Visual Clarity** - Color-coded badges make scanning the table faster
4. **Data Integrity** - Proper role tracking for reporting and analytics
5. **Professional UI** - Modern, clean design that matches the overall system aesthetic

## Files Modified
- `c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Consultations.html` - Lines 590-618
- `c:\xampp\htdocs\iClini V.2\app.py` - Lines 9051-9095

## Result
✅ Role column now visible in consultations table
✅ Color-coded badges for easy identification
✅ Backend provides patient_role data
✅ Frontend displays role with proper styling
✅ Default to "Student" for all current medical records
