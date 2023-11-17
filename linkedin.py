from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from login_info import email, password # file login_info.py that contains email,password values
import time

LOGIN_URL = "https://linkedin.com/login"
CONNECTIONS_URL = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
driver = webdriver.Edge()
driver.get(LOGIN_URL)
time.sleep(1)

# Login process
user_mail = driver.find_element(By.ID, "username")
user_mail.send_keys(email)
user_pass = driver.find_element(By.ID, "password")
user_pass.send_keys(password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Redirecting to connection page
driver.get(CONNECTIONS_URL)
time.sleep(2)

# Scroll up and scroll down
driver.find_element(By.TAG_NAME,"body").send_keys(Keys.END)
time.sleep(2)
driver.find_element(By.TAG_NAME,"body").send_keys(Keys.HOME)

# Find All Message button to send message
all_buttons = driver.find_elements(By.TAG_NAME,'button')
message_buttons = [btn for btn in all_buttons if btn.text == "Message"]
print(len(message_buttons))

# Sending a message for each new connection
for i in range(0,len(message_buttons)):
    try:
        # Click message button for each new connection
        driver.execute_script("arguments[0].click();", message_buttons[i])
        time.sleep(2)

        # Click on the message div
        msg_div = driver.find_element(By.XPATH,"//div[starts-with(@class, 'msg-form__contenteditable')]")
        msg_div.click()

        # Write a message
        paragraphs = driver.find_elements(By.TAG_NAME,"p")
        paragraphs[-5].send_keys("Sorry hada gha automated message 🙏🙏🙏")
        time.sleep(2)

        # Send the message
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # X button for close conversation
        x_button = driver.find_element(By.XPATH,"//button[starts-with(@class, 'msg-overlay-bubble-header__control artdeco-button artdeco-button--circle')]")
        x_button.click()

        if i==2:
            break

    except Exception as e:
        print(e)

input("Press Enter to close the browser...\n")
