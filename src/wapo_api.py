import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    geckodriver_path = "/snap/bin/geckodriver"
    service = Service(executable_path=geckodriver_path)

    return webdriver.Firefox(options=options, service=service)


def get_wapo_url(day: str = None):
    driver = _get_driver()

    try:
        driver.get("https://www.washingtonpost.com/crossword-puzzles/daily/")

        wait = WebDriverWait(driver, 5)

        btn_accept_cookies = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        btn_accept_cookies.click()

        crossword_frame = wait.until(
            EC.element_to_be_clickable((By.ID, "iframe-xword"))
        )
        driver.switch_to.frame(crossword_frame)

        item_latest_crossword = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "puzzle-link"))
        )
        item_latest_crossword.click()

        btn_footer = wait.until(EC.element_to_be_clickable((By.ID, "footer-btn")))
        btn_footer.click()

        # Wait for things to load
        time.sleep(2)

        btn_invite = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "nav-social-play-invite-icon"))
        )
        btn_invite.click()

        textarea_invite_link = wait.until(
            EC.presence_of_element_located((By.ID, "social-link"))
        )
        return textarea_invite_link.get_attribute("value")

    finally:
        driver.quit()


def is_complete(url: str) -> bool:
    driver = _get_driver()

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 5)

        btn_accept_cookies = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        btn_accept_cookies.click()

        crossword_frame = wait.until(
            EC.element_to_be_clickable((By.ID, "iframe-xword"))
        )
        driver.switch_to.frame(crossword_frame)

        modal_title = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-title"))
        )
        return modal_title.text == "Congratulations!"

    except Exception as e:
        print(f"Unable to check puzzle complete: {e}")
        return False

    finally:
        driver.quit()


def get_puzzle_time(url: str) -> int:
    driver = _get_driver()

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 5)

        btn_accept_cookies = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        btn_accept_cookies.click()

        crossword_frame = wait.until(
            EC.element_to_be_clickable((By.ID, "iframe-xword"))
        )
        driver.switch_to.frame(crossword_frame)

        time_str = wait.until(
            EC.visibility_of_element_located((By.ID, "clock_str"))
        )  # "X minutes and Y seconds"

        parts = time_str.text.split(" ")
        numbers = [p for p in parts if p.isdigit()]

        return int(numbers[0]) * 60 + int(numbers[1])

    except Exception as e:
        print(f"Unable to get puzzle complete time: {e}")
        return False

    finally:
        driver.quit()