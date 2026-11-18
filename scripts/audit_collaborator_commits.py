#!/usr/bin/env python3
"""
Collaborator Commit Auditor & Architecture Compatibility Checker
================================================================
Monitors repository commits made by team collaborators, analyzes changed files,
verifies compliance with project rules (DPDP Act, licences, API contracts,
work package alignment), and generates action reminders for the ML Lead.

Usage:
  python scripts/audit_collaborator_commits.py [--since-commit <sha>] [--max-commits 10] [--fetch]
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime

CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), "..", ".last_audited_commit")

# Forbidden file extensions that violate DPDP Act or repo hygiene
FORBIDDEN_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".heic",  # Raw face photos
    ".onnx", ".pt", ".pth", ".tflite", ".bin"                     # Heavy models should use Git LFS / storage
}

# Work Package mapping based on paths
WP_MAPPING = {
    "mobile/student_app": "WP1 (Student Enrolment App)",
    "mobile/faculty_app": "WP2 (Faculty Capture App)",
    "recognition-engine": "WP3 (Recognition Engine & ML)",
    "integration": "WP4 (Contineo Integration Layer)",
    "admin-dashboard": "WP5 (Admin & Reports)",
    "config": "System Configuration",
    "docs": "Documentation & Decisions",
}

def run_git(cmd_args):
    """Execute a git command and return stripped stdout."""
    res = subprocess.run(["git"] + cmd_args, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        return None
    return res.stdout.strip()

def get_current_user_email():
    return run_git(["config", "user.email"]) or ""

def get_last_audited_commit():
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r") as f:
                return f.read().strip()
        except Exception:
            return None
    return None

def save_last_audited_commit(commit_sha):
    try:
        with open(CHECKPOINT_FILE, "w") as f:
            f.write(commit_sha.strip())
    except Exception as e:
        print(f"Warning: Could not save last audited commit: {e}", file=sys.stderr)

def fetch_remotes():
    print("🔄 Fetching latest commits from remote...")
    subprocess.run(["git", "fetch", "--all", "--prune"], check=False)

def get_commits(since_commit=None, max_count=10):
    """Retrieve list of commits (sha, author_name, author_email, date, subject)."""
    rev_range = f"{since_commit}..HEAD" if since_commit else f"-n {max_count}"
    log_format = "%H|%an|%ae|%ad|%s"
    cmd = ["log", f"--format={log_format}", "--date=short"]
    if since_commit:
        cmd.append(f"{since_commit}..HEAD")
    else:
        cmd.extend(["-n", str(max_count)])
    
    output = run_git(cmd)
    if not output:
        return []

    commits = []
    for line in output.split("\n"):
        parts = line.strip().split("|", 4)
        if len(parts) == 5:
            commits.append({
                "sha": parts[0],
                "author": parts[1],
                "email": parts[2],
                "date": parts[3],
                "subject": parts[4]
            })
    return commits

def get_changed_files(commit_sha):
    """Get list of files modified/added/deleted in a commit."""
    output = run_git(["diff-tree", "--no-commit-id", "--name-status", "-r", "--root", commit_sha])
    if not output:
        return []
    changes = []
    for line in output.split("\n"):
        parts = line.strip().split("\t", 1)
        if len(parts) == 2:
            changes.append({"status": parts[0], "file": parts[1]})
    return changes

def analyze_changes(changed_files):
    """Audit changes against project standards and work package alignment."""
    findings = {
        "wps_affected": set(),
        "violations": [],
        "warnings": [],
        "notices": [],
        "action_items": []
    }

    for item in changed_files:
        status = item["status"]
        fpath = item["file"]
        ext = os.path.splitext(fpath)[1].lower()

        # 1. DPDP Compliance check: Raw photos or unapproved heavy binaries committed
        if ext in FORBIDDEN_EXTENSIONS:
            if not fpath.startswith("docs/"):
                findings["violations"].append(
                    f"🚨 [DPDP / Git Hygiene] File with restricted extension '{fpath}' was committed. "
                    "Raw face photos MUST NEVER be committed to Git under the DPDP Act 2023. Model weights must use LFS/external volume."
                )

        # 2. Work package classification
        matched_wp = False
        for prefix, wp_name in WP_MAPPING.items():
            if fpath.startswith(prefix):
                findings["wps_affected"].add(wp_name)
                matched_wp = True
                break
        if not matched_wp and not fpath.startswith("."):
            findings["wps_affected"].add("Root / General")

        # 3. Model & Licence check: dependency changes
        if fpath in ("recognition-engine/requirements.txt", "mobile/student_app/pubspec.yaml", "mobile/faculty_app/pubspec.yaml"):
            findings["warnings"].append(
                f"📋 [Licence Warning] Dependencies modified in '{fpath}'. "
                "Ensure any new package uses an OSI-approved licence and update docs/MODEL_LICENCE_REGISTER.md."
            )
            findings["action_items"].append("Review new packages in MODEL_LICENCE_REGISTER.md for commercial compliance.")

        # 4. API Contract check
        if fpath.startswith("recognition-engine/api/") or fpath == "config/engine_config.yaml":
            findings["notices"].append(
                f"🔌 [API/Config Impact] '{fpath}' was modified. "
                "Ensure changes align with Mobile (WP1/WP2) and Integration (WP4) expectations."
            )
            findings["action_items"].append("Verify API response schemas with Mobile and Backend teammates.")

        # 5. Mobile integration check
        if fpath.startswith("mobile/"):
            findings["action_items"].append(
                "Coordinate with mobile devs: ensure guided selfie capture (WP1) and review screen (WP2) meet ML requirements."
            )

        # 6. Integration layer check
        if fpath.startswith("integration/"):
            findings["action_items"].append(
                "Coordinate with backend dev: verify Contineo attendance payload matches the recognition output format."
            )

    return findings

def audit_commits(since_commit=None, max_commits=5, fetch=False):
    if fetch:
        fetch_remotes()

    last_checkpoint = since_commit or get_last_audited_commit()
    commits = get_commits(since_commit=last_checkpoint, max_count=max_commits)

    if not commits:
        print("✅ No new commits found since last checkpoint.")
        return

    print("=" * 80)
    print(f"🔎 CONTINEO AI ATTENDANCE — COLLABORATOR AUDIT REPORT")
    print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📦 Commits to review: {len(commits)}")
    print("=" * 80)

    all_action_items = set()

    for idx, c in enumerate(commits, 1):
        sha_short = c["sha"][:7]
        print(f"\n[{idx}/{len(commits)}] Commit {sha_short} by {c['author']} ({c['email']}) on {c['date']}")
        print(f"📝 Message: {c['subject']}")
        
        changed_files = get_changed_files(c["sha"])
        findings = analyze_changes(changed_files)

        # Summary of files
        print(f"   Files changed: {len(changed_files)}")
        for f in changed_files[:6]:
            print(f"     • [{f['status']}] {f['file']}")
        if len(changed_files) > 6:
            print(f"     ... and {len(changed_files) - 6} more files")

        # Work packages
        if findings["wps_affected"]:
            print(f"   🎯 Impacted Work Packages: {', '.join(sorted(findings['wps_affected']))}")

        # Violations
        if findings["violations"]:
            print("   🚨 CRITICAL VIOLATIONS:")
            for v in findings["violations"]:
                print(f"      {v}")

        # Warnings
        if findings["warnings"]:
            print("   ⚠️ WARNINGS:")
            for w in findings["warnings"]:
                print(f"      {w}")

        # Notices
        if findings["notices"]:
            print("   ℹ️ NOTICES:")
            for n in findings["notices"]:
                print(f"      {n}")

        for act in findings["action_items"]:
            all_action_items.add(act)

    print("\n" + "=" * 80)
    print("📋 YOUR ACTION REMINDER (ML LEAD & ARCHITECT CHECKLIST):")
    if all_action_items:
        for act in sorted(all_action_items):
            print(f"  [ ] {act}")
    else:
        print("  [x] All inspected commits align with current project architecture!")
    print("=" * 80)

    # Save latest commit as new checkpoint
    save_last_audited_commit(commits[0]["sha"])
    print(f"💾 Checkpoint updated to commit {commits[0]['sha'][:7]}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit collaborator commits for Contineo AI Attendance")
    parser.add_argument("--since-commit", help="Commit hash to check after")
    parser.add_argument("--max-commits", type=int, default=5, help="Max commits to check if no checkpoint exists")
    parser.add_argument("--fetch", action="store_true", help="Run git fetch before auditing")
    args = parser.parse_args()

    audit_commits(since_commit=args.since_commit, max_commits=args.max_commits, fetch=args.fetch)
