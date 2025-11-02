import pytest
from pages.form_page import FormPage
from pages.listing_page import ListingPage
from utility.random_utility import RandomUtility
import os


#poetry run pytest --html=report.html  --self-contained-html tests/test_crud_pom.py
@pytest.mark.usefixtures("browser", "base_url")
class TestCrudPOM:

    @pytest.fixture(autouse=True)
    def setup(self, browser, base_url):
        """Fixture to initialize pages before tests."""
        self.driver = browser
        self.base_url = base_url
        self.form_page = FormPage(browser)
        self.listing_page = ListingPage(browser)
        self.random_utility = RandomUtility()
        self.listing_url = self.base_url + "records"

        # Initialize form data
        self.form_data = {
            "singleLine": self.random_utility.generate_random_string(),
            "multiLine": self.random_utility.generate_multiple_line_content(),
            "editor": self.random_utility.generate_multiple_line_content(),
            "number": self.random_utility.generate_random_numberss(),
            "email": self.random_utility.generate_random_email(),
            "phone": self.random_utility.generate_fake_phone_number(),
            "time": self.random_utility.generate_random_time(),
            "location": self.random_utility.generate_random_lat_long(),
            "singleSelection": "random",
            "multiSelection": "random",
            "radio": "random",
            "checkbox": "random",
            "datePicker": self.random_utility.generate_random_date(),
            "dateRange": self.random_utility.generate_random_date_range(),
            "file": os.path.abspath("utility/test.png")
        }

    def test_create_and_delete_record(self):
        """Test to verify a record can be added and deleted."""
        # Go to listing page and click add
        self.listing_page.goto_listing_page(self.listing_url)
        self.listing_page.click_on_add_button()

        # Fill form and save
        self.form_page.fill_form(self.form_data)
        self.form_page.save_record()

        # Verify record exists in table
        single_line_text = self.listing_page.get_latest_table_value("Single Line", self.form_data["singleLine"])
        assert single_line_text == self.form_data["singleLine"], "Verify single line value is as expected"

        # Delete record and wait
        self.listing_page.click_on_delete_button(single_line_text)
        self.listing_page.wait_milliseconds(5000)
        self.listing_page.reject_confirm_dialog()