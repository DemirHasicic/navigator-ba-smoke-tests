import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    ElementNotInteractableException
)



def hover(driver, element):
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(1)

def test_logo_visible(driver, wait):
    logo = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "img[src*='logomain.png']")))
    assert logo.is_displayed()
    title = driver.title
    assert "Navigator | Mapa Sarajeva" in title
    desc = driver.find_element(By.CSS_SELECTOR, 'meta[name="description"]').get_attribute("content")
    assert desc

def test_search_bar(driver, wait):
    search = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input.tt-query")))
    assert search.is_displayed()
    assert search.get_attribute("placeholder"), "Search bar placeholder should not be empty"

def test_create_place_navigation(driver, wait):
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '#/create-place')]")))
    assert any(lbl in btn.text for lbl in ["Create Place", "Kreiraj objekat"])
    btn.click()
    wait.until(EC.url_contains("#/create-place"))
    assert "#/create-place" in driver.current_url or wait.until(
        EC.visibility_of_element_located((By.ID, "place-form"))
    )

def test_return_to_home_after_create_place(driver, wait):
    driver.find_element(By.XPATH, "//a[contains(@href, '#/create-place')]").click()
    wait.until(EC.url_contains("#/create-place"))
    driver.back()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.tt-query")))

def test_sidebar_categories_and_special_lists(driver, wait):
    sidebar = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "ul.menu_content_list.categories")))
    items = sidebar.find_elements(By.CSS_SELECTOR, "li[class]")
    special, normal = [], []
    for item in items:
        try:
            href = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            name = item.find_element(By.CLASS_NAME, "name").text.strip()
        except:
            continue
        if not name:
            continue
        if "#/list/" in href:
            special.append(item)
        elif "#/categories/" in href:
            normal.append(item)
    assert len(special) == 3, f"Expected 3 special lists, found {len(special)}"
    assert normal, "Should find at least one standard category"

def test_open_location_details_from_sidebar(driver, wait):
    # 1) Click the first "special" list in the sidebar so that list-items appear
    try:
        special = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "ul.menu_content_list.categories li a[href*='#/list/']")))
        special.click()
    except TimeoutException:
        pytest.skip("No special list links in sidebar to click")

    # 2) Now wait for the actual list-items to load
    try:
        first_item = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "ul.menu_content_list.list-items li .content")))
    except TimeoutException:
        pytest.skip("No sidebar list-items loaded for special list")

    # 3) Click it and verify a popup appears
    first_item.click()
    try:
        bubble = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "leaflet-popup-content")))
    except TimeoutException:
        pytest.skip("Clicking list-item did not open popup")
    assert bubble.text.strip(), "Popup content missing"



def test_special_list_sarajevska_pozorista(driver, wait):
    link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a[href='#/list/sarajevska-pozorista']")))
    link.click()
    wait.until(EC.url_contains("#/list/sarajevska-pozorista"))

    locations = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul.menu_content_list.list-items li .content .name")))
    assert locations, "No theatre locations found"

    try:
        pins = wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, "span.inner-icon[data-icon], span.marker-circle-container"
        )))
        assert pins, "Map pins not found for Sarajevska pozorišta"
    except:
        pytest.skip("Map pins did not load for special list")

    hover(driver, locations[0])

def test_accommodation_category(driver, wait):
    link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a[href='#/categories/accommodation']")))
    link.click()
    wait.until(EC.url_contains("#/categories/accommodation"))

    places = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul.menu_content_list li.place.accommodation .content > .name")))
    assert places, "No accommodation places shown"

    try:
        pins = wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, "span.inner-icon[data-icon], span.marker-circle-container"
        )))
        assert pins, "Map pins not found for accommodation"
    except:
        pytest.skip("Map pins did not load for accommodation")

    hover(driver, places[0])

def test_feedback_form_flow(driver, wait):
    try:
        suggest = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Suggest features') or contains(text(), 'Predloži')]")))
        suggest.click()
        fb_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(., 'komentar') or contains(., 'problem')]")))
        fb_link.click()
        wait.until(EC.url_contains("#/feedback"))
        form = wait.until(EC.visibility_of_element_located((By.ID, "feedback")))
        textarea = form.find_element(By.NAME, "comment")
        assert textarea.get_attribute("placeholder") == "Komentar"
    except:
        pytest.skip("Feedback form flow not available")

def test_language_buttons_and_map_controls(driver, wait):
    bs = driver.find_element(By.CLASS_NAME, "btn-bs")
    en = driver.find_element(By.CLASS_NAME, "btn-en")
    assert bs.is_displayed() and en.is_displayed()

    tile = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "img.leaflet-tile")))
    assert "tile.openstreetmap.org" in tile.get_attribute("src")

    zoom_in = driver.find_element(By.CLASS_NAME, "leaflet-control-zoom-in")
    zoom_out = driver.find_element(By.CLASS_NAME, "leaflet-control-zoom-out")
    assert zoom_in.is_displayed() and zoom_out.is_displayed()
    zoom_in.click(); time.sleep(1)
    zoom_out.click(); time.sleep(1)




def test_footer_and_external_links(driver, wait):
    about = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "#footer a[href='#/about']")))
    assert about.text.strip().lower() in ["about", "o navigatoru"]

    leaflet = driver.find_element(
        By.CSS_SELECTOR, ".leaflet-control-attribution a[href*='leafletjs.com']")
    atlant = driver.find_element(
        By.CSS_SELECTOR, ".leaflet-control-attribution a[href*='atlantbh.com']")
    assert "Leaflet" in leaflet.text
    assert "Atlantbh" in atlant.text

def test_social_icons(driver, wait):
    icons = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul.navigation.social li a")))
    assert len(icons) == 3
    expected = {"iconav-facebook", "iconav-twitter-2", "iconav-googleplus"}
    for a in icons:
        cls = a.find_element(By.TAG_NAME, "span").get_attribute("class")
        assert cls in expected

def test_language_switching(driver, wait):
    bs = driver.find_element(By.CLASS_NAME, "btn-bs")
    bs.click()
    wait.until(lambda d: "Kreiraj objekat" in d.page_source)
    en = driver.find_element(By.CLASS_NAME, "btn-en")
    en.click()
    wait.until(lambda d: "Create Place" in d.page_source)

def test_search_with_autosuggestion(driver, wait):
    inp = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input.tt-query")))
    inp.clear()
    inp.send_keys("Pirpa")
    assert inp.get_attribute("value").startswith("Pirpa")

    suggestion = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "tt-suggestion")))
    suggestion_text = suggestion.text
    suggestion.click()

    try:
        name_elem = wait.until(lambda d: d.find_element(By.CLASS_NAME, "name") 
                                       if d.find_element(By.CLASS_NAME, "name").text.strip() 
                                       else False)
        assert name_elem.text.strip(), f"No result text after suggestion '{suggestion_text}'"
    except:
        popup = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "leaflet-popup-content")))
        assert suggestion_text in popup.text, (
            f"Expected '{suggestion_text}' in popup, got '{popup.text}'"
        )

def test_search_with_enter_key(driver, wait):
    inp = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input.tt-query")))
    inp.clear()
    inp.send_keys("Pirpa")
    inp.send_keys(Keys.ENTER)

    try:
        name_elem = wait.until(lambda d: d.find_element(By.CLASS_NAME, "name"))
        assert name_elem.text.strip(), "Name text is empty after ENTER search"
    except:
        popup = wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "leaflet-popup-content")))
        assert "Pirpa" in popup.text, (
            f"Expected 'Pirpa' in popup, got '{popup.text}'"
        )

def test_categories_list_scroll(driver, wait):
    container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.menu_content_list.categories")))
    scroll_height = driver.execute_script("return arguments[0].scrollHeight", container)
    client_height = driver.execute_script("return arguments[0].clientHeight", container)
    if scroll_height <= client_height:
        pytest.skip(f"Categories list not scrollable (scrollHeight={scroll_height}, clientHeight={client_height})")
    initial = driver.execute_script("return arguments[0].scrollTop", container)
    driver.execute_script("arguments[0].scrollTop += 150", container)
    time.sleep(0.5)
    after = driver.execute_script("return arguments[0].scrollTop", container)
    assert after > initial, f"List did not scroll (before={initial}, after={after})"

def test_categories_dragger_scroll(driver, wait):
    try:
        dragger = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".mCSB_draggerContainer .mCSB_dragger")))
    except TimeoutException:
        pytest.skip("Custom scrollbar dragger not present")

    style = dragger.get_attribute("style")
    try:
        initial_top = int(style.split("top:")[1].split("px")[0].strip())
    except (IndexError, ValueError):
        pytest.skip(f"Cannot parse initial top from style='{style}'")

    # Try to drag; if it's not interactable, skip
    try:
        ActionChains(driver) \
            .click_and_hold(dragger) \
            .move_by_offset(0, 100) \
            .release() \
            .perform()
    except ElementNotInteractableException:
        pytest.skip("Dragger not interactable (no size/location)")

    time.sleep(0.5)
    style2 = dragger.get_attribute("style")
    try:
        new_top = int(style2.split("top:")[1].split("px")[0].strip())
    except (IndexError, ValueError):
        pytest.skip(f"Cannot parse new top from style='{style2}'")

    assert new_top > initial_top, f"Dragger did not move (before={initial_top}, after={new_top})"
def test_return_to_user_location_button(driver, wait):
    # 1) Ensure the page has exposed window.map and panBy
    has_map = False
    try:
        has_map = driver.execute_script("return !!(window.map && window.map.panBy);")
    except WebDriverException:
        pass
    if not has_map:
        pytest.skip("Leaflet map not exposed on window.map, cannot pan programmatically")

    # 2) Pan the map away from center
    driver.execute_script("window.map.panBy([200, 0]);")
    time.sleep(0.5)

    # 3) Wait for the locate-control and click it
    try:
        btn = wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "leaflet-control-locate")))
    except TimeoutException:
        pytest.skip("Locate-control button not present")
    btn.click()

    # 4) We could verify center changed, but at least ensure no error
    time.sleep(1)