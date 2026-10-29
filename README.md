# ci-whisper

Read a failed CI log, get one paragraph: the first real error, how it led to the red build, and what to fix.

```bash
gh run view 123456 --log-failed | ci-whisper
```

```
FIRST REAL ERROR
  line 12: FAILED tests/test_render.py::test_render_header - AssertionError

CAUSAL CHAIN
  root         line 12: FAILED tests/test_render.py::test_render_header - AssertionError
  github-error line 13: ##[error]Process completed with exit code 1.

SUGGESTED FIX
  tests/test_render.py::test_render_header failed with AssertionError.
  Run it alone to reproduce, then fix the expectation or the code it exercises.

Scanned 13 lines, 2 signals.
```

## Install

```bash
pipx install ci-whisper
```

No dependencies. Python 3.9+.

## Usage

```bash
# from a run id (uses the gh CLI you already have)
ci-whisper --gh 1234567

# from a saved log
gh run view 1234567 --log-failed > failed.log
ci-whisper --file failed.log

# piped
cat failed.log | ci-whisper

# machine-readable, for agents and scripts
ci-whisper --file failed.log --json

# as an agent skill: paste the log and say "diagnose this CI failure"
```

Exit code is `0` when an error was found, `1` when the log contains no error signal.

## Why it exists

A failed CI log is 10,000 lines of setup noise, timestamps, and then fifteen cascading
exit codes. The last line is never the cause. The first line that matters is usually
sitting in the middle, wrapped in a group, and by the time you find it you have forgotten
what you were doing.

ci-whisper ranks signals instead of printing them:

- **Exceptions beat their prefaces.** `ModuleNotFoundError: No module named 'yaml'` outranks
  the `Traceback (most recent call last):` line above it, because the second is a header.
- **Cascades are demoted.** `##[error]Process completed with exit code 1.` is reported as a
  consequence, not a cause.
- **Noise is dropped.** Warnings, deprecation notices, download progress, and
  `0 failed` summaries never become the root cause.
- **Every claim is cited.** Each line in the report carries the original log line number, so
  you can jump straight to it.

## What it does not do

- It does not call an LLM and does not send your logs anywhere. This is a local parser.
- It does not know your codebase, so the suggested fix is the first action, not the final answer.

## How it works

1. Strip ANSI escapes and ISO timestamps, keeping line numbers.
2. Classify each line against structured error patterns, after dropping known noise.
3. Rank: exception and module errors (4), traceback/test/compiler errors (3), package manager and
   GitHub annotations (2), bare exit codes (1). Highest rank wins; ties break by earliest line.
4. Build the chain: the winner, the causal hints that follow it, and the first three downstream signals.
5. Map the winner to a fix rule (`ModuleNotFoundError`, `ERESOLVE`, `EADDRINUSE`, `EACCES`,
   timeouts, OOM kills, syntax errors, assertion failures).

## Supported today

GitHub Actions logs in the `gh run view --log-failed` shape. The classifier is line-based, so
most other CI providers work if you strip their prefixes; provider-specific adapters are welcome.

## Tests

```bash
python -m pytest -q
```

Eight tests over real failure shapes: pytest assertion, npm ERESOLVE, Python traceback,
noise-only log, exit-code-only log, citation accuracy, and chain ordering.

## Contributing

New fix rules and CI providers are the most useful additions. Add a fixture log under
`tests/fixtures/`, a test that asserts the diagnosis, and open a PR. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
