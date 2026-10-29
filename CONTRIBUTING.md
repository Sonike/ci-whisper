# Contributing

## The most useful contributions

1. **New fix rules.** A failure mode you have debugged twice belongs in `FIX_RULES` with a fixture.
2. **CI provider adapters.** Stripping another provider's prefixes is welcome; keep it in `patterns.py`.
3. **Noise patterns.** If the tool reports something that is never a root cause, add the pattern to `NOISE`.

## Rules

- Every behaviour change needs a fixture log and a test asserting the diagnosis.
- Keep the tool dependency-free. It must run from a bare `python` on a CI runner.
- Never make the tool send logs anywhere. Local parsing is the product.
- Cite line numbers in every output path.

## Running tests

```bash
python -m pytest -q
```
