"""
Database Initialization Script for RCMB MOB AI
Regional College of Management Bangalore
Exclusively MBA & PGDM Programs
Includes Official PGDM 2026 1st Semester Timetable & Requested Demo Accounts:
- Student: Satish
- Faculty: Prof. Tapas Panda / Dr. Ashim
- CEO / Director: Dr. S R Mandal (JAY MANDOL)
"""
import sqlite3
import hashlib
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "rcmb.db")

def hash_pw(password: str) -> str:
    return hashlib.sha256(f"rcmb_salt_{password}".encode("utf-8")).hexdigest()

def init_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        mobile TEXT NOT NULL,
        program TEXT NOT NULL, -- Strictly 'MBA' or 'PGDM'
        section TEXT DEFAULT 'Section A',
        semester TEXT DEFAULT '1st Semester',
        role TEXT NOT NULL DEFAULT 'student', -- 'student', 'faculty', 'ceo'
        password_hash TEXT NOT NULL,
        avatar_initials TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create Timetables Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program TEXT NOT NULL, -- 'MBA' or 'PGDM'
        day_of_week TEXT NOT NULL, -- 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
        slot_code TEXT NOT NULL, -- 'S1', 'S2', 'Break', 'S3', 'S4', 'Lunch', 'S5', 'S6', 'S7'
        time_slot TEXT NOT NULL,
        subject TEXT NOT NULL,
        faculty TEXT NOT NULL,
        room TEXT NOT NULL,
        is_break INTEGER DEFAULT 0
    )
    """)

    # Create Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        subject TEXT NOT NULL,
        total_classes INTEGER NOT NULL,
        attended_classes INTEGER NOT NULL,
        percentage REAL NOT NULL
    )
    """)

    # Create Daily Attendance Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        date TEXT NOT NULL,
        subject TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    # Create Assignments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program TEXT NOT NULL,
        subject TEXT NOT NULL,
        title TEXT NOT NULL,
        due_date TEXT NOT NULL,
        faculty TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # Create Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        content TEXT NOT NULL,
        audience TEXT NOT NULL
    )
    """)

    # Create Campus Events Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        venue TEXT NOT NULL,
        description TEXT NOT NULL
    )
    """)

    conn.commit()

    # Clear existing seed data
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM timetables")
    cursor.execute("DELETE FROM attendance")
    cursor.execute("DELETE FROM attendance_logs")
    cursor.execute("DELETE FROM assignments")
    cursor.execute("DELETE FROM notifications")
    cursor.execute("DELETE FROM events")

    # Seed Requested Demo Accounts
    seed_users = [
        # Student Demo: Satish
        (
            "satish@rcmb.edu.in",
            "Satish Kumar",
            "+91 98765 12345",
            "PGDM",
            "Section A",
            "1st Semester",
            "student",
            hash_pw("rcmb2026"),
            "SK"
        ),
        # Student Demo: Priya Verma (MBA)
        (
            "priya.verma@rcmb.edu.in",
            "Priya Verma",
            "+91 98765 43210",
            "MBA",
            "Section A",
            "1st Semester",
            "student",
            hash_pw("rcmb2026"),
            "PV"
        ),
        # Faculty Demo 1: Prof. Tapas Panda
        (
            "tapas.panda@rcmb.edu.in",
            "Prof. Tapas Panda",
            "+91 94480 77889",
            "PGDM",
            "Faculty Wing",
            "Professor",
            "faculty",
            hash_pw("rcmb2026"),
            "TP"
        ),
        # Faculty Demo 2: Dr. Ashim
        (
            "ashim@rcmb.edu.in",
            "Dr. Ashim (AI & Analytics)",
            "+91 94480 33445",
            "PGDM",
            "AI & Tech Lab",
            "Associate Professor",
            "faculty",
            hash_pw("rcmb2026"),
            "DA"
        ),
        # CEO / Director Demo: Dr. S R Mandal (JAY MANDOL)
        (
            "jay.mandal@rcmb.edu.in",
            "Dr. S R Mandal (Jay Mandal)",
            "+91 98800 99887",
            "PGDM",
            "Executive Boardroom",
            "Founder - Director & CEO",
            "ceo",
            hash_pw("rcmb2026"),
            "JM"
        )
    ]
    cursor.executemany("""
    INSERT INTO users (email, full_name, mobile, program, section, semester, role, password_hash, avatar_initials)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, seed_users)

    # Seed Official PGDM 2026 1st Semester Timetable (From the uploaded official document)
    pgdm_official = [
        # Monday
        ("PGDM", "Monday", "S1", "09:30 - 10:25", "STATISTICS FOR MANAGEMENT", "Prof. Smitha", "Amphitheatre Hall A", 0),
        ("PGDM", "Monday", "S2", "10:25 - 11:20", "ECONOMICS FOR MANAGERS", "Prof. Amitabha", "Amphitheatre Hall A", 0),
        ("PGDM", "Monday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("PGDM", "Monday", "S3", "11:40 - 12:35", "ACCOUNTING FOR MANAGERS", "Prof. Sourish", "Amphitheatre Hall A", 0),
        ("PGDM", "Monday", "S4", "12:35 - 01:30", "MARKETING FOR CUSTOMER VALUE", "Dr. Biswas", "Amphitheatre Hall A", 0),
        ("PGDM", "Monday", "Lunch", "01:30 - 02:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("PGDM", "Monday", "S5", "02:30 - 03:25", "STATISTICS FOR MANAGEMENT", "Prof. Amitabha", "Amphitheatre Hall A", 0),
        ("PGDM", "Monday", "S6", "03:25 - 04:20", "Open Slot (Self Study / Library)", "Faculty Guided", "Central Library", 0),
        ("PGDM", "Monday", "S7", "04:20 - 05:30", "Extracurricular / Subject Clinic", "Academic Mentors", "Seminar Hall", 0),

        # Tuesday
        ("PGDM", "Tuesday", "S1", "09:30 - 10:25", "BUSINESS ENVIRONMENTAL LAW", "Prof. Nayana", "Amphitheatre Hall A", 0),
        ("PGDM", "Tuesday", "S2", "10:25 - 11:20", "ACCOUNTING FOR MANAGERS", "Prof. Sourish", "Amphitheatre Hall A", 0),
        ("PGDM", "Tuesday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("PGDM", "Tuesday", "S3", "11:40 - 12:35", "COMMUNICATION SKILLS", "Prof. Tapas", "Amphitheatre Hall A", 0),
        ("PGDM", "Tuesday", "S4", "12:35 - 01:30", "MARKETING FOR CUSTOMER VALUE", "Dr. Biswas", "Amphitheatre Hall A", 0),
        ("PGDM", "Tuesday", "Lunch", "01:30 - 02:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("PGDM", "Tuesday", "S5", "02:30 - 03:25", "ORGANIZATIONAL BEHAVIOUR", "Prof. Reddy", "Amphitheatre Hall A", 0),
        ("PGDM", "Tuesday", "S6", "03:25 - 04:20", "Aptitude & Placement Training", "Placement Cell", "Auditorium", 0),
        ("PGDM", "Tuesday", "S7", "04:20 - 05:30", "Extracurricular / Subject Clinic", "Academic Mentors", "Seminar Hall", 0),

        # Wednesday
        ("PGDM", "Wednesday", "S1", "09:30 - 10:25", "COMMUNICATION SKILLS", "Prof. Tapas", "Amphitheatre Hall A", 0),
        ("PGDM", "Wednesday", "S2", "10:25 - 11:20", "MARKETING FOR CUSTOMER VALUE", "Dr. Aditi", "Amphitheatre Hall A", 0),
        ("PGDM", "Wednesday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("PGDM", "Wednesday", "S3", "11:40 - 12:35", "STATISTICS FOR MANAGEMENT", "Prof. Smitha", "Amphitheatre Hall A", 0),
        ("PGDM", "Wednesday", "S4", "12:35 - 01:30", "ECONOMICS FOR MANAGERS", "Prof. Amitabha", "Amphitheatre Hall A", 0),
        ("PGDM", "Wednesday", "Lunch", "01:30 - 02:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("PGDM", "Wednesday", "S5", "02:30 - 03:25", "ORGANIZATIONAL BEHAVIOUR", "Prof. Tapas", "Amphitheatre Hall A", 0),
        ("PGDM", "Wednesday", "S6", "03:25 - 04:20", "Open Slot (Self Study / Case Analysis)", "Faculty Guided", "Central Library", 0),
        ("PGDM", "Wednesday", "S7", "04:20 - 05:30", "Extracurricular / Subject Clinic", "Academic Mentors", "Seminar Hall", 0),

        # Thursday
        ("PGDM", "Thursday", "S1", "09:30 - 10:25", "ORGANIZATIONAL BEHAVIOUR", "Prof. Tapas", "Amphitheatre Hall A", 0),
        ("PGDM", "Thursday", "S2", "10:25 - 11:20", "ECONOMICS FOR MANAGERS", "Prof. Amitabha", "Amphitheatre Hall A", 0),
        ("PGDM", "Thursday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("PGDM", "Thursday", "S3", "11:40 - 12:35", "BUSINESS ENVIRONMENTAL LAW", "Prof. Kamal", "Amphitheatre Hall A", 0),
        ("PGDM", "Thursday", "S4", "12:35 - 01:30", "STATISTICS FOR MANAGEMENT", "Prof. Amitabha", "Amphitheatre Hall A", 0),
        ("PGDM", "Thursday", "Lunch", "01:30 - 02:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("PGDM", "Thursday", "S5", "02:30 - 03:25", "ACCOUNTING FOR MANAGERS", "Prof. Sourish", "Amphitheatre Hall A", 0),
        ("PGDM", "Thursday", "S6", "03:25 - 04:20", "Aptitude & Logical Reasoning", "Placement Cell", "Auditorium", 0),
        ("PGDM", "Thursday", "S7", "04:20 - 05:30", "Extracurricular / Subject Clinic", "Academic Mentors", "Seminar Hall", 0),

        # Friday
        ("PGDM", "Friday", "S1", "09:30 - 10:25", "ECONOMICS FOR MANAGERS", "Prof. Amitabha", "Amphitheatre Hall A", 0),
        ("PGDM", "Friday", "S2", "10:25 - 11:20", "ACCOUNTING FOR MANAGERS", "Prof. Sourish", "Amphitheatre Hall A", 0),
        ("PGDM", "Friday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("PGDM", "Friday", "S3", "11:40 - 12:35", "AI & ITS APPLICATIONS", "Dr. Ashim", "Advanced Tech Lab", 0),
        ("PGDM", "Friday", "Lunch", "12:35 - 01:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("PGDM", "Friday", "S4", "01:30 - 02:30", "MARKETING FOR CUSTOMER VALUE", "Dr. Aditi", "Amphitheatre Hall A", 0),
        ("PGDM", "Friday", "S5", "02:30 - 03:25", "Open Slot (Self Study / Digital Lab)", "Lab Faculty", "Tech Lab", 0),
        ("PGDM", "Friday", "S6", "03:25 - 04:20", "MENTORSHIP", "Faculty Mentors", "Conference Room", 0),
        ("PGDM", "Friday", "S7", "04:20 - 05:30", "MENTORSHIP", "Faculty Mentors", "Conference Room", 0),

        # Saturday
        ("PGDM", "Saturday", "S1", "09:30 - 11:30", "Global Business Simulation Competition", "Senior Academic Panel", "Main Auditorium", 0),
        ("PGDM", "Saturday", "S2", "11:45 - 01:15", "Executive Placement & Corporate Mock Interviews", "Corporate Relations Team", "Seminar Hall", 0),
        ("PGDM", "Saturday", "S3", "01:45 - 03:30", "Management Clubs & E-Cell Activities", "Student Council", "Innovation Hub", 0)
    ]
    cursor.executemany("""
    INSERT INTO timetables (program, day_of_week, slot_code, time_slot, subject, faculty, room, is_break)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, pgdm_official)

    # Seed MBA Timetable
    mba_official = [
        # Monday
        ("MBA", "Monday", "S1", "09:30 - 10:25", "STATISTICS FOR MANAGEMENT", "Prof. Smitha", "Executive Room 201", 0),
        ("MBA", "Monday", "S2", "10:25 - 11:20", "ECONOMICS FOR MANAGERS", "Prof. Amitabha", "Executive Room 201", 0),
        ("MBA", "Monday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("MBA", "Monday", "S3", "11:40 - 12:35", "ACCOUNTING FOR MANAGERS", "Prof. Sourish", "Executive Room 201", 0),
        ("MBA", "Monday", "S4", "12:35 - 01:30", "MARKETING FOR CUSTOMER VALUE", "Dr. Biswas", "Executive Room 201", 0),
        ("MBA", "Monday", "Lunch", "01:30 - 02:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("MBA", "Monday", "S5", "02:30 - 03:25", "STATISTICS FOR MANAGEMENT", "Prof. Amitabha", "Executive Room 201", 0),
        ("MBA", "Monday", "S6", "03:25 - 04:20", "Open Slot (Self Study)", "Faculty Guided", "Central Library", 0),
        ("MBA", "Monday", "S7", "04:20 - 05:30", "Subject Clinic & Remedial", "Academic Mentors", "Seminar Hall", 0),

        # Tuesday
        ("MBA", "Tuesday", "S1", "09:30 - 10:25", "BUSINESS ENVIRONMENTAL LAW", "Prof. Nayana", "Executive Room 201", 0),
        ("MBA", "Tuesday", "S2", "10:25 - 11:20", "ACCOUNTING FOR MANAGERS", "Prof. Sourish", "Executive Room 201", 0),
        ("MBA", "Tuesday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("MBA", "Tuesday", "S3", "11:40 - 12:35", "COMMUNICATION SKILLS", "Prof. Tapas", "Executive Room 201", 0),
        ("MBA", "Tuesday", "S4", "12:35 - 01:30", "MARKETING FOR CUSTOMER VALUE", "Dr. Biswas", "Executive Room 201", 0),
        ("MBA", "Tuesday", "Lunch", "01:30 - 02:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("MBA", "Tuesday", "S5", "02:30 - 03:25", "ORGANIZATIONAL BEHAVIOUR", "Prof. Reddy", "Executive Room 201", 0),
        ("MBA", "Tuesday", "S6", "03:25 - 04:20", "Aptitude Skills", "Placement Cell", "Auditorium", 0),
        ("MBA", "Tuesday", "S7", "04:20 - 05:30", "Extracurricular / Subject Clinic", "Academic Mentors", "Seminar Hall", 0),

        # Wednesday
        ("MBA", "Wednesday", "S1", "09:30 - 10:25", "COMMUNICATION SKILLS", "Prof. Tapas", "Executive Room 201", 0),
        ("MBA", "Wednesday", "S2", "10:25 - 11:20", "MARKETING FOR CUSTOMER VALUE", "Dr. Aditi", "Executive Room 201", 0),
        ("MBA", "Wednesday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("MBA", "Wednesday", "S3", "11:40 - 12:35", "STATISTICS FOR MANAGEMENT", "Prof. Smitha", "Executive Room 201", 0),
        ("MBA", "Wednesday", "S4", "12:35 - 01:30", "ECONOMICS FOR MANAGERS", "Prof. Amitabha", "Executive Room 201", 0),
        ("MBA", "Wednesday", "Lunch", "01:30 - 02:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("MBA", "Wednesday", "S5", "02:30 - 03:25", "ORGANIZATIONAL BEHAVIOUR", "Prof. Tapas", "Executive Room 201", 0),
        ("MBA", "Wednesday", "S6", "03:25 - 04:20", "Open Slot (Self Study)", "Faculty Guided", "Central Library", 0),
        ("MBA", "Wednesday", "S7", "04:20 - 05:30", "Subject Clinic", "Academic Mentors", "Seminar Hall", 0),

        # Thursday
        ("MBA", "Thursday", "S1", "09:30 - 10:25", "ORGANIZATIONAL BEHAVIOUR", "Prof. Tapas", "Executive Room 201", 0),
        ("MBA", "Thursday", "S2", "10:25 - 11:20", "ECONOMICS FOR MANAGERS", "Prof. Amitabha", "Executive Room 201", 0),
        ("MBA", "Thursday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("MBA", "Thursday", "S3", "11:40 - 12:35", "BUSINESS ENVIRONMENTAL LAW", "Prof. Kamal", "Executive Room 201", 0),
        ("MBA", "Thursday", "S4", "12:35 - 01:30", "STATISTICS FOR MANAGEMENT", "Prof. Amitabha", "Executive Room 201", 0),
        ("MBA", "Thursday", "Lunch", "01:30 - 02:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("MBA", "Thursday", "S5", "02:30 - 03:25", "ACCOUNTING FOR MANAGERS", "Prof. Sourish", "Executive Room 201", 0),
        ("MBA", "Thursday", "S6", "03:25 - 04:20", "Aptitude Skills", "Placement Cell", "Auditorium", 0),
        ("MBA", "Thursday", "S7", "04:20 - 05:30", "Subject Clinic", "Academic Mentors", "Seminar Hall", 0),

        # Friday
        ("MBA", "Friday", "S1", "09:30 - 10:25", "ECONOMICS FOR MANAGERS", "Prof. Amitabha", "Executive Room 201", 0),
        ("MBA", "Friday", "S2", "10:25 - 11:20", "ACCOUNTING FOR MANAGERS", "Prof. Sourish", "Executive Room 201", 0),
        ("MBA", "Friday", "Break", "11:20 - 11:40", "Mini Break", "Campus Cafeteria", "Student Lounge", 1),
        ("MBA", "Friday", "S3", "11:40 - 12:35", "AI & ITS APPLICATIONS", "Dr. Ashim", "Advanced Tech Lab", 0),
        ("MBA", "Friday", "Lunch", "12:35 - 01:30", "Lunch Break", "Campus Dining Hall", "Dining Hall", 1),
        ("MBA", "Friday", "S4", "01:30 - 02:30", "MARKETING FOR CUSTOMER VALUE", "Dr. Aditi", "Executive Room 201", 0),
        ("MBA", "Friday", "S5", "02:30 - 03:25", "Open Slot (Case Analysis)", "Lab Faculty", "Tech Lab", 0),
        ("MBA", "Friday", "S6", "03:25 - 04:20", "MENTORSHIP", "Faculty Mentors", "Conference Room", 0),
        ("MBA", "Friday", "S7", "04:20 - 05:30", "MENTORSHIP", "Faculty Mentors", "Conference Room", 0),

        # Saturday
        ("MBA", "Saturday", "S1", "09:30 - 11:30", "Harvard Business Case Study Analysis", "Combined Academic Panel", "Main Auditorium", 0),
        ("MBA", "Saturday", "S2", "11:45 - 01:15", "Corporate Placement & Aptitude Workshop", "Placement Cell", "Seminar Hall", 0),
        ("MBA", "Saturday", "S3", "01:45 - 03:30", "Management Clubs & Peer Learning", "Student Council", "Student Center", 0)
    ]
    cursor.executemany("""
    INSERT INTO timetables (program, day_of_week, slot_code, time_slot, subject, faculty, room, is_break)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, mba_official)

    # Seed Sample Attendance for Satish (PGDM) and Priya (MBA)
    seed_attendance = [
        # Satish Kumar (PGDM)
        ("satish@rcmb.edu.in", "STATISTICS FOR MANAGEMENT", 24, 23, 95.8),
        ("satish@rcmb.edu.in", "ECONOMICS FOR MANAGERS", 24, 22, 91.6),
        ("satish@rcmb.edu.in", "ACCOUNTING FOR MANAGERS", 22, 21, 95.4),
        ("satish@rcmb.edu.in", "MARKETING FOR CUSTOMER VALUE", 24, 22, 91.6),
        ("satish@rcmb.edu.in", "COMMUNICATION SKILLS (Prof. Tapas)", 20, 19, 95.0),
        ("satish@rcmb.edu.in", "ORGANIZATIONAL BEHAVIOUR", 22, 20, 90.9),
        ("satish@rcmb.edu.in", "AI & ITS APPLICATIONS (Dr. Ashim)", 18, 17, 94.4),

        # Priya Verma (MBA)
        ("priya.verma@rcmb.edu.in", "STATISTICS FOR MANAGEMENT", 24, 22, 91.6),
        ("priya.verma@rcmb.edu.in", "ECONOMICS FOR MANAGERS", 24, 21, 87.5),
        ("priya.verma@rcmb.edu.in", "ACCOUNTING FOR MANAGERS", 20, 18, 90.0),
        ("priya.verma@rcmb.edu.in", "MARKETING FOR CUSTOMER VALUE", 22, 19, 86.3),
        ("priya.verma@rcmb.edu.in", "COMMUNICATION SKILLS", 18, 16, 88.8)
    ]
    cursor.executemany("""
    INSERT INTO attendance (user_email, subject, total_classes, attended_classes, percentage)
    VALUES (?, ?, ?, ?, ?)
    """, seed_attendance)

    # Seed Sample Daily Attendance Logs
    sample_dates = ["2026-11-02", "2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06"]
    for email in ["satish@rcmb.edu.in", "priya.verma@rcmb.edu.in"]:
        for d in sample_dates:
            cursor.execute("""
            INSERT INTO attendance_logs (user_email, date, subject, status)
            VALUES (?, ?, 'Core PGDM Lecture Session', 'Present')
            """, (email, d))

    # Seed Assignments
    seed_assignments = [
        ("PGDM", "COMMUNICATION SKILLS", "Executive Oral Pitch & Boardroom Presentation Mastery", "2026-11-15", "Prof. Tapas Panda", "Pending"),
        ("PGDM", "AI & ITS APPLICATIONS", "Predictive Analytics & Machine Learning Models in Business", "2026-11-18", "Dr. Ashim", "Pending"),
        ("PGDM", "STATISTICS FOR MANAGEMENT", "Hypothesis Testing & Regression Diagnostics", "2026-11-20", "Prof. Smitha", "Submitted"),
        ("PGDM", "ECONOMICS FOR MANAGERS", "Monetary Policy & Inflation Impacts on FMCG Sector", "2026-11-22", "Prof. Amitabha", "Pending"),
        ("MBA", "MARKETING FOR CUSTOMER VALUE", "Brand Audit & Consumer Journey Case Analysis", "2026-11-15", "Dr. Biswas", "Pending"),
        ("MBA", "ACCOUNTING FOR MANAGERS", "Comparative Ratio Analysis of 3 NIFTY 50 Companies", "2026-11-20", "Prof. Sourish", "Submitted")
    ]
    cursor.executemany("""
    INSERT INTO assignments (program, subject, title, due_date, faculty, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, seed_assignments)

    # Seed Notifications
    seed_notifications = [
        ("Official PGDM 2026 1st Semester Timetable Released", "Academic", "08 Nov 2026", "The official 1st semester timetable is now active across all lecture halls. Download the PDF copy from the portal.", "All"),
        ("Outlook Magazine Features Founder - Director Dr. S R Mandal", "Leadership", "07 Nov 2026", "Outlook Magazine spotlight: Founder - Director RCMB, Dr. S R Mandal emphasises on Inclusive Education System Rooted in Equality and Diversity.", "All"),
        ("AI & Python Lab Workshop with Dr. Ashim", "Academic", "06 Nov 2026", "Hands-on machine learning session scheduled for this Friday in the Advanced Tech Lab.", "All"),
        ("Communication Skills Clinic by Prof. Tapas Panda", "Skill Development", "05 Nov 2026", "Special evening subject clinic on public speaking and corporate GD techniques from 4:20 PM in the Seminar Hall.", "All")
    ]
    cursor.executemany("""
    INSERT INTO notifications (title, category, date, content, audience)
    VALUES (?, ?, ?, ?, ?)
    """, seed_notifications)

    # Seed Events
    seed_events = [
        ("Founder's Leadership Address - Dr. S R Mandal", "2026-11-18", "10:30 AM - 12:00 PM", "Main Auditorium", "Keynote address by Founder-Director Dr. S R Mandal on inclusive leadership and the 2026-27 strategic vision."),
        ("RCMB National Management Fest 'PRAGYAN 2026'", "2026-11-28", "09:30 AM - 05:00 PM", "Campus Amphitheatre & Grounds", "Inter-college business simulations, case battles, and mock stock challenges."),
        ("Corporate Placement Conclave 2026-27", "2026-12-05", "09:00 AM - 04:30 PM", "Executive Conference Center", "Top hiring partners Deloitte, EY, HDFC, Amazon visiting for on-campus interviews.")
    ]
    cursor.executemany("""
    INSERT INTO events (title, date, time, venue, description)
    VALUES (?, ?, ?, ?, ?)
    """, seed_events)

    conn.commit()
    conn.close()
    print("Database re-seeded successfully with Official PGDM 2026 Timetable and requested demo accounts.")

if __name__ == "__main__":
    init_database()
