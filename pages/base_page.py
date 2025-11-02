import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class BasePage:
    def __init__(self, driver: WebDriver, wait_time: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)
        # self.base_url = os.getenv("baseURL")

    def go_to(self, url: str):
        self.driver.get(url)

    def find_element(self, selector: tuple) -> WebElement:
        return self.driver.find_element(*selector)

    def find_elements(self, selector: tuple) -> list[WebElement]:
        return self.driver.find_elements(*selector)

    def find_element_with_wait(self, selector: tuple) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(selector))

    def find_elements_with_wait(self, selector: tuple) -> list[WebElement]:
        return self.wait.until(EC.visibility_of_all_elements_located(selector))

    def click_when_clickable(self, selector: tuple):
        self.wait.until(EC.element_to_be_clickable(selector)).click()

    def send_keys_when_ready(self, selector: tuple, text: str):
        element = self.wait.until(EC.element_to_be_clickable(selector))
        element.clear()
        element.send_keys(text)

    def upload_file(self, selector: tuple, file_path: str):
        abs_path = os.path.abspath(file_path)
        self.send_keys_when_ready(selector, abs_path)

    def get_all_option_values_of_select_dropdown(self, selector: tuple) -> list[str]:
        dropdown_element = self.wait.until(EC.element_to_be_clickable(selector))
        select = Select(dropdown_element)
        return [option.text for option in select.options]

    def select_by_visible_text(self, selector: tuple, text: str):
        dropdown = self.wait.until(EC.element_to_be_clickable(selector))
        select = Select(dropdown)
        select.select_by_visible_text(text)

    def switch_to_iframe(self, iframe_selector: tuple):
        iframe = self.wait.until(EC.element_to_be_clickable(iframe_selector))
        self.driver.switch_to.frame(iframe)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def wait_for_non_empty_text(self, selector: tuple) -> str:
        return self.wait.until(lambda d: (value := d.find_element(*selector).text).strip() or None)

    def wait_for_non_empty_attribute(self, selector: tuple, attribute: str) -> str:
        return self.wait.until(lambda d: (value := d.find_element(*selector).get_attribute(attribute)).strip() or None)

    def wait_for_table_cell_text(self, cell_index: int, expected_text: str) -> str:
        return self.wait.until(lambda d: (
            (text := d.find_elements(By.CSS_SELECTOR, "table tr:last-child td")[cell_index].text)
            if len(d.find_elements(By.CSS_SELECTOR, "table tr:last-child td")) > cell_index and
            d.find_elements(By.CSS_SELECTOR, "table tr:last-child td")[cell_index].text == expected_text
            else None
        ))


    def get_all_field_names_in_table(self) -> list[str]:
        elements = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"table thead tr th")))
        return [el.text for el in elements]

    def get_options_attribute_value(self, selector: tuple) -> list[str]:
        elements = self.wait.until(EC.presence_of_all_elements_located(selector))
        return [el.get_attribute("value") for el in elements]

    def click_by_value(self, radio_selector: tuple, value_to_click: str):
        radios = self.wait.until(EC.presence_of_all_elements_located(radio_selector))
        for radio in radios:
            if radio.get_attribute("value") == value_to_click:
                radio.click()
                break

    def type_input(self, element: WebElement, value: str):
        element.send_keys(value)

    def click_with_javascript(self, selector: tuple):
        element = self.wait.until(EC.element_to_be_clickable(selector))
        self.driver.execute_script("arguments[0].click();", element)

    def get_all_field_texts_in_table(self, selector: tuple) -> list[str]:
        elements = self.wait.until(EC.visibility_of_all_elements_located(selector))
        return [el.text for el in elements]

    def reject_confirm_dialog(self):
        alert = self.wait.until(EC.alert_is_present())
        alert.dismiss()

    def accept_confirm_dialog(self):
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()

    def find_child_element(self, parent_selector: tuple, child_selector: tuple) -> WebElement:
        parent = self.wait.until(EC.visibility_of_element_located(parent_selector))
        return parent.find_element(*child_selector)

    def wait_milliseconds(self, ms: int):
        time.sleep(ms / 1000)

    def click_button_in_table_row(self, cell_text: str, button_selector: tuple):
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tr")
        for row in rows:
            if cell_text in row.text:
                row.find_element(*button_selector).click()
                break

    def find_element_containing_text(self, parent_selector: tuple, partial_text: str) -> WebElement:
        elements = self.driver.find_elements(*parent_selector)
        for el in elements:
            if partial_text in el.text:
                return el
        return None

    def select_date(self, day: str, month: str, year: str):
        year_dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".react-datepicker__year-dropdown-container")))
        year_dropdown.click()

        year_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'react-datepicker__year-option') and text()='{year}']")))
        year_option.click()

        month_dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".react-datepicker__month-dropdown-container")))
        month_dropdown.click()

        month_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'react-datepicker__month-option') and text()='{month}']")))
        month_option.click()

        padded_day = f"{int(day):02d}"
        date_locator = (By.CSS_SELECTOR,
                        f"div[class*='react-datepicker__day--0{padded_day}'][aria-label*='{month} {day}']")
        day_element = self.wait.until(EC.element_to_be_clickable(date_locator))
        day_element.click()