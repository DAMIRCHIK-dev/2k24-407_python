import time
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)  # kutish vaqtini ko‘paytirdik
driver.get("https://shaxzodbek.com/")

login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/nav/ul/li[4]/a")))
login_button.click()

login_button2 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/div[2]/a[1]")))

driver.execute_script("arguments[0].scrollIntoView(true);", login_button2)
time.sleep(1)
driver.execute_script("arguments[0].click();", login_button2)

login_button3 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/div[1]/div/div[3]/div[2]/h4/a")))
driver.execute_script("arguments[0].scrollIntoView(true);", login_button3)
time.sleep(1)
driver.execute_script("arguments[0].click();", login_button3)

title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".certification-header h3"))).text
obtained_date = driver.find_element(By.CLASS_NAME, "certification-date").text.replace("Obtained: ", "")
image_url = driver.find_element(By.CSS_SELECTOR, ".certification-image img").get_attribute("src")
description = driver.find_element(By.CLASS_NAME, "certification-description").text.strip()

print("Title:", title)
print("Obtained Date:", obtained_date)
print("Image URL:", image_url)
print("Description:", description)

conn = psycopg2.connect(
    host="localhost",
    database="selenuim",
    user="postgres",
    password="admin1234"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        public_date TEXT NOT NULL,
        image_url TEXT,
        description TEXT
    );
""")

cur.execute("""
    DELETE FROM certifications
    WHERE title = %s AND public_date = %s;
""", (title, obtained_date))

cur.execute("""
    INSERT INTO certifications (title, public_date, image_url, description)
    VALUES (%s, %s, %s, %s);
""", (title, obtained_date, image_url, description))

conn.commit()
cur.close()
conn.close()

print("✅ Sertifikat ma'lumotlari muvaffaqiyatli qo‘shildi.")
driver.quit()