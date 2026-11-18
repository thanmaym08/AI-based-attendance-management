# 🎯 Contineo AI Classroom Attendance

> **Internship Programme 2026** · e-Sutra Chronicles Pvt Ltd (Contineo®)  
> **Problem:** AI-based attendance from classroom photos, posted straight into Contineo.

## What This Does

A teacher takes 2–3 photos of their classroom. The AI:
1. **Detects** every face in the photos
2. **Matches** them against that class's enrolled students
3. **Flags** students from wrong sections (cross-section fraud detection)
4. **Shows** the teacher a review screen with confidence scores
5. **Posts** confirmed attendance directly into Contineo®

## Architecture

| Component | Tech | Location |
|-----------|------|----------|
| Student Enrolment App | Flutter + LiteRT | Android phone |
| Faculty Capture App | Flutter | Android phone |
| Recognition Engine | Python + OpenCV + FAISS | Server (India) |
| Backend API | FastAPI | Server (Docker) |
| Database | Percona MySQL | Server |
| Integration | REST → Contineo® ERP | Server |

## Project Structure

```
├── recognition-engine/     # WP3: ML pipeline (Python)
│   ├── api/                # FastAPI endpoints
│   ├── core/               # Detection, embedding, matching
│   ├── preprocessing/      # CLAHE, alignment, quality checks
│   ├── tests/              # Accuracy benchmarks, unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── mobile/                 # WP1 + WP2: Flutter apps
│   ├── student_app/        # Enrolment with guided selfies
│   └── faculty_app/        # Photo capture + review
├── integration/            # WP4: Contineo connector
├── admin-dashboard/        # WP5: Reports & monitoring
├── models/                 # Model weights (Git LFS / DVC)
├── data/                   # Data files (NOT photos — see .gitignore)
├── docs/                   # Documentation
│   ├── MODEL_LICENCE_REGISTER.md
│   ├── OPEN_QUESTIONS.md
│   └── decisions/
├── config/                 # Configuration files
├── scripts/                # Utility scripts
├── TIMELINE.md
└── README.md
```

## Quick Start

```bash
# Clone
git clone <repo-url>
cd contineo-ai-attendance

# Recognition engine
cd recognition-engine
pip install -r requirements.txt
uvicorn api.main:app --reload

# See docs/ for detailed setup
```

## Team

| Role | Owns |
|------|------|
| Team Leader | Plan, gates, pitch |
| ML / Computer Vision | WP3 recognition engine |
| Mobile App Dev | WP1 enrolment + WP2 faculty app |
| Backend & Integration | WP4 API + Contineo connector |
| Full-stack / QA | WP5 dashboard + testing |

## Key Targets

| Metric | Target |
|--------|--------|
| Correct marks | ≥ 95% |
| False marks | < 1% |
| Photo → Contineo | < 60 seconds |
| Student enrolment | < 2 minutes |

## Licence

All components use OSI-approved open-source licences. See [Model & Licence Register](docs/MODEL_LICENCE_REGISTER.md).
