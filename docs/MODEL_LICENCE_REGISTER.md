# 📋 Model & Licence Register

> **Required by Contineo briefing.** Keep updated throughout the project.

## Rules
- All libraries: OSI-approved open-source licence
- All models: open-weight, licensed for commercial use
- No closed or paid face-recognition APIs
- Research-only weights: benchmark only, never shipped

## Register

| # | Model/Library | Version | Licence | Commercial? | Use in Project | Status |
|---|--------------|---------|---------|-------------|----------------|--------|
| 1 | YuNet | v2023 | Apache 2.0 | ✅ Yes | Face detection | 🔬 Evaluating |
| 2 | SFace | v2023 | Apache 2.0 | ✅ Yes | Face embeddings | 🔬 Evaluating |
| 3 | FAISS | latest | MIT | ✅ Yes | Vector matching | ✅ Selected |
| 4 | OpenCV | 4.x | Apache 2.0 | ✅ Yes | Image processing | ✅ Selected |
| 5 | FastAPI | 0.100+ | MIT | ✅ Yes | Backend API | ✅ Selected |
| 6 | Flutter | stable | BSD-3 | ✅ Yes | Mobile apps | ✅ Selected |
| 7 | Percona MySQL | 8.x | GPL v2 | ✅ Server use | Database | ✅ Selected |
| 8 | LiteRT | latest | Apache 2.0 | ✅ Yes | On-device inference | 🔬 Evaluating |

## Benchmark-Only Models (DO NOT SHIP)

| Model | Licence | Why Not Shippable | Benchmark Result |
|-------|---------|-------------------|------------------|
| ArcFace (MS1MV3) | Research only | MS-Celeb-1M derived, non-commercial | TBD |

## Licence Check Process
1. Before adding ANY new model/library, check its licence
2. Record it in this register
3. If unsure, ask mentor before using
4. Keep download URLs and licence file copies in `docs/licences/`
