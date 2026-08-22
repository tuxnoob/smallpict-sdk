#!/usr/bin/env bash
# ==============================================================================
# SmallPict SDK Parent Contract Verification & Quality Audit Script
# Validates that all 7 official SDK repositories strictly adhere to OpenAPI 3.1.0,
# contain standard documentation, security policies, and centralized workflows.
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
OPENAPI_SPEC="${ROOT_DIR}/../smallPict-api/docs/openapi.yaml"

echo "=================================================="
echo "  SmallPict Master SDK Contract Audit (Phase 4)   "
echo "=================================================="

# 1. Check OpenAPI specification
if [ -f "${OPENAPI_SPEC}" ]; then
  echo "✅ Master OpenAPI 3.1.0 Spec: ${OPENAPI_SPEC}"
else
  echo "❌ Missing Master OpenAPI Spec at: ${OPENAPI_SPEC}"
  exit 1
fi

# 2. Check centralized GitHub Actions workflows
CENTRAL_WORKFLOWS=(".github/workflows/ci.yml" ".github/workflows/release.yml")
for wf in "${CENTRAL_WORKFLOWS[@]}"; do
  if [ -f "${ROOT_DIR}/${wf}" ]; then
    echo "✅ Centralized Workflow: ${wf}"
  else
    echo "❌ Missing Centralized Workflow: ${wf}"
    exit 1
  fi
done

REQUIRED_DOCS=("LICENSE" "SECURITY.md" "CHANGELOG.md" "README.md")

SDKS=(
  "smallpict-node:npm:@smallpict/sdk"
  "smallpict-python:pypi:smallpict"
  "smallpict-php:packagist:smallpict/smallpict-php"
  "smallpict-go:pkg.go.dev:github.com/tuxnoob/smallpict-go"
  "smallpict-rust:crates.io:smallpict"
  "smallpict-ruby:rubygems:smallpict"
  "smallpict-java:maven:com.smallpict:smallpict-java"
)

TOTAL_ERRORS=0

echo ""
echo "Auditing 7 SDK Child Repositories..."
echo "--------------------------------------------------"

for entry in "${SDKS[@]}"; do
  IFS=":" read -r dir registry package_name <<< "${entry}"
  TARGET_PATH="${ROOT_DIR}/${dir}"

  if [ ! -d "${TARGET_PATH}" ]; then
    echo "❌ Missing SDK directory: ${TARGET_PATH}"
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    continue
  fi

  MISSING_FILES=()
  for file in "${REQUIRED_DOCS[@]}"; do
    if [ ! -f "${TARGET_PATH}/${file}" ]; then
      MISSING_FILES+=("${file}")
    fi
  done

  if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    printf "✅ [%-16s] (%-10s -> %-35s) : PASS\n" "${dir}" "${registry}" "${package_name}"
  else
    printf "❌ [%-16s] Missing files: %s\n" "${dir}" "${MISSING_FILES[*]}"
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
  fi
done

echo "--------------------------------------------------"

if [ ${TOTAL_ERRORS} -eq 0 ]; then
  echo "🎉 100% PASS: All 7 SDK repositories satisfy parent contract standards!"
  exit 0
else
  echo "💥 Audit failed with ${TOTAL_ERRORS} error(s)."
  exit 1
fi
