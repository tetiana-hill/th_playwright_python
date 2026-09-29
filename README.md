# Python + Playwright | QA Automation Portfolio

[![UI Tests](https://github.com/tetiana-hill/th_playwright_python/actions/workflows/ui-tests.yml/badge.svg)](https://github.com/tetiana-hill/th_playwright_python/actions/workflows/ui-tests.yml)

**Tetiana Hil — QA Engineer with 6+ years of commercial QA experience, strong backend/API testing skills, and a growing focus on Python test automation.**

This personal portfolio project applies QA test design to browser automation: meaningful assertions, independent tests, negative coverage, readable page objects, and actionable failure evidence. It demonstrates current automation skills; the 6+ years refer to commercial QA experience, not 6+ years of commercial Python/Playwright automation.

The suite tests [SauceDemo](https://www.saucedemo.com/), the public Sauce Labs sample store. It complements my [API testing portfolio](https://github.com/tetiana-hill/th_api_testing).

## What this project demonstrates

- **18 scenarios per browser** covering authentication, sorting, cart state and checkout.
- **A complete purchase journey** checking product identity, prices, quantities, subtotal, tax, total, confirmation and an empty cart afterward.
- **Negative cases** for invalid credentials, a locked account, anonymous access and missing checkout information.
- **Maintainable Python:** small page objects, shared product/header components, typed fixtures and parameterized tests.
- **Isolation:** a fresh browser context for each test, with no dependency on execution order.
- **GitHub Actions:** Python quality checks followed by Chromium and Firefox runs, with JUnit results and failure screenshots/traces.

## Quick start

Use **Python 3.12** (the version used in CI), Git and an internet connection. No paid accounts or private credentials are required.

```bash
git clone https://github.com/tetiana-hill/th_playwright_python.git
cd th_playwright_python
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and run:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium firefox
python -m pytest
```

The default run is headless Chromium. On Linux, install browser system dependencies with `python -m playwright install --with-deps chromium firefox`. If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` in place of `python`; changing the execution policy is unnecessary.

## Useful commands

```bash
# Critical login + complete purchase (2 scenarios per browser)
python -m pytest -m smoke

# Full browser matrix (36 executions)
python -m pytest --browser chromium --browser firefox

# Watch the purchase journey
python -m pytest -m e2e --headed

# Negative cases only
python -m pytest -m negative

# JUnit report, suitable for CI
python -m pytest --junitxml=reports/junit.xml

# Same code checks as CI
python -m ruff check .
python -m ruff format --check .
```

`--base-url` can point to another deployment of the **same SauceDemo app**, for example `python -m pytest --base-url=http://localhost:3000`. The tests are not generic checks for arbitrary websites.

## Project layout

```text
pages/
  login.py           # Login actions and controls
  inventory.py       # Catalog and sorting
  cart.py            # Cart navigation
  checkout.py        # Customer information, overview and completion
  components.py      # Shared header and exact-name product rows
tests/
  conftest.py        # Selectors, browser settings and test prerequisites
  data.py            # Public demo accounts and expected products
  test_auth.py
  test_inventory.py
  test_cart.py
  test_checkout.py
docs/
  test-strategy.md    # Scope, risks and design decisions
  test-cases.md       # Scenario-to-code mapping and expected outcomes
  troubleshooting.md # Failure evidence and local debugging
.github/workflows/ui-tests.yml
pyproject.toml       # Pytest options, markers and Ruff configuration
requirements.txt    # Pinned direct dependencies
```

Page objects contain locators and actions. Tests contain business expectations; fixtures check their own prerequisites. `ProductList` is reused across catalog, cart and checkout so product selection stays consistent without a large inheritance framework.

## CI and failure evidence

Open [UI Tests](https://github.com/tetiana-hill/th_playwright_python/actions/workflows/ui-tests.yml) for the current result. CI runs on pushes to `main`, pull requests targeting `main`, and manual dispatch. Both browser jobs must pass; there are no automatic test retries or allowed failures.

Each browser job uploads `ui-results-<browser>-<attempt>` for 14 days:

- `reports/junit.xml`: pass/fail results and assertion details.
- `test-results/`: full-page screenshots and Playwright traces retained for failed tests.

A passing run normally has only the JUnit report. Browser startup failures may occur before a screenshot or trace can be created. After downloading and extracting a failure artifact, open its trace locally:

```bash
python -m playwright show-trace path/to/trace.zip
```

See [troubleshooting](docs/troubleshooting.md) for a practical failure triage workflow.

## Scope and limits

SauceDemo is a public training application. The purchase is simulated; this suite does not validate real payments, backend order persistence or server-side authorization. Its UI access checks demonstrate expected demo navigation behavior, not a security audit.

The suite covers the standard catalog and the documented `locked_out_user`. Other intentionally faulty demo accounts, dynamic catalog, mobile, WebKit, accessibility, visual regression and performance testing are outside this MVP. Demo availability and upstream UI changes can cause genuine failures that require investigation.

The product catalog, displayed error messages and 8% demo tax are explicit test expectations. A legitimate upstream change should lead to a reviewed test-data update, not a relaxed assertion.

Read the [test strategy](docs/test-strategy.md) and [scenario matrix](docs/test-cases.md) for the reasoning behind the coverage.

## References

- [Sauce Labs sample application source](https://github.com/saucelabs/sample-app-web)
- [Playwright pytest plugin and fixtures](https://playwright.dev/python/docs/test-runners)
- [Playwright assertions](https://playwright.dev/python/docs/test-assertions)

Maintained as a personal QA automation portfolio by **Tetiana Hil**.
