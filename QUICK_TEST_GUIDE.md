# QUICK TEST GUIDE - Medical Records to Consultations Integration

## Mabilis na Paraan Para I-Test

### 1. Add Medical Record for Student

```
1. Open Staff-Patients.html
2. Click any STUDENT sa patient list
3. Click "Add Medical Record" button (green button)
4. Fill the form:
   - Chief Complaint: "Headache and fever"
   - Treatment: "Paracetamol 500mg, rest"
   - (Optional: Fill vital signs)
5. Click "Save Medical Record"
6. Wait for success message
```

### 2. Verify sa Consultations

```
1. Open Staff-Consultations.html
2. Click "All Consultations" tab (if not already there)
3. Click "Refresh Data" button (purple button)
4. Look for your new record:
   - Should show patient name
   - Blue badge with "Student"
   - Chief complaint: "Headache and fever"
   - Treatment: "Paracetamol 500mg, rest"
```

### 3. Test for Other Patient Types

**For Visitor:**
```
1. Staff-Patients.html → Select VISITOR
2. Add Medical Record
3. Staff-Consultations.html → Should see ORANGE "Visitor" badge
```

**For Teaching Staff:**
```
1. Staff-Patients.html → Select TEACHING STAFF
2. Add Medical Record
3. Staff-Consultations.html → Should see GREEN "Teaching Staff" badge
```

**For Non-Teaching Staff:**
```
1. Staff-Patients.html → Select NON-TEACHING STAFF
2. Add Medical Record
3. Staff-Consultations.html → Should see PURPLE "Non-Teaching Staff" badge
```

## Expected Results

✅ **Medical record appears immediately** after refresh
✅ **Correct patient name** displayed
✅ **Correct role badge** with proper color
✅ **All medical details** available when clicking "View"
✅ **Sorted by date** (most recent first)

## Troubleshooting

### If record doesn't appear:

1. **Check browser console** (F12)
   - Look for: `✅ Loaded medical records: X records`
   - Should show increased count

2. **Refresh the page** completely (Ctrl+F5)

3. **Check if medical record was saved**:
   - Go back to Staff-Patients.html
   - Select the same patient
   - Check if medical record appears in the list

4. **Check database connection**:
   - Look for console errors
   - Verify Flask server is running

## Console Logs to Look For

### Success Indicators:
```
🔍 Loading medical records from API...
📡 API Response status: 200
✅ Loaded medical records: 45 records
🎯 Transformed consultations: 45 items
```

### Error Indicators:
```
❌ Failed to load medical records: 500
💥 Error loading medical records: [error message]
```

## Quick Verification Checklist

- [ ] Medical record saved successfully in Staff-Patients.html
- [ ] Success notification appeared
- [ ] Navigated to Staff-Consultations.html
- [ ] Clicked "Refresh Data" button
- [ ] New record appears in table
- [ ] Patient name is correct
- [ ] Role badge is correct color
- [ ] Can click "View" to see full details
- [ ] All medical information is displayed correctly

## Ang Pinaka-Important

**Kapag nag-add ng medical record sa Staff-Patients.html, AUTOMATIC na makikita sa Staff-Consultations.html!**

Hindi na kailangan ng additional steps. Just add medical record, then refresh ang consultations page. Done! 🎉
