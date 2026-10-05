# User Guide & System Walkthrough Manual (Review 2 Complete)

## 1. Getting Started & Installation

### Step 1: Start Backend API (FastAPI)
```bash
cd backend
source venv/bin/activate
./venv/bin/pytest tests/test_full_project.py tests/test_phase_a.py tests/test_phase_b.py -v
python app/main.py
```
*FastAPI server runs on `http://localhost:8000`. Interactive API Docs are available at `http://localhost:8000/docs`.*

### Step 2: Start Frontend UI (React + Vite)
```bash
cd frontend
npm install
npm run build   # Production code-splitting build
npm run dev     # Starts dev server on http://localhost:5173
```

---

## 2. Comprehensive System Walkthrough

### Step 1: Multilingual Complaint Submission & Attachment
1. Open `http://localhost:5173/` and log in as `Citizen` (`ORG_001`).
2. Navigate to **Submit Complaint**.
3. Select **Tamil** (`தெரு விளக்கு எரியவில்லை...`) or **Hindi** (`पानी की पाइपलाइन फट गई है...`).
4. Select category and attach supporting document.
5. Click **Submit Complaint** and receive anonymous complaint ID (`COMPLAINT_001`).

### Step 2: Tamil/Hindi Translation & Resolution Workflow
1. Switch role to `Grievance Officer` (`ORG_001`).
2. Navigate to **Complaint Details** (`/complaints/COMPLAINT_001`).
3. Click **Translate Complaint** -> Select target language (**English**) -> View instant deterministic translation output alongside preserved original text.
4. Click **Resolve Complaint** -> Confirm in modal -> Complaint status updates to `Resolved` in SQLite database.

### Step 3: TF-IDF Vector Semantic Help Search
1. Open **Feature Discovery Assistant** panel on the right.
2. In the **Help Search Query** field, type `"audit logs and escalation"`.
3. Click **TF-IDF Vector Search**.
4. Inspect ranked matches with similarity score percentages and authorization badges.

### Step 4: A/B Discovery Uplift Analytics & F003/F006/F008 Breakdown
1. Navigate to **System Analytics** (`/analytics`).
2. Inspect live KPI cards: Overall Discovery Uplift (+499.88%) and Completion Uplift (+100.0%).
3. View the **Feature-Level Uplift Table** for `F003` (Translate Complaint), `F006` (Internal Case Notes), and `F008` (Audit & Escalation Logs).

### Step 5: Interactive Stakeholder System Validation
1. On the **System Analytics** page, click **Validate System** (or **Add Validation**).
2. Fill out evaluator role, usability rating (1–5), explainability rating (1–5), routing speedup %, and qualitative comments.
3. Click **Submit Evaluation** -> Feedback is persisted to database and live summary metrics update.
