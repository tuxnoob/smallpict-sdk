#!/usr/bin/env zsh
# ==============================================================================
# SmallPict SDK Synchronized Multi-Registry Release Orchestrator
# Bumps versions across all 7 standalone repos, runs contract audit,
# creates GPG signed commits & tags, and pushes with gg1-push.
# ==============================================================================
set -e

# Source user environment for custom aliases like gg1-push
if [[ -f "$HOME/.zshrc" ]]; then
  source "$HOME/.zshrc" 2>/dev/null || true
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

VERSION="${1:-0.0.1}"

echo "=================================================="
echo "  SmallPict Multi-SDK Release Orchestrator"
echo "  Target Release Version: v${VERSION}"
echo "=================================================="
echo ""

# 1. Jalankan audit kontrak integritas
echo "🔍 Menjalankan Cross-SDK Contract Integrity Audit..."
"${SCRIPT_DIR}/check-sdk-contract.sh"
echo ""

# 2. Update versi di semua manifest file jika ada perubahan versi
echo "📝 Menyesuaikan version string ke ${VERSION} di 7 repositori..."

# Python
if [[ -f "${PARENT_DIR}/smallpict-python/pyproject.toml" ]]; then
  sed -i '' "s/version = \".*\"/version = \"${VERSION}\"/" "${PARENT_DIR}/smallpict-python/pyproject.toml" 2>/dev/null || true
  sed -i '' "s/__version__ = \".*\"/__version__ = \"${VERSION}\"/" "${PARENT_DIR}/smallpict-python/smallpict/__init__.py" 2>/dev/null || true
fi

# Node.js
if [[ -f "${PARENT_DIR}/smallpict-node/package.json" ]]; then
  sed -i '' "s/\"version\": \".*\"/\"version\": \"${VERSION}\"/" "${PARENT_DIR}/smallpict-node/package.json" 2>/dev/null || true
fi

# Rust
if [[ -f "${PARENT_DIR}/smallpict-rust/Cargo.toml" ]]; then
  sed -i '' "s/^version = \".*\"/version = \"${VERSION}\"/" "${PARENT_DIR}/smallpict-rust/Cargo.toml" 2>/dev/null || true
fi

# Ruby
if [[ -f "${PARENT_DIR}/smallpict-ruby/lib/smallpict/version.rb" ]]; then
  sed -i '' "s/VERSION = \".*\"/VERSION = \"${VERSION}\"/" "${PARENT_DIR}/smallpict-ruby/lib/smallpict/version.rb" 2>/dev/null || true
fi

# Java
if [[ -f "${PARENT_DIR}/smallpict-java/pom.xml" ]]; then
  sed -i '' "s/<version>.*<\/version>/<version>${VERSION}<\/version>/" "${PARENT_DIR}/smallpict-java/pom.xml" 2>/dev/null || true
fi

echo "✅ Manifest file versi ${VERSION} siap!"
echo ""

# 3. Jalankan push-to-github.sh
PUSH_SCRIPT="${PARENT_DIR}/push-to-github.sh"
if [[ -f "${PUSH_SCRIPT}" ]]; then
  echo "🚀 Memulai Signed Commit & Push ke 7 Repositori via gg1-push..."
  "${PUSH_SCRIPT}" "feat: release v${VERSION}"
else
  echo "⚠️ Skrip ${PUSH_SCRIPT} tidak ditemukan. Silakan jalankan push manual."
fi
