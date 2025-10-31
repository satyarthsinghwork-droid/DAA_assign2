# 📘 Faculty Allocation Dashboard

A **Streamlit web application** that automates the allocation of students to faculty members based on their CGPA and preference rankings.  
The system helps departments efficiently assign faculty advisors or project supervisors while also visualizing allocation statistics and student preferences.

---

## 🚀 Features

✅ **Upload Student Data** — Import student records and preference rankings via CSV.  
✅ **Automated Allocation** — Assigns students to faculties in a round-robin fashion sorted by CGPA.  
✅ **Preference Summary** — Generates an overview of student preferences per faculty.  
✅ **Interactive Dashboard** — Displays allocations, summaries, charts, and metrics.  
✅ **Logging System** — All actions and errors are recorded in `allocation.log`.  
✅ **Downloadable Reports** — Export both allocation and preference summaries as CSV files.

---

## 🧮 Example CSV Format

Your uploaded CSV should include these columns:

| Roll | Name | Email | CGPA | Faculty_A | Faculty_B | Faculty_C |
|------|------|--------|-------|------------|------------|------------|
| 101  | John Doe | john@example.com | 9.1 | 1 | 2 | 3 |
| 102  | Jane Smith | jane@example.com | 8.7 | 2 | 1 | 3 |
| 103  | Alex Kim | alex@example.com | 9.0 | 3 | 2 | 1 |

**Required Columns:**
- `Roll`, `Name`, `Email`, `CGPA`
- One or more faculty preference columns (e.g. `Faculty_A`, `Faculty_B`, ...)

---

## 🧠 How It Works

1. **Upload** your CSV file containing student preferences.  
2. **System sorts** students by CGPA in descending order.  
3. **Sequential allocation** (round-robin) assigns each student to a faculty.  
4. **Preference summary** is generated to show how many students ranked each faculty as top choices.  
5. **Visual dashboard** displays:
   - Allocation table
   - Preference summary table
   - Faculty assignment chart
   - Key metrics (total students, faculties, average CGPA)

---

## 💻 Local Setup (Without Docker)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/faculty-allocation-dashboard.git
cd faculty-allocation-dashboard
