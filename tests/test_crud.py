import pytest
import pytest_check as check
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from utility.random_utility import RandomUtility
import os
from pages.base_page import BasePage

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
objBasePage = BasePage(driver)

def test_crud(base_url):
    wait = WebDriverWait(driver, 10)

    #selectors
    single_line_selector = (By.ID, "singleLine")
    multi_line_selector = (By.ID, "multiLine")
    editor_iframe_selector = (By.CSS_SELECTOR, "iframe[id*='tiny-react']")
    editor_selector = (By.CSS_SELECTOR, "body#tinymce")
    number_selector = (By.CSS_SELECTOR, "input[id='number']")
    email_selector = (By.XPATH, "//input[@id='email']")
    phone_selector = (By.CSS_SELECTOR, "input[type*='tel']")
    single_selection_selector = (By.CSS_SELECTOR, "#singleSelect")
    multi_selection_selector = (By.CSS_SELECTOR, "#multiSelect")
    file_field_selector = (By.CSS_SELECTOR, "#file")
    radio_button_selector = (
        By.XPATH,
        "//label[contains(text(), 'Radio Buttons')]/following-sibling::div/label/input[@type='radio']"
    )
    checkbox_selector = (By.CSS_SELECTOR, "input[type='checkbox']")
    date_picker_selector = (By.CSS_SELECTOR, "#date")
    date_range_start_selector = (By.CSS_SELECTOR, "#dateRangeStart")
    date_range_end_selector = (By.CSS_SELECTOR, "#dateRangeEnd")
    time_picker_selector = (By.ID, "time")
    location_selector = (By.CSS_SELECTOR, "#location")
    save_button_selector = (By.CSS_SELECTOR, "button[type='submit']")

    
    #creating random values for all fields
    form_data = {}
    form_data["single_line"] = RandomUtility.generate_random_string()
    form_data["multi_line"] = RandomUtility.generate_multiple_line_content()
    form_data["editor"] = RandomUtility.generate_multiple_line_content()
    form_data["number"] = RandomUtility.generate_random_numberss()
    form_data["email"] = RandomUtility.generate_random_email()
    form_data["phone"] = RandomUtility.generate_fake_phone_number()
    form_data["time"] = RandomUtility.generate_random_time()
    form_data["date_picker"] = RandomUtility.generate_random_date()
    form_data["date_range"] = RandomUtility.generate_random_date_range()
    form_data["location"] = RandomUtility.generate_random_lat_long()
    form_data["single_selection"] = "Option 2"
    form_data["multi_selection"] = ["Option 2","Option 1"]
    form_data["radio"] = "option1"
    form_data["file"] = "utility/test.png"


    #go to URL
    driver.get(f"{base_url}/records")
    
    #click on add button
    driver.find_element(By.CLASS_NAME,"bg-green-500").click()

    #add data
    # driver.find_element(*single_line_selector).send_keys(form_data["single_line"]) #need to use asterisk to unpack like spread operator in js
    wait.until(EC.element_to_be_clickable(single_line_selector)).send_keys(form_data["single_line"])
    wait.until(EC.element_to_be_clickable(multi_line_selector)).send_keys(form_data["multi_line"])

    #editor
    iframe_element = wait.until(EC.element_to_be_clickable(editor_iframe_selector))
    driver.switch_to.frame(iframe_element)
    wait.until(EC.element_to_be_clickable(editor_selector)).send_keys(form_data["editor"])
    driver.switch_to.default_content()

    wait.until(EC.element_to_be_clickable(number_selector)).send_keys(form_data["number"])
    wait.until(EC.element_to_be_clickable(email_selector)).send_keys(form_data["email"])
    wait.until(EC.element_to_be_clickable(phone_selector)).send_keys(form_data["phone"])

    #single selection and multi selection
    single_selection_element = wait.until(EC.element_to_be_clickable(single_selection_selector))
    select_element = Select(single_selection_element)
    select_element.select_by_visible_text(form_data["single_selection"])

    multi_selection_element = wait.until(EC.element_to_be_clickable(multi_selection_selector))
    multiselect_element = Select(multi_selection_element)
    multiselect_element.select_by_visible_text((form_data["multi_selection"])[0])
    multiselect_element.select_by_visible_text((form_data["multi_selection"])[1])

    #file
    absolute_path = os.path.abspath(form_data["file"])
    wait.until(EC.element_to_be_clickable(file_field_selector)).send_keys(absolute_path)

    #radio button and checkbox
    radio_buttons = wait.until(EC.visibility_of_all_elements_located(radio_button_selector))
    for i in radio_buttons:
        if i.get_attribute("value") == form_data["radio"]:
            i.click()

    wait.until(EC.element_to_be_clickable(checkbox_selector)).click()

    #Date picker
    wait.until(EC.element_to_be_clickable(date_picker_selector)).click()
    date_picker_elements = form_data["date_picker"][0]
    day = date_picker_elements[0]
    month = date_picker_elements[1]
    year = date_picker_elements[2]
    objBasePage.select_date(day,month,year)

    #Date range start
    wait.until(EC.element_to_be_clickable(date_range_start_selector)).click()
    date_start_elements = form_data["date_range"][0]
    day1 = date_start_elements[0]
    month1 = date_start_elements[1]
    year1 = date_start_elements[2]
    objBasePage.select_date(day1,month1,year1)


    #date range end
    wait.until(EC.element_to_be_clickable(date_range_end_selector)).click()
    date_end_elements = form_data["date_range"][2]
    day2 = date_end_elements[0]
    month2 = date_end_elements[1]
    year2 = date_end_elements[2]
    objBasePage.select_date(day2,month2,year2)

    #time
    wait.until(EC.element_to_be_clickable(time_picker_selector)).send_keys(form_data["time"])
    wait.until(EC.element_to_be_clickable(location_selector)).send_keys(form_data["location"])

    #submit the record
    wait.until(EC.element_to_be_clickable(save_button_selector)).click()

    #verify the record
    single_line_text = form_data["single_line"]
    single_line_actual_text = wait.until(lambda d:((tdBoxes := d.find_elements(By.CSS_SELECTOR,"table tr:last-child td")) and len(tdBoxes) > 1 
                        and tdBoxes[1].text != "" and tdBoxes[1].text == single_line_text and tdBoxes[1].text) or None)
    check.equal(single_line_text,single_line_actual_text,"Verify singleline value")

    #verify the record in edit screen 
    (driver.find_elements(By.CSS_SELECTOR,"table tr:last-child td"))[3].find_element(By.CSS_SELECTOR,".bg-yellow-500").click()
    multi_line_text = form_data["multi_line"]
    multi_line_actual_text = wait.until(lambda d:((text := d.find_element(*multi_line_selector).get_attribute("value")) and text != None and text.strip()!="" and text) or None)
    check.equal(multi_line_text,multi_line_actual_text,"verify multiline value")
