from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from login_info import email, password # file login_info.py that contains email,password values
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


LOGIN_URL = "https://linkedin.com/login"
CONNECTIONS_URL = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
driver = webdriver.Edge()
driver.get(LOGIN_URL)
time.sleep(1)

# LOGIN PROCESS
driver.find_element(By.ID, "username").send_keys(email)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# REDIRECT TO CONNECTIONS PAGE
driver.get(CONNECTIONS_URL)
time.sleep(2)

# SCROLL UP AND SCROLL DOWN AND MAXIMIZE WINDOW
driver.find_element(By.TAG_NAME,"body").send_keys(Keys.END)
time.sleep(2)
driver.find_element(By.TAG_NAME,"body").send_keys(Keys.HOME)
driver.maximize_window()

# FIND ALL MESSAGE BUTTON TO SEND MESSAGE
all_buttons = driver.find_elements(By.TAG_NAME,'button')
message_buttons = [btn for btn in all_buttons if btn.text == "Message"]
print(f"Length Messages : {len(message_buttons)}")
time.sleep(2)

MSG = ", Sorry hada gha automated message 🙏🙏🙏."


# SENDING A MESSAGE FOR EACH NEW CONNECTION
try:
    for i in range(0,len(message_buttons)):

        # CLICK ON THE MESSAGE BUTTON
        driver.execute_script("arguments[0].click();", message_buttons[i])
        time.sleep(2)

        # CLICK ON MESSAGE DIV AND MAXIMIZE IT
        msg_div = driver.find_element(By.XPATH,"//div[starts-with(@class, 'msg-form__contenteditable')]")
        driver.execute_script("arguments[0].click();", msg_div)
        maximize_msg_div = driver.find_element(By.XPATH,"//button[starts-with(@class, 'msg-overlay-bubble-header__control msg-overlay-conversation-bubble__expand-btn')]")
        driver.execute_script("arguments[0].click();", maximize_msg_div)
        time.sleep(2)

        # SCRAPE USER FULLNAME
        try:
            #case 1 - no message before
            user_fullname = driver.find_element(By.XPATH,"//div[@class='artdeco-entity-lockup__title ember-view']")
        except:
            #case 2 - already sent the first message before
            user_fullname = driver.find_element(By.XPATH,"//span[starts-with(@class,'t-14 t-bold hoverable-link-text')]")
        finally:
            print(user_fullname.text)
        time.sleep(2)

        # WRITE A MESSAGE
        paragraphs = driver.find_elements(By.TAG_NAME,"p")
        target_paragraph = paragraphs[-5]
        MESSAGE = f"Hello {user_fullname.text}, {MSG}"
        # target_paragraph.send_keys(MESSAGE)
        driver.execute_script("arguments[0].innerText = arguments[1];", target_paragraph, MESSAGE)##Clear existing content and set new content using JavaScript
        driver.implicitly_wait(2)
        driver.execute_script("var evt = document.createEvent('Events'); evt.initEvent('input', true, false); arguments[0].dispatchEvent(evt);", target_paragraph)##Trigger an input event after setting inner text
        time.sleep(2)
        assert target_paragraph.is_displayed(), "Paragraph is not visible after sending keys."##Verify visibility after sending keys
        driver.implicitly_wait(2)##Wait for a short period after sending keys

        # SEND THE MESSAGE
        wait = WebDriverWait(driver, 10)
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='msg-form__send-button artdeco-button artdeco-button--1']")))
        print(f"Button Text: {send_btn.text}, Is Enabled: {send_btn.is_enabled()}")
        if send_btn.is_enabled() == True:
            driver.execute_script("arguments[0].click();", send_btn)
        else:
            time.sleep(2)
            driver.execute_script("arguments[0].click();", send_btn)
        time.sleep(2)
        
        # X BUTTON FOR CLOSE CONVERSATION
        x_button = driver.find_element(By.XPATH,"//button[starts-with(@class, 'msg-overlay-bubble-header__control artdeco-button artdeco-button--circle')]")
        driver.execute_script("arguments[0].click();", x_button)
        time.sleep(2)

        if i == 10:
            break

except Exception as e:
    print(e)

finally:
    input("Press any key to close the browser...\n")
