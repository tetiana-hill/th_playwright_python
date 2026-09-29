# Test strategy

## Objective

Provide a small, reviewable regression suite for the highest-value customer paths in SauceDemo. Show how commercial QA test-design experience translates into maintainable Python browser automation.

## Risk-based scope

| Risk | Coverage | Priority |
| --- | --- | --- |
| Valid customer cannot access the store | Successful login and inventory visibility | High |
| Rejected credentials still expose inventory | Incorrect password, locked user, required fields | High |
| Anonymous or logged-out user reopens inventory | Direct navigation before login and after logout | High |
| Cart silently loses or retains the wrong products | Add/remove two products, empty state, reload persistence | High |
| Checkout loses product identity or miscalculates money | Two-product journey; item, quantity, price, subtotal, tax, total | High |
| Incomplete customer data proceeds to overview | Each required field missing independently | High |
| User loses cart when cancelling checkout | Cancel information step and inspect cart | Medium |
| Catalog ordering misleads the customer | Both name orders and both numeric price orders | Medium |

The empty string is the covered required-field boundary. Postal-format rules and field-length limits are not claimed because this demo does not provide those requirements.

## Test architecture

Tests use the official `pytest-playwright` plugin and synchronous Python API. The plugin owns browser/context/page lifetime and diagnostic artifacts. Each test gets a fresh context; session-scoped browser reuse does not share cookies or local storage.

UI login is used for setup so the suite needs no invented backend API or direct state manipulation. At this size the extra setup is acceptable. A larger suite could reuse authenticated storage state per worker, provided cart isolation remains explicit.

Page objects expose actions and locators. Assertions remain in tests, except readiness checks in fixtures. Shared `Header` and `ProductList` components avoid duplicated selectors. Products are selected by exact names; row position is not used as identity.

Locators use the app's `data-test` attributes and accessible button roles. Web-first `expect` assertions retry until a bounded deadline. There are no arbitrary sleeps, forced clicks, conditional passes, automatic retries or broad exception handlers.

Sorting expectations are derived from the original complete list, then compared as a full sequence after selecting an order. This detects wrong ordering and missing/duplicate entries. Monetary expectations in the purchase scenario use independent known prices and Python `Decimal`, with the demo's 8% tax rounded to cents.

## Environments and data

- Target: `https://www.saucedemo.com`, standard catalog.
- Python 3.12; Chromium and Firefox from the pinned Playwright release.
- Local and CI use the same pytest configuration and direct dependency versions.
- Public accounts: `standard_user`, `locked_out_user`; published password: `secret_sauce`.
- Synthetic checkout identity: `Test Customer`, postal code `12345`.
- Fresh browser state removes any need to reset shared backend records.
- Tests run sequentially inside each browser job to keep traffic modest; the two CI jobs are independent.

Direct dependencies are pinned. Transitive dependencies are resolved by pip, so this is not a complete dependency lock. Dependabot proposes monthly updates, which must pass CI before acceptance. GitHub Actions are pinned to commit SHAs.

## Entry and exit criteria

Entry: target reachable, dependencies and browser binaries installed, standard demo account available.

Exit: quality checks pass, all 18 scenarios pass in each CI browser, no skipped/expected-failure cases hide regressions, and results are attached to the run. A green run is evidence for that commit and environment only.

For a failure, retain the assertion, identify whether the cause is test code, infrastructure, an intentional upstream change or application behavior, and fix only the appropriate layer. A later successful rerun does not explain an earlier failure; record the cause when it is known.

## Limitations and possible next steps

This is UI functional testing of a training store. It does not establish backend correctness or production security. Native mobile, accessibility audits, visual baselines, payment integrations and load testing require separate tools and acceptance criteria.

Potential extensions after the MVP: product detail checks, accessibility coverage, and API/UI integration on an application with a real documented backend. These are ideas, not implemented claims.
