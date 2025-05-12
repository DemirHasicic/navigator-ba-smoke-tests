# Navigator.ba Smoke Test Suite

This repository contains:

1. **Manual Test Cases**  #
   - `Test_cases.pdf` – the full set of manual test-cases (positive & negative) for https://www.navigator.ba  
   - A smoke-test subset was identified and automated.
   - Bugs were also recorded

2. **Automated Smoke Tests**  
   - `Smoke_test.py` – pytest file with all automated smoke tests  
   - `conftest.py` – pytest fixtures, setup/teardown, and custom reporting hook  

3. **Requirements**  
   - `requirements.txt` – Python dependencies  

---
## 📑 Manual Test-Case Analysis

All test cases were reviewed and classified accordingly:

- **Positive test cases** (core happy-paths & bug-validation positives):  
  NAV-00, NAV-01, …, MAP-05, CLAIM-04, SUGG-01, …, CREATE-03  
- **Negative test cases** (validation failures, error-paths):  
  NAV-26, NAV-29, CLAIM-01…03, SUGG-03…09, CREATE-01  

From those, these were selected as a **smoke** subset (critical end-to-end flows that must always work):

| Smoke ID | Description                                      |
|----------|--------------------------------------------------|
| NAV-00   | Homepage loads & main elements                   |
| NAV-08   | Category filtering → correct pins & sidebar list |
| NAV-09   | Sidebar & popup scrolling                        |
| NAV-10A  | Autocomplete suggestion navigation               |
| NAV-10B  | Enter-key search navigation                      |
| NAV-12   | Open location details from sidebar               |
| MAP-01   | Zoom in/out controls                             |
| MAP-02   | Map panning (drag)                               |
| MAP-03   | “Locate me” button                               |

---

## ⚙️ Automation Details

- **Language & Framework**: Python 3.8+, pytest  
- **Browser Automation**: Selenium WebDriver with ChromeDriver  
- **Key Files**:
  - **`conftest.py`**  
    - Defines a module-scoped `driver()` fixture that starts Chrome once per session  
    - A function-scoped `open_home()` fixture that returns to the homepage before each test  
    - A `wait()` fixture for a 10 s `WebDriverWait`  
    - A custom `pytest_runtest_logreport` hook to print `PASSED`/`SKIPPED`/`FAILED` on each test

  - **`Smoke_test.py`**  
    - Covers all smoke flows above plus some extras (logo/title/meta check, map-scrolling, sidebar dragging)  
    - Uses `pytest.skip()` whenever a feature isn’t present (so your CI doesn’t fail on optional features)  

---

## 🛠 Prerequisites

1. **Python 3.8+**  
2. **Google Chrome** (matching your ChromeDriver)  
3. **ChromeDriver** on your `PATH` (or specify its location via `webdriver.Chrome(executable_path=…)`)  
4. (Optional) a virtual environment tool: `venv`, `virtualenv`, etc.

---

## 🚀 Setup & Installation

```bash
# 1) Clone this repo
git clone https://github.com/DemirHasicic/navigator-ba-smoke-tests.git
cd navigator-ba-smoke-tests

# 2) Create & activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt
```````
---

## 🧪 Test Execution Summary

All automated smoke tests were executed using the following command:

```bash
pytest Smoke_test.py -s
========================================================================= test session starts =========================================================================
platform win32 -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
rootdir: C:\Users\korisnik\Desktop\Github\Automated smoke tests\Search_test
collected 18 items

Smoke_test.py
DevTools listening on ws://127.0.0.1:52397/devtools/browser/181e9e90-075c-4441-9df7-a85f5a610660
.test_logo_visible: PASSED
.test_search_bar: PASSED
.test_create_place_navigation: PASSED
.test_return_to_home_after_create_place: PASSED
.test_sidebar_categories_and_special_lists: PASSED
.test_open_location_details_from_sidebar: PASSED
.test_special_list_sarajevska_pozorista: PASSED
.test_accommodation_category: PASSED
.test_feedback_form_flow: PASSED
.test_language_buttons_and_map_controls: PASSED
.test_footer_and_external_links: PASSED
.test_social_icons: PASSED
.test_language_switching: PASSED
.test_search_with_autosuggestion: PASSED
.test_search_with_enter_key: PASSED
stest_categories_list_scroll: SKIPPED
stest_categories_dragger_scroll: SKIPPED
stest_return_to_user_location_button: SKIPPED

=================================================================== 15 passed, 3 skipped in 30.88s ====================================================================
ℹ️ Tests marked as SKIPPED correspond to optional UI features that may not appear in all environments or screen sizes (e.g., sidebar scroll dragger, "locate me" button). These are skipped gracefully to allow CI to continue.

🐞 Bug Reports
Bug reports were documented in the same file as the manual test cases (TESTCASES.pdf), and clearly labeled (e.g., CREATE-BUG-01, NAV-BUG-XX).
Example:

CREATE-BUG-01 — 500 Internal Server Error on Minimal Valid Input
Component: Create Place Form
Steps: Fill only “Name” and “Category” → Click "Create"
Expected: Object created or shown validation error
Actual: 500 Internal Server Error
Impact: User may assume object was saved when it wasn’t
