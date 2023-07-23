from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
# Set up the driver (adjust the path to your driver executable)

# Navigate to the webpage
driver.get('https://ais.usvisa-info.com/en-ca/niv/schedule/38176035/appointment')

accept_button = driver.find_element(By.CSS_SELECTOR, 'button[class="ui-button ui-corner-all ui-widget"]')
accept_button.click()

import json

# Specify the path to the JSON file
json_file_path = "./user_config.json"
# Open the JSON file
with open(json_file_path) as file:
    # Load the JSON data into a dictionary
    data = json.load(file)
# Access the data as a dictionary
# For example, access a specific key
username = data["username"]
password = data["password"]

#Find username and password input textbox
username_input_field = driver.find_element(By.ID, 'user_email')
password_input_field = driver.find_element(By.ID, 'user_password')
check_button = driver.find_element(By.CSS_SELECTOR, 'label[for="policy_confirmed"]')

#Clear Values in the textbox fields
username_input_field.clear()
password_input_field.clear()

#Enter credentials
username_input_field.send_keys(username)
password_input_field.send_keys(password)
check_button.click()

#Submit form
username_input_field.submit()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_until_element_appears(driver, locator, timeout):
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.presence_of_element_located(locator))
    return element

timeout = 10

locator = (By.ID, "appointments_consulate_appointment_facility_id")
element = wait_until_element_appears(driver, locator, timeout)
consulate_location = Select(driver.find_element(By.ID, "appointments_consulate_appointment_facility_id"))
consulate_location.select_by_visible_text("Vancouver")

wait = WebDriverWait(driver, timeout)  # Adjust the timeout as needed

#open the calendar on the website
locator = (By.ID, "appointments_consulate_appointment_date")
element = wait.until(EC.element_to_be_clickable(locator))  # Replace with your desired locator
element = wait_until_element_appears(driver, locator, timeout)
calendar = driver.find_element(By.ID, "appointments_consulate_appointment_date")
calendar.click()

def isAvailable():
    try:
        driver.find_element(By.CSS_SELECTOR,'a[class="ui-state-default"]')
        return True
    except:
        return False

def goNext():
    next_button = driver.find_element(By.CSS_SELECTOR,'a[data-handler="next"]')
    next_button.click()

def getDates():
    dates = driver.find_elements(By.CSS_SELECTOR,'a[class="ui-state-default"]')
    return dates

while True:
    if not isAvailable():
        goNext()
    else:
        break


locator = (By.ID, "appointments_consulate_appointment_facility_id")
element = wait_until_element_appears(driver, locator, timeout)
consulate_location = Select(driver.find_element(By.ID, "appointments_consulate_appointment_facility_id"))
consulate_location.select_by_visible_text("Vancouver")

wait = WebDriverWait(driver, timeout)  # Adjust the timeout as needed

#open the calendar on the website
locator = (By.ID, "appointments_consulate_appointment_date")
element = wait.until(EC.element_to_be_clickable(locator))  # Replace with your desired locator
element = wait_until_element_appears(driver, locator, timeout)
calendar = driver.find_element(By.ID, "appointments_consulate_appointment_date")
calendar.click()

def isAvailable():
    try:
        driver.find_element(By.CSS_SELECTOR,'a[class="ui-state-default"]')
        return True
    except:
        return False

def goNext():
    next_button = driver.find_element(By.CSS_SELECTOR,'a[data-handler="next"]')
    next_button.click()

def getDates():
    dates = driver.find_elements(By.CSS_SELECTOR,'a[class="ui-state-default"]')
    return dates

while True:
    if not isAvailable():
        goNext()
    else:
        break

#load in old appointment data
appointmentData = data["CurrentAppointment"]
curr_year, curr_month, curr_day = appointmentData["year"], appointmentData["month"], appointmentData["day"]

def isEarlier(x: tuple[int, int, int], y: tuple[int, int, int], index: int = 0) -> bool:
    if index > 2:
        return False
    elif x[index] > y[index]:
        return False
    elif x[index] < y[index]:
        return True
    else:
        return isEarlier(x, y, index + 1)

def getDates():
    dates = driver.find_elements(By.CSS_SELECTOR,'td[data-handler="selectDay"]')
    return dates

dates = getDates()
bestdate = (curr_year,curr_month,curr_day)
bestelement = None
for date in dates:
    year = int(date.get_attribute("data-year"))
    month = int(date.get_attribute("data-month"))
    day = int(date.text)
    if isEarlier((year,month,day),bestdate):
        bestdate = (year,month,day)
        bestelement = date
        date.click()
try:
    bestelement.click()
    success=True
except:
    # driver.quit()
    success=False
    pass

select_element = Select(driver.find_element(By.ID,"appointments_consulate_appointment_time"))  # Replace "select-element-id" with the ID of the select element

# Get all the options within the select element
options = select_element.options
print(options)
# Select the first valid time option
for option in options:
    value = option.get_attribute("value")
    if value:
        select_element.select_by_value(value)


import json

def update_json(file_path, new_entries):
    # Read existing JSON data from file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Update specific entries in the JSON data
    for key, value in new_entries.items():
        data[key] = value

    # Write the updated JSON data back to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

if success is True:
    year = bestdate[0]
    month = bestdate[1]
    day = bestdate[2]
    new_entries = {
        'CurrentAppointment':{
        "year": 1,
        "month": 1,
        "day": 1,
        }
    }

    update_json('./user_config.json', new_entries)


reschedule = driver.find_element(By.ID,"appointments_submit")
reschedule.click()

if (isEarlier(bestdate,(curr_year,curr_month,curr_day))):
    confirm_reschedule = driver.find_element(By.CSS_SELECTOR,'a[class="button alert"]')
    confirm_reschedule.click()
else:
    cancel_reschedule = driver.find_element(By.CSS_SELECTOR,'span[class="fas fa-times"]')
    cancel_reschedule.click()