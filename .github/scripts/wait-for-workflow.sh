#!/usr/bin/env bash
# wait-for-workflow.sh
# Polls a GitHub Actions workflow until it completes.
#
# Usage: wait-for-workflow.sh <workflow_name> [branch]
#
# Environment variables:
#   GH_TOKEN         - GitHub token for authentication (required)
#   POLL_INITIAL_WAIT - Seconds to wait before polling (default: 30)
#   POLL_INTERVAL    - Seconds between poll attempts (default: 15)
#   POLL_MAX_ATTEMPTS - Maximum number of poll attempts (default: 20)

set -euo pipefail

WORKFLOW_NAME="${1:?Usage: $0 <workflow_name> [branch]}"
BRANCH="${2:-}"

POLL_INITIAL_WAIT="${POLL_INITIAL_WAIT:-30}"
POLL_INTERVAL="${POLL_INTERVAL:-15}"
POLL_MAX_ATTEMPTS="${POLL_MAX_ATTEMPTS:-20}"

BRANCH_ARGS=()
[ -n "$BRANCH" ] && BRANCH_ARGS=("--branch" "$BRANCH")

echo "Waiting ${POLL_INITIAL_WAIT}s for workflow '${WORKFLOW_NAME}' to start..."
sleep "${POLL_INITIAL_WAIT}"

for i in $(seq 1 "${POLL_MAX_ATTEMPTS}"); do
  STATUS=$(gh run list --workflow "${WORKFLOW_NAME}" "${BRANCH_ARGS[@]}" \
    --limit 1 --json status,conclusion \
    --jq '.[0] | "\(.status):\(.conclusion)"' 2>/dev/null || echo "pending:")
  echo "Attempt ${i}/${POLL_MAX_ATTEMPTS}: ${STATUS}"
  case "${STATUS}" in
    completed:*) echo "Workflow '${WORKFLOW_NAME}' completed."; exit 0 ;;
  esac
  sleep "${POLL_INTERVAL}"
done

echo "Timed out waiting for workflow '${WORKFLOW_NAME}'."
exit 1
