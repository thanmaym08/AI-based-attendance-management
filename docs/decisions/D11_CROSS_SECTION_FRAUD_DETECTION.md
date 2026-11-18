# 🚨 Cross-Section Fraud Detection — Design Document

> **Decision ID:** D11  
> **Date:** 18 November 2026  
> **Status:** ✅ Approved (team feature addition)  
> **Priority:** High — differentiator in competition

---

## Problem

A student enrolled in **Section A** walks into **Section B's** classroom and sits there.
Without cross-section detection, two things can go wrong:

| Scenario | What Happens Without This Feature |
|----------|----------------------------------|
| Section A student in Section B | They get **wrongly marked present** in Section B (false mark) AND **remain absent** in Section A |
| System only matches against class roster | The intruder's face is simply "not found" and silently ignored — no alert |

## Solution: Two-Tier Matching

### Tier 1 — Class Roster Match (Standard)
Match detected faces against **only** the students enrolled in this specific class+section.
- Match found → ✅ **Mark present** (with confidence score)

### Tier 2 — Global Enrolment Match (Fraud Detection)
If a face does **NOT** match the class roster, run it against **all enrolled students institution-wide**.
- Match in another section → 🚨 **INTRUDER**: "Rahul Sharma (Section A, USN: 1BM22CS045) detected in your Section B class"
- No match anywhere → ⚠️ **UNKNOWN**: "Unrecognised face detected — possibly unenrolled student or visitor"

### Why Two Tiers?

| Approach | Speed | Accuracy | Fraud Detection |
|----------|-------|----------|-----------------|
| Roster-only matching | ⚡ Fast (40–60 students) | High (small gallery) | ❌ None |
| Global-only matching | 🐌 Slower (1000+ students) | Lower (bigger gallery = more confusion) | ✅ Yes |
| **Two-tier (ours)** | ⚡ Fast for most, slight delay for unknowns | ✅ Best of both | ✅ Yes |

## FAISS Index Architecture

```
indices/
├── roster/
│   ├── CS_SEC_A_SEM5.index      # 60 students
│   ├── CS_SEC_B_SEM5.index      # 58 students
│   ├── EC_SEC_A_SEM3.index      # 55 students
│   └── ...
└── global/
    └── institution_all.index     # ALL enrolled students (~2000-5000)
```

**Flow:**
1. Faculty takes photo → API receives `faculty_id + timestamp`
2. Contineo resolves → `class = CS_SEC_A_SEM5`, roster = 60 students
3. Detect faces → 45 faces found
4. Match each face against `CS_SEC_A_SEM5.index`
   - 42 matches → ✅ Present
   - 3 no-match → go to Tier 2
5. Match 3 unknowns against `institution_all.index`
   - 2 match students from Section B → 🚨 Intruder alert
   - 1 no match anywhere → ⚠️ Unknown face

## API Response Schema

```json
{
  "session_id": "sess_20261118_CS_A_0900",
  "class": "CS_SEC_A_SEM5",
  "total_faces_detected": 45,
  "results": {
    "present": [
      {
        "student_id": "1BM22CS001",
        "name": "Student Name",
        "confidence": 0.92,
        "photo_index": 1
      }
    ],
    "absent": [
      {
        "student_id": "1BM22CS015",
        "name": "Student Name",
        "note": "Not detected in any photo"
      }
    ],
    "intruders": [
      {
        "detected_student_id": "1BM22CS045",
        "detected_name": "Rahul Sharma",
        "actual_section": "CS_SEC_B_SEM5",
        "confidence": 0.88,
        "photo_index": 2,
        "alert": "Student from Section B detected in your class"
      }
    ],
    "unknown_faces": [
      {
        "face_id": "face_003",
        "confidence": null,
        "bounding_box": [120, 45, 230, 190],
        "photo_index": 1,
        "alert": "Unrecognised face — verify manually"
      }
    ]
  },
  "processing_time_ms": 4200
}
```

## Faculty Review Screen (What Mobile Dev Should Build)

```
┌─────────────────────────────────────────┐
│  📸 Attendance — CS Section A, 9:00 AM  │
├─────────────────────────────────────────┤
│                                         │
│  ✅ PRESENT (42/60)          [View All] │
│  ┌──────────────────────────────────┐   │
│  │ ✅ Anil Kumar        92% ✓      │   │
│  │ ✅ Priya Desai       95% ✓      │   │
│  │ ✅ ...                           │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ❌ ABSENT (15/60)           [View All] │
│  ┌──────────────────────────────────┐   │
│  │ ❌ Kiran Rao         [+Add]     │   │
│  │ ❌ ...                           │   │
│  └──────────────────────────────────┘   │
│                                         │
│  🚨 INTRUDERS (2)          ⚠️ REVIEW   │
│  ┌──────────────────────────────────┐   │
│  │ 🚨 Rahul Sharma      88%       │   │
│  │    Section B student detected!   │   │
│  │    [Dismiss] [Report to Admin]   │   │
│  │                                  │   │
│  │ 🚨 Meera Joshi       85%       │   │
│  │    Section C student detected!   │   │
│  │    [Dismiss] [Report to Admin]   │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ⚠️ UNKNOWN FACES (1)                  │
│  ┌──────────────────────────────────┐   │
│  │ ⚠️ Unknown person    [View]     │   │
│  │    [Dismiss] [Report]            │   │
│  └──────────────────────────────────┘   │
│                                         │
│         [✅ Submit Attendance]          │
└─────────────────────────────────────────┘
```

## Edge Cases to Handle

| Case | Handling |
|------|---------|
| Student officially transferred from A to B | Contineo roster is source of truth — if roster says they're in B, they're legitimate |
| Combined class (A+B together for a lab) | Faculty selects "combined class" mode; roster = union of both sections |
| Guest lecturer in photo | Shows as unknown face — professor dismisses |
| Student with legitimate reason in other section | Professor can dismiss the intruder alert (logged in audit) |
| Same student enrolled in elective across sections | Roster includes them — no false intruder alert |

## Impact on Scoring

This feature directly improves:
- **False marking (10%)** — prevents wrong-section attendance
- **Recognition accuracy (25%)** — demonstrates robust matching
- **Usability (15%)** — professors get actionable alerts
- **Privacy & security (10%)** — demonstrates audit trail thinking
- **Final pitch (5%)** — strong differentiator in viva-voce

**Total potential impact: up to 65% of score criteria touched.**

## Implementation Priority

| Task | Week | Effort |
|------|------|--------|
| Build global FAISS index alongside roster indices | Week 4 | Low — same embedding pipeline |
| Add two-tier matching logic | Week 5 | Medium — conditional matching |
| Design intruder alert API response | Week 5 | Low — schema addition |
| Coordinate with mobile dev for review UI | Week 5–6 | Medium — UI design |
| Test with cross-section scenarios | Week 6–8 | Ongoing |
