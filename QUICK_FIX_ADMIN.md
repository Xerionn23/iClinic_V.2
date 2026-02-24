# ⚡ QUICK FIX - Admin Account

## 🎯 I-run Mo Lang To sa phpMyAdmin:

```sql
UPDATE users 
SET role = 'admin',
    position = 'System Admin'
WHERE user_id = 'ADMIN-002';
```

## ✅ Tapos Na!

**Login ulit:**
- User ID: `ADMIN-002`
- Password: (yung password mo)

**Expected Result:**
- Role: `admin` ✅
- Position: `System Admin` ✅
- Redirect: Admin Dashboard ✅

---

## 📋 Verification Query:

```sql
SELECT user_id, email, role, position 
FROM users 
WHERE user_id = 'ADMIN-002';
```

**Should show:**
```
user_id: ADMIN-002
role: admin
position: System Admin
```

---

## 🔧 Code Fixed:

Lahat ng **BAGONG admin accounts** from now on:
- ✅ Automatic `role = 'admin'`
- ✅ Automatic `position = 'System Admin'`
- ✅ Automatic `user_id` populated

**Your existing account**: Kailangan mo pa i-update gamit yung SQL command sa taas.

---

**RUN SQL → LOGIN → DONE! 🚀**
