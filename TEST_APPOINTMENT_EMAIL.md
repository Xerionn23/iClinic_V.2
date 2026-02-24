# Quick Test Guide: Appointment Email Notifications

## 🧪 How to Test the 3-Day Email Logic

### Test Scenario 1: Appointment TODAY (Should Send Email ✅)

1. **Login as Student**
   - Go to: `http://127.0.0.1:5000`
   - Login with student credentials

2. **Book Appointment for TODAY**
   - Go to Appointments page
   - Select today's date on calendar
   - Choose any available time slot
   - Fill the form:
     - Patient Name: (auto-filled)
     - Contact: Your phone number
     - Appointment Type: General Checkup
     - Reason: Testing email notification
   - Click "Request Appointment"

3. **Check Console Output**
   ```
   ✅ New appointment auto-confirmed: ID 123 for [Your Name] on 2025-10-28 at 09:00
   📅 Days until appointment: 0
   ⚡ Appointment is within 3 days! Sending email notification...
   📧 Sending appointment notification to: your.email@example.com
   ✅ Email notification sent successfully to: your.email@example.com
   ```

4. **Check Gmail Inbox**
   - Open your Gmail
   - Look for email from: `norzagaraycollege.clinic@gmail.com`
   - Subject: "Appointment Confirmation - iClinic Healthcare"
   - Verify appointment details are correct

---

### Test Scenario 2: Appointment TOMORROW (Should Send Email ✅)

1. **Book Appointment for TOMORROW**
   - Select tomorrow's date on calendar
   - Book appointment with any time slot

2. **Expected Console Output**
   ```
   📅 Days until appointment: 1
   ⚡ Appointment is within 3 days! Sending email notification...
   ✅ Email notification sent successfully
   ```

3. **Expected Result**: Email received ✅

---

### Test Scenario 3: Appointment in 2 DAYS (Should Send Email ✅)

1. **Book Appointment 2 Days from Now**
   - Select date 2 days ahead
   - Book appointment

2. **Expected Console Output**
   ```
   📅 Days until appointment: 2
   ⚡ Appointment is within 3 days! Sending email notification...
   ✅ Email notification sent successfully
   ```

3. **Expected Result**: Email received ✅

---

### Test Scenario 4: Appointment in 3 DAYS (Should NOT Send Email ❌)

1. **Book Appointment 3 Days from Now**
   - Select date 3 days ahead
   - Book appointment

2. **Expected Console Output**
   ```
   📅 Days until appointment: 3
   📆 Appointment is 3 days away (≥3 days). No immediate email notification sent.
   ```

3. **Expected Result**: NO email received ❌ (This is correct!)

---

### Test Scenario 5: Appointment NEXT WEEK (Should NOT Send Email ❌)

1. **Book Appointment 7 Days from Now**
   - Select date 1 week ahead
   - Book appointment

2. **Expected Console Output**
   ```
   📅 Days until appointment: 7
   📆 Appointment is 7 days away (≥3 days). No immediate email notification sent.
   ```

3. **Expected Result**: NO email received ❌ (This is correct!)

---

## 📊 Quick Reference Table

| Days Until Appointment | Email Sent? | Console Message |
|------------------------|-------------|-----------------|
| 0 (Today) | ✅ YES | "⚡ Appointment is within 3 days!" |
| 1 (Tomorrow) | ✅ YES | "⚡ Appointment is within 3 days!" |
| 2 | ✅ YES | "⚡ Appointment is within 3 days!" |
| 3 | ❌ NO | "📆 Appointment is 3 days away (≥3 days)" |
| 4 | ❌ NO | "📆 Appointment is 4 days away (≥3 days)" |
| 5 | ❌ NO | "📆 Appointment is 5 days away (≥3 days)" |
| 7+ | ❌ NO | "📆 Appointment is X days away (≥3 days)" |

---

## 🔍 Troubleshooting

### Email Not Received?

1. **Check Spam Folder**
   - Gmail might filter it as spam initially
   - Mark as "Not Spam" if found

2. **Check Console Logs**
   - Look for "✅ Email notification sent successfully"
   - If you see "❌ Gmail Authentication Failed", check Gmail setup

3. **Verify Student Email**
   - Check database: `students` table → `std_EmailAdd` field
   - Make sure email is valid and correct

4. **Check Gmail App Password**
   - Verify in `app.py` line 3370
   - Should be 16 characters, no spaces
   - See `GMAIL_SETUP_GUIDE.md` for setup

### Wrong Days Calculation?

1. **Check System Date/Time**
   - Make sure your computer's date is correct
   - System uses current date to calculate days

2. **Check Appointment Date**
   - Verify the date you selected on calendar
   - Console shows: "📅 Days until appointment: X"

### Email Sent But Appointment ≥ 3 Days?

1. **Check Console Output**
   - Should show: "📆 Appointment is X days away (≥3 days)"
   - If it shows "⚡ Appointment is within 3 days!", there's a bug

2. **Verify Date Calculation**
   - Check `app.py` line 11138: `days_until_appointment = (appointment_date_obj - today).days`
   - Should be correct

---

## ✅ Success Indicators

### You'll Know It's Working When:

1. **Console shows correct day count**
   ```
   📅 Days until appointment: 1
   ```

2. **Correct email decision**
   - < 3 days: "⚡ Appointment is within 3 days!"
   - ≥ 3 days: "📆 Appointment is X days away"

3. **Email received in Gmail** (for < 3 days only)
   - Professional HTML email
   - Correct appointment details
   - iClinic branding

4. **Appointment still created** (even if email fails)
   - System never fails appointment due to email issues
   - Graceful error handling

---

## 🎯 Quick Test Commands

### Test 1: Book Today's Appointment
```
1. Login as student
2. Go to Appointments
3. Select TODAY
4. Book appointment
5. Check Gmail ✅
```

### Test 2: Book Next Week's Appointment
```
1. Login as student
2. Go to Appointments
3. Select date 7 days ahead
4. Book appointment
5. Should NOT receive email ❌
6. Check console: "📆 Appointment is 7 days away"
```

---

## 📧 Sample Email Preview

When email is sent (< 3 days), student receives:

**Subject**: Appointment Confirmation - iClinic Healthcare

**Content**:
- ✅ Appointment Confirmed header
- 📅 Date: October 28, 2025
- ⏰ Time: 09:00
- 🏥 Type: General Checkup
- ⚠️ Reminder to arrive 10 minutes early
- 📍 Clinic location
- 📞 Rescheduling instructions

---

## 🚀 Ready to Test!

**KAYA MO NA I-TEST!** Just follow the scenarios above and check:
1. Console logs for day calculation
2. Email decision (send or not send)
3. Gmail inbox for received emails

**Remember**: 
- **< 3 days** = Email sent ✅
- **≥ 3 days** = No email ❌

Good luck testing! 🎉
