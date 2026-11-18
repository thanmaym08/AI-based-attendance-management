# ❓ Contineo AI Attendance — Open Questions & Decision Points

> **Updated:** 18 November 2026 | **Review Scheduled for:** Tomorrow's Session

---

## 🔴 Category 1: Team & Roles (Gate 1 Requirement)
- [ ] **Q1. Team Composition:** Has your team of 5–7 members been finalized? 
- [ ] **Q2. Role Allocation:** Who is taking which specific role?
  - *Team Leader:* (Takes charge of gate reviews, coordination, pitch)
  - *ML / Computer Vision Engineer:* **You** (WP3: Detection, Recognition, Fraud Detection, FAISS)
  - *Mobile App Developer(s):* (WP1: Enrolment App + WP2: Faculty App in Flutter)
  - *Backend & Integration Developer:* (WP4: FastAPI, Contineo REST Connector)
  - *Full-Stack / QA Engineer:* (WP5: Admin Dashboard, Field testing, Analytics)

---

## 🔴 Category 2: Contineo Access & Mentor Meeting
- [ ] **Q3. Mentor Meeting:** When is your first official meeting with your Contineo mentors (Sowmya BG / Kasheem Karajagi)?
- [ ] **Q4. Sandbox API:** Have you received the Contineo Sandbox API credentials, token endpoints, and payload documentation yet?
- [ ] **Q5. NDA & Consent Guidelines:** Has the NDA paperwork been signed by the team?

---

## 🟡 Category 3: Data & Testing Benchmarks
- [ ] **Q6. Training Dataset:** When will Contineo provide the consented student face photos for training/testing?
- [ ] **Q7. Immediate Prototyping:** While waiting for Contineo's dataset, should we begin building and benchmarking the YuNet + SFace pipeline using public benchmark datasets (LFW / WIDER Face)?
- [ ] **Q8. Classroom Lighting & Sample Photos:** Do you have any actual classroom photos from BMSIT to evaluate bench depth and lighting conditions?

---

## 🟡 Category 4: Physical Pilot Classroom Specs
- [ ] **Q9. Class Size:** What is the exact student batch size for the pilot classes? (40, 60, or 80 students?)
- [ ] **Q10. Faculty Devices:** What phone models will the faculty use during the pilot? (Mid-range Android, camera resolution?)
- [ ] **Q11. Network Connectivity:** Will the classrooms have reliable Wi-Fi or should the mobile app queue photo uploads if 4G/Wi-Fi drops temporarily?

---

## 🟢 Category 5: Hosting & Infrastructure
- [ ] **Q12. Server Hosting:** Where will the Recognition Engine Docker container be hosted?
  - College local server / lab machine?
  - Cloud server (AWS, GCP, or Azure with student credits) hosted in an India data center (DPDP requirement)?
  - Will Contineo provide a hosting instance?

---

## 🟢 Category 6: Feature Nuances (Cross-Section & Edge Cases)
- [ ] **Q13. Joint / Combined Lectures:** If two sections sit together (e.g., Section A and Section B attend the same seminar or lab), should the faculty app allow selecting "Combined Class" so students from both sections are marked present rather than flagged as intruders?
- [ ] **Q14. Intruder Notification Style:** In the faculty review screen, is a visual warning banner sufficient, or should it trigger an alert dialog?
