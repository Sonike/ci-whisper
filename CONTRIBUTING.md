# Contributing

## Adding a rule

Rules live in `ci_whisper/patterns.py`:

- `STRONG_ERRORS` — `(kind, compiled regex)` pairs
- `NOISE` — things that look like errors and are not
- `FIX_RULES` — `(needle, advice)` mapped to a suggested fix

Add a **fixture** in `tests/fixtures/` using a realistic slice of the log, then assert two things:
the root cause line number, and that the fix text names the actual culprit. A rule without a failing
fixture is a guess.

## Running the tests

```bash
python -m pytest -q
```

CI runs the suite on Python 3.9 and 3.12 plus a CLI smoke test against a fixture.

## Rules of the road

- Never let a consequence outrank its cause (exit codes are always weakest).
- Keep the zero-dependency promise; stdlib only.
- Support GitHub Actions first. Other providers are welcome as fixtures plus rules, not as a rewrite.
- Output must stay honest: if nothing matches, say so and exit 1. Do not invent a diagnosis.

## Pull requests

One rule family per PR, fixture included, `pytest` green.
