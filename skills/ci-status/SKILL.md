---
name: ci-status
description: "Check GitHub Actions workflow status for a repo. Shows recent runs, job statuses, and whether CI is passing. Use when the user asks about CI, builds, deployments, or pipeline status."
argument-hint: "[repo] [run-id]"
---

# CI Status Check

Show GitHub Actions workflow status for a repo.

## Steps

1. **Detect repo**: If `$ARGUMENTS` starts with a subdirectory name, cd into it. Otherwise stay in the current directory. Verify it's a git repo.

2. **If a run ID is provided** (numeric argument), show detailed status for that run:
   ```bash
   gh run view <run-id>
   ```
   Show job names, statuses, durations, and any failure annotations.

3. **Otherwise, list recent runs**:
   ```bash
   gh run list --limit 10
   ```

4. **Present a summary table** with columns:
   - Status (passed/failed/in_progress)
   - Workflow name
   - Commit message (truncated)
   - Branch
   - Duration
   - When

5. **If any runs are failing**, show the failed job details:
   ```bash
   gh run view <failed-run-id> --log-failed
   ```
   Summarize the failure reason concisely.

6. **If runs are in_progress**, mention which jobs are still running and how long they've been going.
