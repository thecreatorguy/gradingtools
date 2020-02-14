#!/usr/bin/python3
"""
Filename: submit_grades.py
Language: Python 3.6
Author: Timothy Johnson <tim@itstimjohnson.com>
Description: Semi-automatically submits lab grades to mycourses.com
"""
import os
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
load_dotenv()

def get_grade_data():
    dirs = [name for name in next(os.walk('.'))[1] if name not in os.getenv('GRADINGTOOLS_DIRECTORIES')]
    while True:
        for i, d in enumerate(dirs):
            print('[%2d] %s' % (i, d))
        choice = input('Select folder to upload: ')
        if not choice.isdigit():
            print('Choice was not in list.')
            continue
        choice = int(choice)
        if choice in range(len(dirs)):
            break
        print('Choice was not in list.')
    choice = dirs[choice]

    lab_files = [name for name in os.listdir(choice)]
    if 'grades.json' not in lab_files:
        print('There is no grade data (grades.json) in that folder.')
        return False

    with open('./' + choice + '/grades.json', 'r') as f:
        grade_data = json.load(f)
    parsed_data = {row['name'].lower():{'grade':row['score'], 'feedback':row['feedback']} for row in grade_data}

    return choice.lower().replace(' ', ''), parsed_data

def shadow_element_by_css_selector(driver, selector, index = 0):
    if index == 0:
        script = 'return document.querySelector("%s").shadowRoot' % selector
    else:
        script = 'return document.querySelectorAll("%s")[%s].shadowRoot' % (selector, index)
    element = driver.execute_script(script)
    return element

def main():
    # Get which directory to upload
    result = get_grade_data()
    if not result:
        return
    choice, grade_data = result

    # Start the driver, go to mycourses home page. We need to login first, so click the login button
    driver = webdriver.Chrome()
    driver.get('https://mycourses.rit.edu/d2l/home')

    # Click the login button
    login_button = driver.find_element_by_css_selector('#login_box1 > a')
    login_button.click()

    # Insert the username and password and submit the form
    username_input = driver.find_element_by_id("username")
    username_input.send_keys(os.getenv('MYCOURSES_USERNAME'))
    password_input = driver.find_element_by_id("password")
    password_input.send_keys(os.getenv('MYCOURSES_PASSWORD'))
    login_button = driver.find_element_by_name("_eventId_proceed")
    login_button.click()

    # Wait for 2FA
    try:
        WebDriverWait(driver, 60).until(EC.title_contains('Homepage'))
    except:
        driver.quit()
        return

    # Go to the grading page and get a list of the headers that can be graded- see if the chosen header is there
    driver.get(os.getenv('GRADE_SHEET_URL'))
    headers = driver.find_elements_by_css_selector('#z_bk tr:nth-child(2) > th')
    # Remove subtotals from this list- they have no buttons, and therefore throw off the button count
    headers = [header.text.lower().replace(' ', '') for header in headers
                    if header.text.lower().replace(' ', '') != 'subtotal']
    header_to_elem_map = {header:index for index, header in enumerate(headers)}
    if choice not in header_to_elem_map.keys():
        print('Location to upload grades not found.')
        return

    # Drop down buttons are in a shadow root- find it, then click the dropdown menu button
    button_root = shadow_element_by_css_selector(
            driver,
            '#z_bk tr:nth-child(2) > th d2l-button-icon',
            header_to_elem_map[choice]
        )
    dd_button = button_root.find_element_by_css_selector('button')
    dd_button.click()

    # Enter grades dropdown element is within the main body, click that
    enter_grades_dd = driver.find_element_by_css_selector(
            'd2l-menu-item[text="Enter Grades"]'
        )
    enter_grades_dd.click()

    # Find each of the names to match with the grade data
    time.sleep(3)
    grade_rows = driver.find_elements_by_css_selector('#z_u tr+tr')
    print(len(grade_rows))
    for row in grade_rows:
        # Find the name that will match the folders in the grading folder
        parts = row.find_element_by_css_selector('th').text.replace(' ', '').lower().split(',')
        if len(parts) < 3:
            continue
        name = parts[0] + ',' + parts[1]
        if name not in grade_data.keys(): # Leave anyone who did not submit something untouched
            continue

        # Input grade
        grade_input = row.find_element_by_css_selector('input[type="text"]')
        grade_input.clear()
        grade_input.send_keys(grade_data[name]['grade'])

        # Click the pencil for feedback
        feedback_button = row.find_element_by_css_selector('td:last-child a')
        time.sleep(1)
        driver.execute_script("arguments[0].click();", feedback_button)

        # Click the source editor button in the feedback window
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((
                By.XPATH,
                "//div[@class='d2l-dialog d2l-dialog-mvc'][1]/div/iframe"
            )))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'a[title="HTML Source Editor"]'
            )))
        source_editor_button = driver.find_element_by_css_selector('a[title="HTML Source Editor"]')
        time.sleep(1)
        driver.execute_script("arguments[0].click();", source_editor_button)

        # Input the html feedback into the feedback box and save
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((
                By.XPATH,
                "//div[@class='d2l-dialog d2l-dialog-mvc'][2]/div/iframe"
            )))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'div.d2l-htmleditor-code > textarea'
            )))
        feedback_box = driver.find_element_by_css_selector('div.d2l-htmleditor-code > textarea')
        feedback_box.clear()
        feedback_box.send_keys(grade_data[name]['feedback'])
        source_save_button = driver.find_element_by_css_selector('button[primary]')
        time.sleep(1)
        source_save_button.click()

        # Click save again
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((
                By.XPATH,
                "//div[@class='d2l-dialog d2l-dialog-mvc'][1]/div/iframe"
            )))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'div.d2l-dialog-buttons button[primary]'
            )))
        feedback_save_button = driver.find_element_by_css_selector('div.d2l-dialog-buttons button[primary]')
        time.sleep(1)
        feedback_save_button.click()

        # Repeat
        driver.switch_to.default_content()



if __name__ == '__main__':
    main()
    input("hit enter to continue")

