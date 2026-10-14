#!/usr/bin/env bash
# HUMAN REVIEW ONLY. NOT EXECUTED BY THE IMPLEMENTATION AGENT.
# First resolve/document the inherited image-dependent regression coverage gap.
# Run each section manually after independent QC; do not run as an unattended script.

# Inspect your own working tree; stop on unrelated changes or mismatched authority.
git branch --show-current
git rev-parse HEAD HEAD^
git status --porcelain
git verify-commit --raw d15865167b4e3c454e398bd498d9d681103096f7
git hash-object docs/p0a0_hebrew_projection_source_identity_and_synthetic_pilot_protocol_v0.9.md
sha256sum docs/p0a0_hebrew_projection_source_identity_and_synthetic_pilot_protocol_v0.9.md
# Expected branch: hebrew-projection-capacity-v0.9
# Expected HEAD: d15865167b4e3c454e398bd498d9d681103096f7
# Expected parent: 8bf0babfd91bdefb0792e93707fd0b0da1c09767
# Expected protocol blob: 0f8b663bfe2432685c9320a00c80fd6bcf436e38
# Expected protocol SHA256: afee667eb578e329e80b8d28dc071ebebab3ae75a2e053b1f67d2c68f037743b
# Verify SHA256SUMS in the extracted package before transferring reviewed additions.
# No registered pilot invocation belongs to this freeze stage.

# Optional repeat of safe regression subset ONLY after reviewing inherited tests
# for local source availability. Both known image-opening tests excluded explicitly:
# PYTHONPATH=src MPLBACKEND=Agg python -m pytest -q tests \
#   --deselect=tests/test_arm_of_god_diagram_source_preparation.py::test_prepared_pngs_match_manifest_hashes \
#   --deselect=tests/test_first_hand_expanded_neutral_geometry_audit.py::test_overlay_renders_from_verified_prepared_crop
# Amendment run completed: 1281 passed, 2 deselected; original failure log retained.

# After independent QC: stage ONLY these exact reviewed additions.
git add -- \
  docs/v0_9/p0a0_human_freeze_commands.sh \
  docs/v0_9/p0a0_implementation_specification.md \
  registered_pilots/p0a0/cases.py \
  registered_pilots/p0a0/fixture_config.json \
  registered_pilots/p0a0/fixtures.py \
  registered_pilots/p0a0/implementation_manifest.json \
  reports/v0_9/p0a0_implementation/AMENDMENT_QC.md \
  reports/v0_9/p0a0_implementation/QC_README.md \
  reports/v0_9/p0a0_implementation/amendment_changes.json \
  reports/v0_9/p0a0_implementation/amendment_controlled_regressions.log \
  reports/v0_9/p0a0_implementation/amendment_dev_checks.log \
  reports/v0_9/p0a0_implementation/amendment_environment.json \
  reports/v0_9/p0a0_implementation/amendment_source.diff \
  reports/v0_9/p0a0_implementation/amendment_static_preservation_checks.json \
  reports/v0_9/p0a0_implementation/changed_paths.txt \
  reports/v0_9/p0a0_implementation/collection.log \
  reports/v0_9/p0a0_implementation/dev_checks.log \
  reports/v0_9/p0a0_implementation/dev_checks_final.log \
  reports/v0_9/p0a0_implementation/environment.json \
  reports/v0_9/p0a0_implementation/inherited_baseline.log \
  reports/v0_9/p0a0_implementation/inherited_baseline_after_pytest_install.log \
  reports/v0_9/p0a0_implementation/integrity.json \
  reports/v0_9/p0a0_implementation/pip_freeze.txt \
  reports/v0_9/p0a0_implementation/static_checks.json \
  scripts/p0a0_registered_pilot.py \
  src/meru_geometry/p0a0/__init__.py \
  src/meru_geometry/p0a0/boundaries.py \
  src/meru_geometry/p0a0/engineering.py \
  src/meru_geometry/p0a0/oracles.py \
  tests/test_p0a0_dev.py \
  tests/test_p0a0_qc_boundaries_dev.py

git diff --cached --check
git diff --cached --stat
git diff --cached
# STOP FOR HUMAN REVIEW of the staged diff. Amendments require regenerated hashes.
# Only after that review and approval:
git commit -S -m "Freeze P0A0 implementation-only synthetic fixtures and oracles"
git verify-commit --raw HEAD
# Require exact signing fingerprint: D4EC014EEFCC90E619D2AA59A91239ABCF512130
git rev-parse HEAD HEAD^
git status --porcelain
# No push suggested or performed. Separate later pilot authorization is required.
