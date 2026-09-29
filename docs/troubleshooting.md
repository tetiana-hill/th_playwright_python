# Running and investigating failures

## Setup problems

- **`python` is not found:** install Python 3.12 and make it available on PATH. On Windows the Python launcher may expose it as `py -3.12`.
- **PowerShell refuses activation:** use `.\.venv\Scripts\python.exe -m ...` directly.
- **Browser executable missing after an update:** run `python -m playwright install chromium firefox` again in the same environment.
- **Linux system library errors:** use `python -m playwright install --with-deps chromium firefox`.
- **Unknown pytest CLI options:** confirm that the virtual environment is active and run `python -m pip install -r requirements.txt`.
- **DNS, TLS or timeout errors:** check the public demo's availability and your network. Do not disable TLS verification or replace a failed scenario with a pass.

## Investigate a failing case

1. Open the failing browser job in [GitHub Actions](https://github.com/tetiana-hill/th_playwright_python/actions/workflows/ui-tests.yml). Check whether the failure happened during setup, browser installation or test execution.
2. Read the pytest assertion and expected/actual values in the test step or `reports/junit.xml`.
3. Download the matching `ui-results-<browser>-<attempt>` artifact. Look at the failure screenshot, then open its trace with `python -m playwright show-trace path/to/trace.zip`.
4. Inspect the action log, DOM snapshots, console and network around the failing action. A wrong locator, stale test data and an unavailable site require different fixes.
5. Reproduce the affected test with its file or `-k` filter and the same browser. For example:

   ```bash
   python -m pytest tests/test_checkout.py -k complete_two_product --browser firefox --headed
   ```

6. Fix the root cause, run the relevant case, then the full matrix. Preserve real defects and infrastructure failures as failures until resolved; do not weaken assertions solely to make the badge green.

For a local investigation, `--tracing=on --screenshot=on` also keeps evidence for passing tests. The defaults keep only failed-test traces and screenshots, under `test-results/`. Download CI artifacts within their 14-day retention window. Reports, traces, screenshots and local environments are ignored by Git.

There is deliberately no automatic retry policy. If a transient external outage is confirmed, rerun the affected CI job after recovery and retain the first run as evidence.

## Adding a scenario

Add the business expectation in `tests/`, reuse an existing page/component, and add a locator/action to `pages/` only if needed. Give parameters meaningful IDs. Update the scenario matrix and test counts when adding cases. Avoid shared mutable data, sleeps, ordering dependencies and selectors tied to row position.
