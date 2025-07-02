# 🔐 Secure File Sharing API

A secure REST API built with Python for controlled file sharing between two types of users: **Operations Users** and **Client Users**.

---

## 🚀 Features

### ✅ Ops User
- Login
- Upload `.pptx`, `.docx`, and `.xlsx` files (only allowed types)

### ✅ Client User
- Sign Up (returns secure, encrypted download URL)
- Email Verification
- Login
- List all uploaded files
- Download file using encrypted URL (access restricted to Client Users)

---

## ⚙️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (can switch to PostgreSQL)
- **Email**: SMTP with `smtplib`
- **Testing**: Pytest
- **Encryption**: Fernet (from `cryptography`)

---

## 🧪 Run Tests

```bash
pytest app/tests/test_encryption.py

