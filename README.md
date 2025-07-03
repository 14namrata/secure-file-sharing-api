<<<<<<< HEAD
# 🔐 Secure File Sharing API

📝 This project was developed as part of the EZ Company Backend Internship Assessment (July 2025).


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

=======
# secure-file-sharing-api
>>>>>>> d7e9a75bed772c870ad730071fd454ed6f509282

## 🚀 Deployment Plan

To deploy this API to production, I would:
1. Use **Docker** to containerize the FastAPI application.
2. Set up a **PostgreSQL or MySQL database** for production.
3. Use **Gunicorn with Uvicorn workers** behind **Nginx** for serving FastAPI.
4. Host on a cloud platform like **Render**, **Railway**, **Heroku**, or **AWS EC2**.
5. Configure **domain, HTTPS (SSL)**, and production email via **SendGrid** or Gmail SMTP.
6. Use **environment variables** for all secrets and tokens through a `.env` file or Docker secrets.
