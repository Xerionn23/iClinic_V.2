# 🚀 QUICK TEST GUIDE - ACCOUNT CREATION & FORGOT PASSWORD
## iClinic Healthcare Management System

**Para sa mabilis na testing ng lahat ng 7 user types**

---

## ✅ ACCOUNT CREATION TESTING

### **1. STUDENT**
```
✓ Go to login page
✓ Click "Create Account" or "Register"
✓ Select Role: Student
✓ Enter ID: 2021-0001
✓ Enter Name: Joseph Flynn
✓ Enter Password: test123
✓ Click Submit

Expected: ✅ "Verification email sent to your registered Gmail"
Check: Email should be sent to student's Gmail from database
```

---

### **2. TEACHING STAFF**
```
✓ Select Role: Teaching Staff
✓ Enter ID: FAC-CS-001
✓ Enter Name: Roberto Lapig
✓ Enter Password: test123
✓ Click Submit

Expected: ✅ "Verification email sent to rlapig@gonzagary.edu.ph"
```

---

### **3. NURSE**
```
✓ Select Role: Nurse
✓ Enter ID: NURSE-001
✓ Enter Name: Green Lloyd Lapig
✓ Enter Password: test123
✓ Click Submit

Expected: ✅ "Verification email sent to llyodlapig@gmail.com"
```

---

### **4. ADMIN**
```
✓ Select Role: Admin
✓ Enter ID: ADMIN-001
✓ Enter Name: System Administrator
✓ Enter Password: test123
✓ Click Submit

Expected: ✅ "Verification email sent to admin@norzagaray.edu.ph"
```

---

### **5. NON-TEACHING STAFF** ⭐ NEWLY FIXED
```
✓ Select Role: Non-Teaching Staff
✓ Enter ID: NTS-001
✓ Enter Name: Maria Santos
✓ Enter Password: test123
✓ Click Submit

Expected: ✅ "Verification email sent to msantos@norzagaray.edu.ph"
Database Check: ✅ Validates against non_teaching_staff table
```

---

### **6. DEANS** ⭐ NEWLY FIXED
```
✓ Select Role: Deans
✓ Enter ID: DEAN-001
✓ Enter Name: Roberto Villanueva
✓ Enter Password: test123
✓ Click Submit

Expected: ✅ "Verification email sent to rvillanueva@norzagaray.edu.ph"
Database Check: ✅ Validates against deans table
```

---

### **7. PRESIDENT** ⭐ NEWLY FIXED
```
✓ Select Role: President
✓ Enter ID: PRES-001
✓ Enter Name: Emilio Aguinaldo
✓ Enter Password: test123
✓ Click Submit

Expected: ✅ "Verification email sent to president@norzagaray.edu.ph"
Database Check: ✅ Validates against president table
```

---

## 🔑 FORGOT PASSWORD TESTING

### **1. STUDENT**
```
✓ Go to login page
✓ Click "Forgot Password?"
✓ Enter User ID: 2021-0001
✓ Click Submit

Expected: ✅ "Password reset link sent to your email"
```

---

### **2. TEACHING STAFF** ⭐ NEWLY FIXED
```
✓ Click "Forgot Password?"
✓ Enter User ID: FAC-CS-001
✓ Click Submit

Expected: ✅ "Password reset link sent to rlapig@gonzagary.edu.ph"
Database Search: ✅ Now searches teaching table by faculty_id
```

---

### **3. NURSE**
```
✓ Click "Forgot Password?"
✓ Enter User ID: NURSE-001
✓ Click Submit

Expected: ✅ "Password reset link sent to llyodlapig@gmail.com"
```

---

### **4. ADMIN**
```
✓ Click "Forgot Password?"
✓ Enter User ID: ADMIN-001
✓ Click Submit

Expected: ✅ "Password reset link sent to admin@norzagaray.edu.ph"
```

---

### **5. NON-TEACHING STAFF** ⭐ NEWLY FIXED
```
✓ Click "Forgot Password?"
✓ Enter User ID: NTS-001
✓ Click Submit

Expected: ✅ "Password reset link sent to msantos@norzagaray.edu.ph"
Database Search: ✅ Now searches non_teaching_staff table by staff_id
```

---

### **6. DEANS** ⭐ NEWLY FIXED
```
✓ Click "Forgot Password?"
✓ Enter User ID: DEAN-001
✓ Click Submit

Expected: ✅ "Password reset link sent to rvillanueva@norzagaray.edu.ph"
Database Search: ✅ Now searches deans table by dean_id
```

---

### **7. PRESIDENT** ⭐ NEWLY FIXED
```
✓ Click "Forgot Password?"
✓ Enter User ID: PRES-001
✓ Click Submit

Expected: ✅ "Password reset link sent to president@norzagaray.edu.ph"
Database Search: ✅ Now searches president table by president_id
```

---

## ❌ ERROR TESTING

### **Invalid ID Number**
```
✓ Enter ID: INVALID-999
✓ Enter Name: Test User
Expected: ❌ "ID not found in database. Please contact HR/Registrar."
```

### **Name Mismatch**
```
✓ Enter ID: NTS-001 (valid)
✓ Enter Name: Wrong Name
Expected: ❌ "Name mismatch. Database shows: Maria Santos"
```

### **Duplicate Email**
```
✓ Try to register with same email twice
Expected: ❌ "Email already registered"
```

### **Forgot Password - No Account**
```
✓ Enter User ID of someone who hasn't created account yet
Expected: ❌ "User ID not found. Please check and try again."
```

---

## 📋 TESTING CHECKLIST

### Account Creation:
- [ ] Student (2021-0001)
- [ ] Teaching Staff (FAC-CS-001) 
- [ ] Nurse (NURSE-001)
- [ ] Admin (ADMIN-001)
- [ ] Non-Teaching Staff (NTS-001) ⭐ NEW
- [ ] Deans (DEAN-001) ⭐ NEW
- [ ] President (PRES-001) ⭐ NEW

### Forgot Password:
- [ ] Student (2021-0001)
- [ ] Teaching Staff (FAC-CS-001) ⭐ NEW
- [ ] Nurse (NURSE-001)
- [ ] Admin (ADMIN-001)
- [ ] Non-Teaching Staff (NTS-001) ⭐ NEW
- [ ] Deans (DEAN-001) ⭐ NEW
- [ ] President (PRES-001) ⭐ NEW

### Error Handling:
- [ ] Invalid ID number
- [ ] Name mismatch
- [ ] Duplicate email
- [ ] Inactive user
- [ ] No user account (forgot password)

---

## 🎯 EXPECTED RESULTS SUMMARY

| User Type | Account Creation | Forgot Password | Status |
|-----------|-----------------|-----------------|--------|
| Student | ✅ Working | ✅ Working | 🟢 READY |
| Teaching Staff | ✅ Working | ✅ **FIXED** | 🟢 READY |
| Nurse | ✅ Working | ✅ Working | 🟢 READY |
| Admin | ✅ Working | ✅ Working | 🟢 READY |
| Non-Teaching Staff | ✅ **FIXED** | ✅ **FIXED** | 🟢 READY |
| Deans | ✅ **FIXED** | ✅ **FIXED** | 🟢 READY |
| President | ✅ **FIXED** | ✅ **FIXED** | 🟢 READY |

---

## 📧 EMAIL VERIFICATION

After registration, check email for:
- ✅ Professional HTML template
- ✅ iClinic branding
- ✅ Verification link
- ✅ 24-hour expiration notice
- ✅ Security instructions

After forgot password, check email for:
- ✅ Password reset link
- ✅ 1-hour expiration notice
- ✅ Security warnings
- ✅ Professional formatting

---

## 🔧 TROUBLESHOOTING

**Email not received?**
- Check spam folder
- Verify Gmail App Password: xtsweijcxsntwhld
- Check console for reset link (testing mode)

**Database error?**
- Ensure all tables exist (run init_db())
- Check sample data is loaded
- Verify database connection

**Name mismatch error?**
- Use exact name from database
- Check capitalization
- Verify ID number is correct

---

**Last Updated:** October 26, 2025, 6:30 PM  
**Status:** 🟢 ALL SYSTEMS GO!
