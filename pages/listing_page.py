from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage

class ListingPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.add_button = (By.CLASS_NAME, "bg-green-500")
        self.delete_button = (By.XPATH, "//*[contains(text(),'Delete')]")

    def goto_listing_page(self,listing_url):
        self.go_to(listing_url)

    def click_on_add_button(self):
        self.click_when_clickable(self.add_button)

    def get_latest_table_value(self, field_name: str, field_value: str) -> str:
        field_names = self.get_all_field_names_in_table()
        if field_name in field_names:
            index_of_field = field_names.index(field_name)
            text = self.wait_for_table_cell_text(index_of_field, field_value)
            return text
        return "No data"

    def click_on_delete_button(self, text: str):
        self.click_button_in_table_row(text, self.delete_button)