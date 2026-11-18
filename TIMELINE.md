# 📅 AI Classroom Attendance — Timeline & Checkpoints

> **Last Updated:** 18 November 2026 | **Status:** 🟡 Pre-Start (Week 0)

## Quick Reference

| Week | Phase | Gate | Key Deliverable | Target |
|------|-------|------|-----------------|--------|
| 0 | Setup | — | Team confirmed, NDA signed | — |
| 1 | Foundation | — | Model survey, sandbox access | — |
| 2 | Foundation | 🚪 G1 | Architecture sign-off | PoC working |
| 3 | Build | — | Core detection+recognition pipeline | ≥85% |
| 4 | Build | — | FAISS + API endpoints live | ≥88% |
| 5 | Build | — | Multi-photo merge + confidence scoring | ≥90% |
| 6 | Build | 🚪 G2 | Hidden test set evaluation | **≥90%** |
| 7 | Polish | — | Accuracy improvement sprint | >92% |
| 8 | Polish | 🚪 G3 | Full integration test | **≥95%, <1% FP** |
| 9 | Pilot | — | First live classroom | Real data |
| 10 | Pilot | — | Continued pilot sessions | Maintain 95% |
| 11 | Pilot | — | Final hidden test + pilot report | Leaderboard |
| 12 | Final | 🎤 | Jury demo + viva-voce | Win! |

## Checkpoint Tags

```
v0.1-gate1-architecture    → Week 2
v0.2-gate2-90pct           → Week 6
v0.3-gate3-95pct           → Week 8
v0.4-pilot-start           → Week 9
v1.0-final-submission      → Week 12
```

## Decisions Log

| # | Date | Decision | Chosen | Rationale | Reversible? |
|---|------|----------|--------|-----------|-------------|
| D1 | 18 Nov | Face Detection | TBD (YuNet likely) | Benchmark in Week 1 | ✅ |
| D2 | 18 Nov | Face Recognition | TBD (SFace likely) | Benchmark in Week 1 | ✅ |
| D3 | 18 Nov | Backend | FastAPI | Briefing rec., async | ⚠️ |
| D4 | 18 Nov | Mobile | Flutter | Briefing rec., cross-platform | ❌ |
| D5 | 18 Nov | Database | Percona MySQL | Briefing rec. | ⚠️ |
| D6 | 18 Nov | Matching | FAISS IndexFlatIP | Exact match, small gallery | ✅ |

---

*Full detailed timeline: see docs/PROJECT_ANALYSIS.md and the artifact in Antigravity.*
