#!/bin/bash
# install-repo.sh — Clone, install, and clean up a single skill repo
# Usage: install-repo.sh <repo-url> <branch> <commit|latest> <agent> [temp-dir]
#
# Examples:
#   install-repo.sh https://github.com/anthropics/skills main latest claude-code
#   install-repo.sh git@gitlab.com:org/skills.git main abc123 cursor /tmp
#
# This is a helper to avoid reconstructing the clone→install→cleanup cycle.
# The operations in references/operations.md describe the same workflow in natural language.

set -euo pipefail

REPO_URL="$1"
BRANCH="$2"
COMMIT="$3"        # "latest" or a specific commit hash
AGENT="$4"
TEMP_DIR="${5:-/tmp}"

CLONE_DIR=$(mktemp -d "${TEMP_DIR}/skillfile-XXXXXX")

cleanup() { rm -rf "$CLONE_DIR"; }
trap cleanup EXIT

echo "→ Cloning $REPO_URL@$BRANCH into $CLONE_DIR"
git clone --branch "$BRANCH" "$REPO_URL" "$CLONE_DIR" 2>&1

if [ "$COMMIT" != "latest" ]; then
    echo "→ Checking out $COMMIT"
    cd "$CLONE_DIR" && git checkout "$COMMIT" 2>&1
fi

ACTUAL_COMMIT=$(cd "$CLONE_DIR" && git rev-parse HEAD)
echo "→ Commit: $ACTUAL_COMMIT"

echo "→ Installing for agent: $AGENT"
npx -y skills@1.4.5 add "$CLONE_DIR" --agent "$AGENT" --skill '*' -y 2>&1

echo "→ Done. Commit: $ACTUAL_COMMIT"
