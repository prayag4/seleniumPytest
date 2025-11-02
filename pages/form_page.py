from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from utility.random_utility import RandomUtility
from pages.base_page import BasePage

class FormPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.random_utility = RandomUtility()

        # Selector list
        self.single_line_selector = (By.ID, "singleLine")
        self.multi_line_selector = (By.ID, "multiLine")
        self.editor_iframe_selector = (By.CSS_SELECTOR, "iframe[id*='tiny-react']")
        self.editor_selector = (By.CSS_SELECTOR, "body#tinymce")
        self.number_selector = (By.CSS_SELECTOR, "input[id='number']")
        self.email_selector = (By.XPATH, "//input[@id='email']")
        self.phone_selector = (By.CSS_SELECTOR, "input[type*='tel']")
        self.single_selection_selector = (By.CSS_SELECTOR, "#singleSelect")
        self.multi_selection_selector = (By.CSS_SELECTOR, "#multiSelect")
        self.file_field_selector = (By.CSS_SELECTOR, "#file")
        self.radio_button_selector = (
            By.XPATH,
            "//label[contains(text(), 'Radio Buttons')]/following-sibling::div/label/input[@type='radio']"
        )
        self.checkbox_selector = (By.CSS_SELECTOR, "input[type='checkbox']")
        self.date_picker_selector = (By.CSS_SELECTOR, "#date")
        self.date_range_start_selector = (By.CSS_SELECTOR, "#dateRangeStart")
        self.date_range_end_selector = (By.CSS_SELECTOR, "#dateRangeEnd")
        self.time_picker_selector = (By.ID, "time")
        self.location_selector = (By.CSS_SELECTOR, "#location")
        self.save_button_selector = (By.CSS_SELECTOR, "button[type='submit']")

    def fill_form(self, form_data: dict):
        if "singleLine" in form_data:
            self.send_keys_when_ready(self.single_line_selector, form_data["singleLine"])

        if "multiLine" in form_data:
            self.send_keys_when_ready(self.multi_line_selector, form_data["multiLine"])

        if "editor" in form_data:
            self.switch_to_iframe(self.editor_iframe_selector)
            self.send_keys_when_ready(self.editor_selector, form_data["editor"])
            self.switch_to_default_content()

        if "number" in form_data:
            self.send_keys_when_ready(self.number_selector, form_data["number"])

        if "email" in form_data:
            self.send_keys_when_ready(self.email_selector, form_data["email"])

        if "phone" in form_data:
            self.send_keys_when_ready(self.phone_selector, form_data["phone"])

        if "time" in form_data:
            self.send_keys_when_ready(self.time_picker_selector, form_data["time"])

        if "location" in form_data:
            self.send_keys_when_ready(self.location_selector, form_data["location"])

        if "file" in form_data:
            self.upload_file(self.file_field_selector, form_data["file"])

        if form_data.get("singleSelection") == "random":
            all_options = self.get_all_option_values_of_select_dropdown(self.single_selection_selector)
            selected_value = self.random_utility.get_random_selected_one_value_from_array(all_options)
            self.select_by_visible_text(self.single_selection_selector, selected_value)
            form_data["singleSelection"] = selected_value

        if form_data.get("multiSelection") == "random":
            all_options = self.get_all_option_values_of_select_dropdown(self.multi_selection_selector)
            selected_values = self.random_utility.get_random_selected_values_from_array(all_options)
            for option in selected_values:
                self.select_by_visible_text(self.multi_selection_selector, option)
            form_data["multiSelection"] = selected_values

        if form_data.get("radio") == "random":
            all_options = self.get_options_attribute_value(self.radio_button_selector)
            selected_value = self.random_utility.get_random_selected_one_value_from_array(all_options)
            self.click_by_value(self.radio_button_selector, selected_value)
            form_data["radio"] = selected_value

        if form_data.get("checkbox") == "random":
            all_options = self.get_options_attribute_value(self.checkbox_selector)
            selected_values = self.random_utility.get_random_selected_values_from_array(all_options)
            for option in selected_values:
                self.click_by_value(self.checkbox_selector, option)
            form_data["checkbox"] = selected_values

        if "datePicker" in form_data:
            self.click_when_clickable(self.date_picker_selector)
            day, month, year = form_data["datePicker"][0]
            self.select_date(day, month, year)

        if "dateRange" in form_data:
            self.click_when_clickable(self.date_range_start_selector)
            day, month, year = form_data["dateRange"][0]
            self.select_date(day, month, year)

            self.click_when_clickable(self.date_range_end_selector)
            day2, month2, year2 = form_data["dateRange"][2]
            self.select_date(day2, month2, year2)

    def save_record(self):
        self.click_when_clickable(self.save_button_selector)