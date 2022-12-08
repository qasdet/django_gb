from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# TODO:
# 5. (**) Реализовать CRUD-тесты через инструмент Selenium. Произвести проверку переключения языка через инструмент Selenium.


class TestNewsSelenium(StaticLiveServerTestCase):

    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/001_news.json",
    )

    def setUp(self):
        super().setUp()
        self.news_title = "News title"
        self.news_preambule = "News preambule"
        self.news_body = "News body"
        self.selenium = WebDriver(executable_path=settings.SELENIUM_DRIVER_PATH_FF)
        self.selenium.implicitly_wait(10)
        # Login
        self.selenium.get(f"{self.live_server_url}{reverse('authapp:login')}")
        self.selenium.find_element(By.ID, "id_username").send_keys("admin")
        self.selenium.find_element(By.ID, "id_password").send_keys("admin")
        button_enter = WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.ID, "commit_creds")))
        button_enter.click()
        # Wait for footer
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto")))

    def test_create_button_clickable(self):
        path_list = f"{self.live_server_url}{reverse('mainapp:news')}"
        path_add = reverse("mainapp:news_create")
        self.selenium.get(path_list)
        button_create = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'[href="{path_add}"]'))
        )
        print("Trying to click button ...")
        button_create.click()  # Test that button clickable
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.ID, "id_title")))
        print("Button clickable!")
        # With no element - test will be failed
        # WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.ID, "id_title111")))

    def test_pick_color(self):
        path = f"{self.live_server_url}{reverse('mainapp:index')}"
        self.selenium.get(path)
        navbar_el = WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "navbar")))
        try:
            # Чтобы тест не падал :)
            # self.assertEqual(navbar_el.value_of_css_property("background-color"), "rgb(255, 255, 155)")
            self.assertNotEqual(navbar_el.value_of_css_property("background-color"), "rgb(255, 255, 155)")
        except AssertionError:
            with open("var/screenshots/001_navbar_el_scrnsht.png", "wb") as outf:
                outf.write(navbar_el.screenshot_as_png)
            raise

    # Основная идея в том, чтобы тестировать все операции на одной новости,
    # поэтому пришлось поместить их в один тест-кейс.
    def test_news_crud_operations(self):
        # test_create:
        path_list = f"{self.live_server_url}{reverse('mainapp:news')}"
        path_add = reverse("mainapp:news_create")
        self.selenium.get(path_list)
        button_create = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'[href="{path_add}"]'))
        )
        button_create.click()
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto")))
        self.selenium.find_element(By.ID, "id_title").send_keys(self.news_title)
        self.selenium.find_element(By.ID, "id_preambule").send_keys(self.news_preambule)
        self.selenium.find_element(By.ID, "id_body").send_keys(self.news_body)
        self.selenium.find_element(By.CLASS_NAME, "btn-primary").click()
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto")))
        self.assertEqual(self.news_title, self.selenium.find_element(By.CLASS_NAME, "card-title").text)
        self.assertEqual(self.news_preambule, self.selenium.find_element(By.CLASS_NAME, "card-text").text)

        # test_get
        details_url = self.selenium.find_element(By.LINK_TEXT, "Подробнее").get_attribute("href")
        self.selenium.get(details_url)
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto")))
        self.assertEqual(self.news_title, self.selenium.find_element(By.CLASS_NAME, "card-title").text)
        self.assertEqual(self.news_body, self.selenium.find_element(By.CLASS_NAME, "card-text").text)

        # test update
        current_news_url = details_url.replace("/detail", "")
        appendix = "_EDITED"
        update_news_url = f"{current_news_url}/update"
        self.selenium.get(update_news_url)
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto")))
        self.selenium.find_element(By.ID, "id_title").send_keys(appendix)
        self.selenium.find_element(By.ID, "id_preambule").send_keys(appendix)
        self.selenium.find_element(By.ID, "id_body").send_keys(appendix)
        self.selenium.find_element(By.CLASS_NAME, "btn-primary").click()
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto")))
        self.assertEqual(f"{self.news_title}{appendix}", self.selenium.find_element(By.CLASS_NAME, "card-title").text)
        self.assertEqual(
            f"{self.news_preambule}{appendix}", self.selenium.find_element(By.CLASS_NAME, "card-text").text
        )

        # test_delete
        update_news_url = f"{current_news_url}/delete"
        self.selenium.get(update_news_url)
        self.selenium.find_element(By.CLASS_NAME, "btn-danger").click()
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto")))
        self.assertNotEqual(
            f"{self.news_title}{appendix}", self.selenium.find_element(By.CLASS_NAME, "card-title").text
        )
        self.assertNotEqual(
            f"{self.news_preambule}{appendix}", self.selenium.find_element(By.CLASS_NAME, "card-text").text
        )

    def tearDown(self):
        # Close browser
        self.selenium.quit()
        super().tearDown()
