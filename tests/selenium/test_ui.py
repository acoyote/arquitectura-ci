import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_mercadolibre_ui(driver):
    try:
        driver.get("https://www.mercadolibre.com")
        wait = WebDriverWait(driver, 10)

        # Seleccionar México
        mexico_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://www.mercadolibre.com.mx']")))
        mexico_link.click()

        # Buscar "playstation 5"
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "as_word")))
        search_box.send_keys("playstation 5")
        search_box.send_keys(Keys.RETURN)

        # Filtro por "Nuevo"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Nuevo']"))).click()
        time.sleep(2)

        # Filtro por "CDMX"
        location_xpath = "//span[contains(text(),'Ciudad de México')]"
        wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath))).click()
        time.sleep(2)

        # Ordenar por "Mayor precio"
        sort_dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "andes-dropdown__trigger")))
        sort_dropdown.click()
        higher_price_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@class='andes-list__item']//span[text()='Mayor precio']")))
        higher_price_option.click()
        time.sleep(3)

        # Obtener los primeros 5 productos
        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-result__wrapper")))[:5]

        print("\n🎮 Primeros 5 productos encontrados:\n")
        for i, product in enumerate(products, start=1):
            title = product.find_element(By.CSS_SELECTOR, "h2.ui-search-item__title").text
            price = product.find_element(By.CSS_SELECTOR, "span.price-tag-fraction").text
            print(f"{i}. {title} - ${price}")

    except Exception as e:
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot("screenshots/error.png")
        pytest.fail(f"Test failed: {e}")
