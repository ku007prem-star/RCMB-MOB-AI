# RCMB MOB AI - Official Digital Campus Platform
**Regional College of Management Bangalore (RCMB)**  
*Exclusively for MBA and PGDM Postgraduate Programs*

---

## 🏛️ Project Overview
**RCMB MOB AI** is a modern, unified academic platform and AI assistant built specifically for the **Regional College of Management Bangalore** community. It brings together timetable lookups by day or date, attendance monitoring, academic assignments, campus announcements, and conversational AI support.

---

## ✨ Key Features Implemented

### 1. 🛡️ Official Logo & College Branding
- Integrated the official **RCMB Crest Shield Logo** (`static/images/rcmb-logo.jpg`).
- College Color Palette: Deep Crimson / Maroon (`#8B1D24`, `#A6192E`), warm ivory/cream background (`#FAF7F2`), subtle gold accents, and clean modern typography.

### 2. 🖥️ Landing Page (Matching Previous Replit Design)
- Header with official logo, `RCM BANGALORE`, `RCMB mob AI`, and live academic session status badge.
- Hero Section:
  - Pill badge: `✨ Made for the RCMB community`
  - Headline: `Welcome to RCMB mob AI`
  - Interactive Role Selection cards: **Student**, **Faculty**, and **CEO / Leadership**.
  - Visual collage on the right: **Our Campus**, **Campus Events**, **Student Life**, and floating badge `One connected campus`.

### 3. 📸 Front-Page Showcase of Uploaded Campus Photos
- **Interactive Amphitheatre Classrooms** (`static/images/rcmb-classroom.jpg`): Tiered wooden amphitheater lecture halls designed for case studies and executive debate.
- **Corporate Seminar & CXO Auditorium** (`static/images/rcmb-auditorium.jpg`): Modern auditorium for convocations, guest lectures, and placement sessions.

### 4. 🎓 Exclusively MBA & PGDM Programs
- Per the college curriculum, **only MBA and PGDM** courses are offered.
- Undergraduate courses (BBA, B.Com) are strictly excluded from all forms, databases, filters, and AI responses.

### 5. 🔐 Real Original Authentication System
- **Sign Up / Registration**:
  - Full Legal Name
  - Official / Personal Email ID
  - 10-digit Indian Mobile Number (auto-formatted with `+91`)
  - Course selection: Strictly **MBA** or **PGDM**
  - Section selection (`Section A` / `Section B`)
  - Password creation with confirmation
- **Sign In / Login**:
  - Email + Password verification with SHA-256 secure hashing
  - Session persistence (Flask session + client storage)
  - Profile editing (update mobile number, full name, or password)
- **1-Click Demo Accounts** (for immediate testing):
  - **MBA Student**: `priya.verma@rcmb.edu.in` / `rcmb2026`
  - **PGDM Student**: `arjun.sharma@rcmb.edu.in` / `rcmb2026`
  - **Faculty**: `faculty@rcmb.edu.in` / `rcmb2026`
  - **CEO / Dean**: `ceo@rcmb.edu.in` / `rcmb2026`

### 6. 🤖 English Conversational AI Chatbot with Day & Date Timetable Search
- Understands questions by **day of the week** (Monday to Saturday) or **calendar date** (e.g. `10 Nov`, `2026-11-12`, `today`, `tomorrow`).
- Automatically resolves the day of the week and returns a structured English breakdown:
  - ⏰ **Period & Time Slot** (e.g. 09:30 AM - 10:45 AM)
  - 📚 **Subject** (e.g. Marketing Management, Corporate Valuation)
  - 👨‍🏫 **Faculty / Teacher** (e.g. Dr. Rajesh Sharma, Prof. Meenakshi Sundaram)
  - 🏛️ **Lecture Hall** (e.g. Amphitheatre Hall A, Executive Classroom 201)
  - 💡 **Focus Topic**
- Sunday awareness: Informs students that Sunday is a weekly holiday with library hours.
- Handles attendance inquiries, upcoming assignment deadlines, college timings, bus routes, and campus events.

### 7. 📊 Complete Inner Student Portal
- **Interactive Timetable Explorer**: Program toggle (MBA/PGDM), day tabs, and a calendar date picker.
- **Attendance Tracker**: Percentage meter, conducted vs attended numbers, exam eligibility check, and **Download Attendance CSV** feature.
- **Assignments**: Track pending and submitted coursework.
- **Campus Circulars**: Real-time notices from Dean's Office, Placement Cell, and Exam Department.
- **Life @ RCMB**: Visual photo gallery of campus facilities.

---

## 🚀 Running the Project Locally

1. Open PowerShell or Command Prompt in the project folder:
   ```powershell
   cd "c:\Users\User\Desktop\RCMB Project"
   ```

2. Initialize the database (if not already initialized):
   ```powershell
   python init_db.py
   ```

3. Start the Flask application:
   ```powershell
   python app.py
   ```

4. Open your web browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🌐 1-Click Hosting & Deployment

This project is 100% production-ready and can be hosted on any platform:

### A. Hosting on Render
1. Push this folder to a GitHub repository.
2. In Render Dashboard, click **New Web Service** and connect your repository.
3. Render automatically detects `render.yaml` and starts your app with `gunicorn app:app`.

### B. Hosting on Replit
1. Create a Python Repl and upload the project files.
2. The provided `.replit` configuration runs `python app.py` automatically.

### C. Hosting on Railway / Heroku
- The included `Procfile` (`web: gunicorn app:app`) is automatically recognized.
