# Scenario matrix

There are **18 collected cases per browser**: 7 authentication, 4 sorting, 2 cart and 5 checkout. Parameterized rows below represent separate pytest cases.

All cases start in a fresh browser context. Inventory/cart/checkout cases use the standard public demo account unless stated otherwise.

| ID | Scenario / action | Expected result | Automated case |
| --- | --- | --- | --- |
| AUTH-01 | Log in with standard credentials | Inventory URL, Products title, six products | `test_standard_user_can_log_in` |
| AUTH-02 | Submit incorrect password | Exact rejection message, login visible, no product rows | `test_login_rejects_invalid_input[invalid-password]` |
| AUTH-03 | Submit locked account | Locked-out message, no product rows | `test_login_rejects_invalid_input[locked-out-user]` |
| AUTH-04 | Submit empty username | Username required, no product rows | `test_login_rejects_invalid_input[empty-username]` |
| AUTH-05 | Submit empty password | Password required, no product rows | `test_login_rejects_invalid_input[empty-password]` |
| AUTH-06 | Log out, then navigate to inventory URL | Login shown, access rejected, no product rows | `test_logout_prevents_inventory_reentry` |
| AUTH-07 | Open inventory URL anonymously | Exact access message, login shown, no product rows | `test_anonymous_user_cannot_open_inventory` |
| INV-01 | Sort price low to high | Complete list in numeric ascending order | `test_sort_products_by_price[low-to-high]` |
| INV-02 | Sort price high to low | Complete list in numeric descending order | `test_sort_products_by_price[high-to-low]` |
| INV-03 | Switch from Z-A to A-Z | Complete list in alphabetical ascending order | `test_sort_products_by_name[a-to-z]` |
| INV-04 | Switch from A-Z to Z-A | Complete list in alphabetical descending order | `test_sort_products_by_name[z-to-a]` |
| CART-01 | Add two products, remove each, continue shopping | Correct items and badge counts; empty cart; Add to cart restored | `test_cart_add_remove_keeps_product_and_badge_in_sync` |
| CART-02 | Add backpack, open cart, reload | Same item, price, quantity and badge after reload | `test_cart_survives_page_reload` |
| CHK-01 | Continue with first name missing | Exact required-field error; remain on information step; cart kept | `test_checkout_requires_customer_information[first-name]` |
| CHK-02 | Continue with last name missing | Exact required-field error; remain on information step; cart kept | `test_checkout_requires_customer_information[last-name]` |
| CHK-03 | Continue with postal code missing | Exact required-field error; remain on information step; cart kept | `test_checkout_requires_customer_information[postal-code]` |
| CHK-04 | Cancel after filling checkout information | Return to cart with original item and badge | `test_cancel_checkout_preserves_cart` |
| E2E-01 | Login → two products → cart → customer info → overview → finish | Correct items/quantities/prices; $39.98 subtotal, $3.20 tax, $43.18 total; confirmation; empty cart | `test_customer_can_complete_two_product_purchase` |

`AUTH-01` and `E2E-01` form the smoke suite. `E2E-01` also has the `e2e` marker. `AUTH-02` through `AUTH-05`, `AUTH-07` and `CHK-01` through `CHK-03` have the `negative` marker. Browser names are also included in actual collected pytest node IDs.

Run `python -m pytest --collect-only -q` to inspect executable cases. Run results belong in GitHub Actions/JUnit, not manually maintained pass/fail labels in this matrix.
