# 🛠️ CONTINEO AI ATTENDANCE — COMMANDS CHEAT SHEET (`CMDS.md`)

> **Living Developer & Agent Reference**  
> This file tracks all CLI commands, assistant triggers, and scripts for the project.  
> It will be continuously updated as new tools, ML pipelines, and integrations are built.

---

## 🤖 1. Assistant Triggers (Things you can prompt Antigravity in Chat)

Whenever you open the chat with your agent, you can ask these quick prompts directly:

| Chat Prompt | What the Assistant Will Do |
| :--- | :--- |
| **`"Check what the collaborators did"`** | Fetches latest remote commits, analyzes diffs, checks architectural compliance, and gives you an executive breakdown. |
| **`"Audit latest commits"`** | Runs the DPDP Act and licence audit, flags any breaking changes, and updates your checklist. |
| **`"What do I need to do next?"`** | Checks current milestone against `TIMELINE.md` and lists your pending tasks as ML Lead. |
| **`"Run model benchmarks"`** | Evaluates YuNet + SFace accuracy and latency on test batches. |
| **`"Check DPDP compliance"`** | Scans repository to ensure no raw face images or unencrypted embeddings are stored. |
| **`"Rollback to last checkpoint"`** | Guides or executes a clean rollback to previous gate tags (`v0.0-scaffold`, `v0.1-gate1`, etc.). |

---

## 👥 2. Collaborator Monitoring & Repository Audit

Commands for reviewing teammate contributions and keeping the codebase aligned:

```bash
# Fetch latest remote branches and audit all new collaborator commits
python scripts/audit_collaborator_commits.py --fetch

# Audit last 5 commits locally without fetching
python scripts/audit_collaborator_commits.py --max-commits 5

# Audit commits since a specific git commit hash
python scripts/audit_collaborator_commits.py --since-commit <commit-hash>
```

---

## 🧠 3. Recognition Engine & ML Pipeline (WP3)

Commands for running and testing the Python/FastAPI ML service:

```bash
# Navigate to recognition engine
cd recognition-engine

# Install/update dependencies
pip install -r requirements.txt

# Start FastAPI development server (auto-reloads on file changes)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Interactive Swagger API Documentation (in browser)
# http://localhost:8000/docs

# Health & readiness probes
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

---

## 🧪 4. Testing & Verification

Commands for running automated test suites:

```bash
# Run all unit tests
pytest recognition-engine/tests/ -v

# Run tests with output printing
pytest recognition-engine/tests/ -s

# Run accuracy benchmark script (when test photos are available)
python recognition-engine/tests/test_accuracy_benchmarks.py
```

---

## 🐳 5. Docker & Container Deployment

Commands for containerizing the recognition engine:

```bash
# Build the Docker container image
docker build -t contineo-recognition-engine:latest -f recognition-engine/Dockerfile recognition-engine/

# Run the container locally (port 8000)
docker run -d --name recognition-service -p 8000:8000 contineo-recognition-engine:latest

# Check container logs
docker logs -f recognition-service

# Stop container
docker stop recognition-service && docker rm recognition-service
```

---

## 🔀 6. Git Workflow & Checkpoints

Quick reference for branches and checkpoint tags:

```bash
# Check current branch & status
git status

# Switch to your ML feature branch
git checkout feature/wp3-recognition-engine

# Pull latest updates from develop
git pull origin develop

# Commit your changes
git add -A
git commit -m "feat(wp3): <describe what you implemented>"
git push origin feature/wp3-recognition-engine

# Create a checkpoint tag for Gate reviews
git tag -a v0.X-gateX -m "Gate X Checkpoint"
git push origin --tags
```

---

*Note: New commands will be appended to this document as we implement subsequent modules.*
