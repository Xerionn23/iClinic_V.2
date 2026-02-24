# Gmail Email Setup Guide for iClinic

## 🚀 Quick Setup Steps

To enable email sending for account verification, you need to set up a Gmail App Password.

### Step 1: Enable 2-Step Verification

1. Go to your Google Account: https://myaccount.google.com/security
2. Click on **"2-Step Verification"**
3. Follow the steps to enable it (you'll need your phone)

### Step 2: Generate App Password

1. After enabling 2-Step Verification, go back to: https://myaccount.google.com/security
2. Scroll down to **"App passwords"** (under "How you sign in to Google")
3. Click **"App passwords"**
4. Select:
   - **App**: Mail
   - **Device**: Windows Computer (or Other)
5. Click **"Generate"**
6. Copy the **16-character password** (it will look like: `abcd efgh ijkl mnop`)

### Step 3: Update app.py

1. Open `app.py`
2. Find line **2131-2132** (in the `send_verification_email` function)
3. Replace the credentials:

```python
sender_email = "your-gmail@gmail.com"  # Your Gmail address
sender_password = "abcdefghijklmnop"   # Your 16-char App Password (no spaces!)
```

**IMPORTANT**: Remove all spaces from the App Password!
- ❌ Wrong: `"abcd efgh ijkl mnop"`
- ✅ Correct: `"abcdefghijklmnop"`

### Step 4: Test Email Sending

1. Restart your Flask server
2. Try registering a new account
3. Check the terminal/console for email sending logs:
   - ✅ `Email sent successfully to: user@gmail.com`
   - ❌ `Gmail Authentication Failed` (wrong password)

### Step 5: Check Gmail Inbox

1. Open Gmail: https://gmail.com
2. Check the inbox of the email address you registered with
3. Look for email from your iClinic sender email
4. Click the verification link to complete registration

---

## 🔧 Troubleshooting

### "Gmail Authentication Failed"
- Make sure 2-Step Verification is enabled
- Generate a new App Password
- Remove all spaces from the password
- Use the App Password, NOT your regular Gmail password

### "Connection refused" or "Timeout"
- Check your internet connection
- Make sure port 587 is not blocked by firewall
- Try using port 465 with SSL instead

### Email not received
- Check spam/junk folder
- Verify the recipient email is correct
- Check Gmail sending limits (500 emails per day for free accounts)

### Testing without Gmail
The system will still work even if email sending fails. Check the terminal/console for the verification link and copy it manually.

---

## 📧 Current Configuration

**File**: `app.py` (lines 2131-2132)

```python
sender_email = "iclinic.norzagaray@gmail.com"
sender_password = "your-16-char-app-password-here"
```

**SMTP Settings**:
- Server: `smtp.gmail.com`
- Port: `587` (TLS)
- Security: STARTTLS

---

## ✅ Verification

Once properly configured, you should see these logs when registering:

```
📧 Sending verification email to: user@gmail.com
🔗 Verification link: http://127.0.0.1:5000/complete-registration?token=...
📧 Connecting to Gmail SMTP server...
🔐 Logging in with: iclinic.norzagaray@gmail.com
📤 Sending email to: user@gmail.com
✅ Email sent successfully to: user@gmail.com
```

---

## 🔐 Security Notes

- **Never commit** your App Password to Git
- Use environment variables for production
- Rotate App Passwords regularly
- Revoke unused App Passwords from Google Account settings

---

Need help? Contact IT support or check Google's official guide:
https://support.google.com/accounts/answer/185833
