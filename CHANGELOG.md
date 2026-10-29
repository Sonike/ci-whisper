# Changelog

## v0.1.0 - 2026-10-29

- Read a failed CI log from stdin, `--file`, or `--gh <run-id>` and report the
  first real error, its causal chain, and a suggested fix, citing original log
  line numbers instead of line numbers in a cleaned copy.
- Signal ranking so consequences do not masquerade as causes: exceptions and
  module errors (4) outrank the bare `Traceback` header, test and compiler
  failures (3), then npm and GitHub annotations (2), then a lone exit code (1).
- Go test failures recognized at strength 3 with package-name recovery, and an
  earlier compiler diagnostic keeps precedence over a later test failure.
  Contributed by @Sonike in #3.
- `--json` for machine consumption; exit 1 when no error signal is found at all.
- 13 tests over real log shapes (pytest, npm, traceback, Go).
- Install: `pipx install git+https://github.com/mgkvibez/ci-whisper.git`.
