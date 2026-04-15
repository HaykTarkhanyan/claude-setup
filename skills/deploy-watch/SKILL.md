---
name: deploy-watch
description: "Monitor a deployment end-to-end after push. Finds the triggered CI run, polls until completion, downloads test artifacts, and reports results. Use after pushing to track the full deployment pipeline."
argument-hint: "[repo]"
---

# Deploy Watch

End-to-end deployment monitoring after a push.

## Steps

1. **Detect repo**: If `$ARGUMENTS` names a repo or subdirectory, use it. Otherwise detect from the current directory.

2. **Find the triggered CI run**:
   ```bash
   gh run list --limit 5 --json databaseId,status,conclusion,headBranch,workflowName,createdAt,event
   ```
   Pick the most recent run triggered by a `push` event. Show the run ID, workflow name, and branch.

3. **Tell the user**: "Watching run #ID (workflow) on branch. I'll check back periodically."

4. **Poll for completion** using iterative background checks (NOT a bash while loop - avoids 600s timeout):
   ```bash
   gh run view <run-id> --json status,conclusion
   ```
   Run this with `run_in_background: true`. When the notification comes back:
   - If `status` is still `in_progress` or `queued`: wait ~20 seconds, then run another background check
   - If `status` is `completed`: proceed to step 5
   - Repeat up to 30 times (covers ~10 minutes of deployment)

5. **Check the result**:
   ```bash
   gh run view <run-id> --json conclusion,jobs
   ```
   Parse jobs for pass/fail status and duration.

6. **Download test artifacts** if they exist:
   ```bash
   rm -rf /tmp/test-results
   gh run download <run-id> --name test-results --dir /tmp/test-results 2>/dev/null
   ```
   If artifacts exist, summarize test results (pass/fail counts, failed test names).

7. **Report final status**:
   - Run conclusion (success/failure)
   - Per-job status with duration
   - Test results summary (if artifacts existed)
   - If failed: `gh run view <run-id> --log-failed | tail -50`
