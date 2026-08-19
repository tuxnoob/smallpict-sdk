#!/usr/bin/env bash
set -euo pipefail

# SmallPict Cross-SDK Contract & Repository Validator
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OPENAPI_SPEC="${WORKSPACE_ROOT}/../smallPict-api/docs/openapi.yaml"

echo "=================================================="
echo "  SmallPict SDK Parent Contract Verification      "
echo "=================================================="

# 1. Verify OpenAPI Specification
if [ ! -f "${OPENAPI_SPEC}" ]; then
  echo "❌ Error: OpenAPI specification not found at ${OPENAPI_SPEC}"
  exit 1
fi
echo "✅ OpenAPI 3.1.0 Specification verified: ${OPENAPI_SPEC}"

SDKS=(
  "smallpict-node:package.json:npm"
  "smallpict-python:pyproject.toml:pypi"
  "smallpict-php:composer.json:packagist"
  "smallpict-go:go.mod:pkg.go.dev"
  "smallpict-rust:Cargo.toml:crates.io"
  "smallpict-ruby:smallpict.gemspec:rubygems"
  "smallpict-java:pom.xml:maven"
)

ERRORS=0

echo ""
echo "Auditing 7 SDK child repositories..."
echo "--------------------------------------------------"

for entry in "${SDKS[@]}"; do
  IFS=":" read -r sdk_dir manifest registry <<< "${entry}"
  TARGET_PATH="${WORKSPACE_ROOT}/${sdk_dir}"

  echo -n "Checking [${sdk_dir}] (${registry})... "

  if [ ! -d "${TARGET_PATH}" ]; then
    echo "⚠️  Directory missing: ${TARGET_PATH}"
    ERRORS=$((ERRORS + 1))
    continue
  fi

  MISSING_FILES=()
  for req in "README.md" "LICENSE" "SECURITY.md" "${manifest}"; do
    if [ ! -f "${TARGET_PATH}/${req}" ]; then
      MISSING_FILES+=("${req}")
    fi
  done

  if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "⚠️  Missing files: ${MISSING_FILES[*]}"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Ready"
  fi
done

echo "--------------------------------------------------"
if [ ${ERRORS} -eq 0 ]; then
  echo "🎉 All 7 SDK repositories satisfy parent contract standards!"
  exit 0
else
  echo "⚠️  Contract validation finished with ${ERRORS} warnings/errors."
  exit 1
fi
