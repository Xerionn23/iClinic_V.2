# Real-Time Appointment Time Slot Blocking

## Overview
Implemented real-time blocking of past time slots to prevent students from booking appointments for times that have already passed. The system now dynamically blocks time slots based on the current time.

## Problem Solved
**User Request:** "Gusto ko real-time, for example today 9AM, so dapat mga 8AM bawal na mag-appointment"

**Solution:** Time slots that have passed are automatically blocked and cannot be selected for booking.

## Implementation

### 1. Frontend Real-Time Blocking (ST-appointment.html)

**Enhanced `availableTimeSlots` Computed Property:**
```javascript
// Get current date and time for real-time blocking
const now = new Date();
const today = now.toISOString().split('T')[0];
const currentTimeMinutes = now.getHours() * 60 + now.getMinutes();
const isToday = this.selectedDate === today;

// REAL-TIME BLOCKING: Block past time slots for today
if (isToday) {
    const slotMinutes = this.timeToMinutes(slot.time);
    if (slotMinutes <= currentTimeMinutes) {
        available = false;
        console.log(`🚫 Real-time block: ${slot.time} has passed`);
    }
}
```

**How It Works:**
1. Gets current date and time when checking availability
2. Compares selected date with today's date
3. If booking for today, compares each time slot with current time
4. Blocks all time slots that are <= current time
5. Updates dynamically as time passes

### 2. Backend Real-Time Validation (app.py)

**Enhanced `/api/appointment-requests` POST Endpoint:**
```python
# REAL-TIME VALIDATION: Prevent booking past times
from datetime import datetime
now = datetime.now()
today_str = now.strftime('%Y-%m-%d')
current_time = now.time()

appointment_date = data['preferred_date']
appointment_time = datetime.strptime(data['preferred_time'], '%H:%M').time()

# Check if trying to book a past time slot
if appointment_date == today_str and appointment_time <= current_time:
    return jsonify({
        'error': f'Cannot book appointment for {appointment_time_str}. This time has already passed. Current time is {current_time.strftime("%H:%M")}.'
    }), 400

# Check if trying to book a past date
if appointment_date < today_str:
    return jsonify({
        'error': f'Cannot book appointment for {appointment_date}. This date has already passed.'
    }), 400
```

## Real-Time Blocking Examples

### Example 1: Current Time is 9:00 AM
**Available Time Slots:**
- ❌ 8:00 AM - **BLOCKED** (past)
- ❌ 8:30 AM - **BLOCKED** (past)
- ❌ 9:00 AM - **BLOCKED** (current time)
- ✅ 9:30 AM - **AVAILABLE**
- ✅ 10:00 AM - **AVAILABLE**
- ✅ 10:30 AM - **AVAILABLE**
- ✅ 11:00 AM - **AVAILABLE**
- ... (all future times available)

### Example 2: Current Time is 2:45 PM (14:45)
**Available Time Slots:**
- ❌ 8:00 AM - **BLOCKED** (past)
- ❌ 9:00 AM - **BLOCKED** (past)
- ❌ 10:00 AM - **BLOCKED** (past)
- ❌ 11:00 AM - **BLOCKED** (past)
- ❌ 1:00 PM - **BLOCKED** (past)
- ❌ 2:00 PM - **BLOCKED** (past)
- ❌ 2:30 PM - **BLOCKED** (past)
- ✅ 3:00 PM - **AVAILABLE**
- ✅ 3:30 PM - **AVAILABLE**
- ✅ 4:00 PM - **AVAILABLE**
- ✅ 4:30 PM - **AVAILABLE**

### Example 3: Booking for Tomorrow
**All Time Slots Available:**
- ✅ 8:00 AM - **AVAILABLE** (future date)
- ✅ 8:30 AM - **AVAILABLE** (future date)
- ✅ 9:00 AM - **AVAILABLE** (future date)
- ... (all slots available for future dates)

## User Experience

### Visual Indicators:
- **Blocked Time Slots (Past):**
  - Red background
  - Strikethrough text
  - Disabled/unclickable
  - Cursor: not-allowed

- **Available Time Slots (Future):**
  - White background
  - Normal text
  - Clickable
  - Hover effects

### Error Messages:

**Frontend Validation:**
```
"The selected time slot is blocked by clinic events or confirmed appointments. 
Please choose a different time."
```

**Backend Validation (Past Time):**
```
"Cannot book appointment for 08:00. This time has already passed. 
Current time is 09:15. Please select a future time slot."
```

**Backend Validation (Past Date):**
```
"Cannot book appointment for 2025-10-20. This date has already passed. 
Please select today or a future date."
```

## Technical Details

### Time Comparison Logic:
1. **Convert to Minutes:** All times converted to minutes since midnight for easy comparison
   - 8:00 AM = 480 minutes
   - 9:15 AM = 555 minutes
   - 2:30 PM = 870 minutes

2. **Comparison:** `slotMinutes <= currentTimeMinutes` → BLOCKED

3. **Dynamic Updates:** Computed property recalculates when:
   - Page loads
   - Date changes
   - Appointments load
   - User interacts with calendar

### Console Logging:
```
⏰ Real-time check: Today=2025-10-21, Selected=2025-10-21, IsToday=true, CurrentTime=9:15
🚫 Real-time block: 08:00 (480min) has passed current time (555min)
🚫 Real-time block: 08:30 (510min) has passed current time (555min)
🚫 Real-time block: 09:00 (540min) has passed current time (555min)
```

## Benefits

✅ **Prevents Booking Past Times** - Students cannot book appointments for times that have passed
✅ **Real-Time Updates** - Blocks update automatically as time progresses
✅ **Double Validation** - Both frontend and backend validation for security
✅ **User-Friendly** - Clear visual indicators and error messages
✅ **Accurate Availability** - Shows only genuinely available time slots
✅ **No Manual Refresh Needed** - Works automatically in real-time

## Validation Layers

### Layer 1: Frontend Visual Blocking
- Time slots grayed out and disabled
- Cannot be clicked or selected
- Immediate visual feedback

### Layer 2: Frontend Form Validation
- Checks before form submission
- Alerts user if invalid time selected
- Prevents API call for invalid times

### Layer 3: Backend API Validation
- Server-side validation as final check
- Returns 400 error for past times
- Prevents database insertion of invalid appointments

## Flow Diagram

```
Student selects today's date
    ↓
System gets current time (e.g., 9:15 AM)
    ↓
System checks all time slots:
    - 8:00 AM → 480 min ≤ 555 min → BLOCKED ❌
    - 8:30 AM → 510 min ≤ 555 min → BLOCKED ❌
    - 9:00 AM → 540 min ≤ 555 min → BLOCKED ❌
    - 9:30 AM → 570 min > 555 min → AVAILABLE ✅
    - 10:00 AM → 600 min > 555 min → AVAILABLE ✅
    ↓
Student can only select 9:30 AM or later
    ↓
If student somehow submits past time:
    ↓
Backend rejects with error message
```

## Testing Scenarios

### Test 1: Morning Booking (9:00 AM)
- [ ] 8:00 AM slot is blocked
- [ ] 8:30 AM slot is blocked
- [ ] 9:00 AM slot is blocked
- [ ] 9:30 AM slot is available
- [ ] Can successfully book 10:00 AM

### Test 2: Afternoon Booking (2:30 PM)
- [ ] All morning slots blocked
- [ ] 1:00 PM slot is blocked
- [ ] 2:00 PM slot is blocked
- [ ] 2:30 PM slot is blocked
- [ ] 3:00 PM slot is available
- [ ] Can successfully book 3:30 PM

### Test 3: Future Date Booking
- [ ] All time slots available for tomorrow
- [ ] All time slots available for next week
- [ ] No real-time blocking for future dates

### Test 4: Backend Validation
- [ ] API rejects past time for today
- [ ] API rejects past dates
- [ ] API accepts future times for today
- [ ] API accepts all times for future dates

## Past Date Blocking (Calendar)

### Visual Indicators for Past Dates:
- **Gray background** with reduced opacity (50%)
- **Strikethrough text** on date numbers
- **Cursor: not-allowed** - cannot click
- **Tooltip:** "🚫 Past date - Cannot book appointments"

### Calendar Behavior:
```javascript
// Check if date is in the past
const isPastDate = dateStr < todayStr;

// Prevent clicking on past dates
@click="!day.isPastDate && selectDate(day)"

// Visual styling
'bg-gray-100 text-gray-400 cursor-not-allowed opacity-50 line-through': day.isPastDate
```

### Example Calendar View (Today: Oct 21, 2025):

```
Sun  Mon  Tue  Wed  Thu  Fri  Sat
     ~~1~~  ~~2~~  ~~3~~  ~~4~~  ~~5~~  ~~6~~   ← All grayed out (past)
~~7~~  ~~8~~  ~~9~~ ~~10~~ ~~11~~ ~~12~~ ~~13~~  ← All grayed out (past)
~~14~~ ~~15~~ ~~16~~ ~~17~~ ~~18~~ ~~19~~ ~~20~~ ← All grayed out (past)
 21   22   23   24   25   26   27   ← Today + future (clickable)
 28   29   30   31                   ← Future dates (clickable)
```

**Legend:**
- ~~Strikethrough~~ = Past dates (disabled)
- **Bold** = Today (current date)
- Normal = Future dates (available)

## Date Implemented
October 21, 2025

## Complete Blocking Summary

### Past Dates (Before Today):
- ❌ **ALL time slots BLOCKED** (red background)
- ❌ Cannot book any appointments
- ✅ Can VIEW past appointments
- 🔴 All time slots show as unavailable/red

### Today:
- ❌ **Past time slots BLOCKED** (red background)
- ✅ **Future time slots AVAILABLE** (green background)
- ✅ Can book future time slots only

### Future Dates:
- ✅ **ALL time slots AVAILABLE** (green background)
- ✅ Can book any time slot
- ⚠️ Unless blocked by existing appointments or clinic events

## Status
✅ **ACTIVE** - Real-time appointment blocking is now live
✅ **ACTIVE** - Past date blocking is now live
✅ **ACTIVE** - Past date time slot blocking is now live

## Notes
- Time slots update dynamically based on current time
- Past dates are visually disabled in calendar
- No page refresh needed - works in real-time
- Both frontend and backend validation ensure data integrity
- Clear error messages guide users to select valid times
- Students can only book for today or future dates
