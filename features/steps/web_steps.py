"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""

import logging
import requests
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204


@when('I visit the "Home Page"')
def step_impl(context):
    """Visit the base url"""
    context.driver.get(context.base_url + "/")
    # Uncomment next line to take a screenshot of the web page
    # context.driver.save_screenshot('home_page.png')


@given("the server is running")
def step_impl(context):
    """Verify the server is running"""
    rest_endpoint = f"{context.base_url}/shopcarts"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """The home page title should be visible on the page"""
    print(context.driver.title)
    assert message in str(context.driver.title)


@then('I should not see "{message}"')
def step_impl(context, message):
    """There should be no errors on the page"""
    assert message not in str(context.resp.text)


@when('I press the "{button}" button')
def step_impl(context, button):
    """Presses button on the UI"""
    button_id = button.replace(" ", "-").lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see "{element_id}" in the results')
def step_impl(context, element_id):
    """Verifies visibility of <td> with id=element_id in the results table"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located((By.ID, element_id))
    )
    assert found


@then('I should see "{text_string}" under the row "{element_id}" in the table')
def step_impl(context, text_string, element_id):
    """Verifies visibility of <td> with id=element_id in the results table"""
    element_id = element_id.lower().replace(" ", "-")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, element_id), text_string
        )
    )
    assert found


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """Verifies absence of <td> with id=element_id in the results table"""
    found_element = False
    context.driver.implicitly_wait(1)
    try:
        context.driver.find_element(By.ID, name)
        found_element = True
    except NoSuchElementException:
        pass

    context.driver.implicitly_wait(context.wait_seconds)
    assert found_element is False


@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"), message
        )
    )
    assert found


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id), text_string
        )
    )
    assert found


@then('I should not see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)

    not_found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.not_(
            expected_conditions.text_to_be_present_in_element_value(
                (By.ID, element_id), text_string
            )
        )
    )
    assert not_found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == ""


@then('the "{element_name}" field should not be empty')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") != ""


@then('I should see "{element_name}" in the results being "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "_")
    print(element_id)
    found_text = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id), text_string
        )
    )
    assert (
        found_text
    ), f"Expected text '{text_string}' not found in element '{element_id}'"


##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard contains: %s", context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)
