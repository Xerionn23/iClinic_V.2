# Cancel Appointment Feature

## Overview
Implemented the ability for students to cancel their confirmed appointments through the student appointment interface.

## Feature Details

### Student Interface (ST-appointment.html)

**Cancel Button:**
- Appears only for **Confirmed** appointments
- Red icon (x-circle) with hover effect
- Located next to the appointment status badge
- Tooltip: "Cancel Appointment"

**Workflow:**
1. Student views their confirmed appointments
2. Clicks the cancel button (red X icon)
3. Confirmation dialog appears: "Are you sure you want to cancel this appointment?"
4. If confirmed:
   - API call to update appointment status to 'Cancelled'
   - Success message: "Appointment cancelled successfully!"
   - Appointments list refreshes automatically
   - Status badge changes to red "Cancelled"

### Visual Indicators

**Appointment Status Colors:**
- 🟡 **Pending** - Yellow badge (bg-yellow-100)
- 🟢 **Confirmed** - Green badge (bg-green-100) + Cancel button visible
- 🟣 **Completed** - Purple badge (bg-purple-100)
- 🔴 **Cancelled** - Red badge (bg-red-100)

**Cancel Button Styling:**
- Red text color (text-red-600)
- Hover: Light red background (hover:bg-red-50)
- Rounded corners
- Smooth transitions

### Backend Integration

**API Endpoint Used:**
- `PUT /api/appointments/{id}`
- Request body: `{ "status": "Cancelled" }`
- Already implemented in app.py (lines 8548-8602)

**Status Update:**
- Changes appointment status from 'Confirmed' to 'Cancelled'
- Updates `updated_at` timestamp
- Returns success response with updated appointment data

### User Experience

**Before Cancellation:**
```
┌─────────────────────────────────────────┐
│ 👤 John Doe                             │
│ 10:00 AM - General Checkup             │
│                    [Confirmed] [❌]     │
└─────────────────────────────────────────┘
```

**After Cancellation:**
```
┌─────────────────────────────────────────┐
│ 👤 John Doe                             │
│ 10:00 AM - General Checkup             │
│                    [Cancelled]          │
└─────────────────────────────────────────┘
```

### Technical Implementation

**Frontend Function:**
```javascript
async cancelAppointment(appointmentId) {
    if (!confirm('Are you sure you want to cancel this appointment?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/appointments/${appointmentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: 'Cancelled' })
        });
        
        if (response.ok) {
            alert('Appointment cancelled successfully!');
            await this.loadAppointments();
            // Refresh feather icons
            setTimeout(() => {
                if (typeof feather !== 'undefined') {
                    feather.replace();
                }
            }, 100);
        } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Failed to cancel appointment'));
        }
    } catch (error) {
        console.error('Error cancelling appointment:', error);
        alert('Failed to cancel appointment. Please try again.');
    }
}
```

**HTML Button:**
```html
<button x-show="appointment.status === 'Confirmed'" 
        @click="cancelAppointment(appointment.id)"
        class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        title="Cancel Appointment">
    <i data-feather="x-circle" class="w-4 h-4"></i>
</button>
```

## Business Rules

### 3-Day Cancellation Policy

**Policy Rule:**
Students can only cancel appointments that are **3 or more days away** from today.

### When Can Students Cancel?

✅ **Can Cancel:**
- Appointments with status = 'Confirmed'
- Appointments that are **3+ days in the future**
- Example: Today is Oct 21 → Can cancel appointments on Oct 24 or later

❌ **Cannot Cancel:**
- Appointments within 3 days (Oct 21, 22, 23 if today is Oct 21)
- Today's appointments
- Tomorrow's appointments
- Completed appointments (status = 'Completed')
- Already cancelled appointments (status = 'Cancelled')
- Pending requests (these are not appointments yet)

### Cancellation Policy Examples

**Today: October 21, 2025**

| Appointment Date | Days Away | Can Cancel? | Reason |
|-----------------|-----------|-------------|---------|
| Oct 21 (Today) | 0 days | ❌ No | Within 3 days |
| Oct 22 (Tomorrow) | 1 day | ❌ No | Within 3 days |
| Oct 23 | 2 days | ❌ No | Within 3 days |
| Oct 24 | 3 days | ✅ Yes | Exactly 3 days |
| Oct 25 | 4 days | ✅ Yes | More than 3 days |
| Oct 30 | 9 days | ✅ Yes | More than 3 days |

### Automatic Behavior

**After Cancellation:**
1. Appointment remains in the database
2. Status changes to 'Cancelled'
3. Appointment still visible in student's history
4. Time slot becomes available for other students
5. Staff can see cancelled appointments in their view

**No Deletion:**
- Appointments are NOT deleted from database
- Maintains appointment history
- Allows for reporting and analytics
- Staff can track cancellation patterns

## Use Cases

### Use Case 1: Student Cancels Due to Schedule Conflict (Valid)
**Scenario:** Student has appointment on Oct 30, today is Oct 21 (9 days away)
1. Student opens appointment page
2. Finds confirmed appointment for Oct 30
3. Sees red cancel button (✅ allowed - 9 days away)
4. Clicks cancel button
5. Confirms cancellation
6. Appointment marked as cancelled
7. Time slot freed for others

### Use Case 2: Student Tries to Cancel Last-Minute (Blocked)
**Scenario:** Student has appointment tomorrow, today is Oct 21
1. Student opens appointment page
2. Finds confirmed appointment for Oct 22
3. Sees gray info icon (ℹ️) instead of cancel button
4. Hovers over icon: "Cannot cancel - appointment is within 3 days"
5. Tries to cancel anyway → Policy message appears
6. **Message:** "You can only cancel appointments that are 3 or more days away. Your appointment is on Oct 22 (1 day from now). Please contact the clinic directly."
7. Student must call/visit clinic to cancel

### Use Case 3: Accidental Booking (Within Policy)
**Scenario:** Student booked wrong date/time for Oct 30, today is Oct 21
1. Student immediately sees mistake
2. Appointment is 9 days away (within policy)
3. Cancels wrong appointment successfully
4. Books correct appointment
5. No staff intervention needed

## Benefits

✅ **Student Autonomy** - Students can manage their own appointments (with policy limits)
✅ **Reduced No-Shows** - Students cancel instead of not showing up
✅ **Time Slot Availability** - Cancelled slots become available immediately
✅ **No Staff Burden** - No need for staff to manually cancel (for advance cancellations)
✅ **Appointment History** - Cancelled appointments tracked for records
✅ **User-Friendly** - Simple one-click cancellation with confirmation
✅ **3-Day Policy** - Prevents last-minute cancellations that waste clinic resources
✅ **Fair to Others** - Gives clinic time to offer slots to other students
✅ **Professional Standard** - Follows medical appointment best practices

## Error Handling

**Network Error:**
```
Failed to cancel appointment. Please try again.
```

**API Error:**
```
Error: [specific error message from server]
```

**Appointment Not Found:**
```
Error: Appointment not found
```

**3-Day Policy Violation:**
```
❌ Cancellation Policy:

You can only cancel appointments that are 3 or more days away.

Your appointment is on [date] (X day(s) from now).

Please contact the clinic directly if you need to cancel.
```

## Future Enhancements (Optional)

### Potential Improvements:
1. **Cancellation Reason** - Ask why student is cancelling
2. **Reschedule Option** - Offer to reschedule instead of just cancel
3. **Cancellation Deadline** - Prevent cancellation within X hours of appointment
4. **Email Notification** - Send confirmation email when cancelled
5. **Cancellation Limit** - Track excessive cancellations
6. **Undo Cancellation** - Allow reverting cancellation within time window

## Testing Checklist

- [ ] Cancel button appears only for Confirmed appointments
- [ ] Confirmation dialog shows before cancelling
- [ ] Appointment status changes to Cancelled after confirmation
- [ ] Appointments list refreshes automatically
- [ ] Cancelled appointment shows red badge
- [ ] Cancel button disappears after cancellation
- [ ] Time slot becomes available for other students
- [ ] Staff can see cancelled appointments
- [ ] Error messages display correctly
- [ ] Network errors handled gracefully

## Date Implemented
October 21, 2025

## Status
✅ **ACTIVE** - Cancel appointment feature is now live for students

## Related Features
- Automatic Appointment Approval (AUTOMATIC_APPOINTMENT_APPROVAL.md)
- Real-time Appointment Blocking (REALTIME_APPOINTMENT_BLOCKING.md)
- Auto-Complete Appointments (AUTO_COMPLETE_APPOINTMENTS.md)

## Notes
- Backend API endpoint already existed, only frontend implementation was needed
- Cancel button uses Feather Icons (x-circle)
- Cancellation is immediate and permanent (no undo)
- Cancelled appointments remain in database for record-keeping
- Students can view their cancelled appointments in history
