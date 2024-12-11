import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from dotenv import load_dotenv
import os
import json

# 환경 변수 로드
load_dotenv()

class NaverSessionManager:
    def __init__(self):
        self.driver = None
        self.wait = None

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--enable-javascript')
        chrome_options.add_argument('--enable-unsafe-swiftshader')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.implicitly_wait(10)

    def safe_click(self, element, timeout=3):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                element.click()
                return True
            except ElementClickInterceptedException:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception:
                    time.sleep(0.5)
        return False

    def auto_login(self, user_id, user_pw):
        try:
            self.driver.get("https://nid.naver.com/nidlogin.login")
            time.sleep(2)
            
            id_input = self.wait.until(EC.presence_of_element_located((By.ID, 'id')))
            id_input.clear()
            id_input.click()
            pyperclip.copy(user_id)
            id_input.send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            
            pw_input = self.wait.until(EC.presence_of_element_located((By.ID, 'pw')))
            pw_input.clear()
            pw_input.click()
            pyperclip.copy(user_pw)
            pw_input.send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            
            login_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'log.login')))
            self.safe_click(login_button)
            
            try:
                self.wait.until(EC.url_contains("https://www.naver.com"))
                print("로그인 성공")
                return True
            except TimeoutException:
                print("로그인 시간 초과")
                return False
            
        except Exception as e:
            print(f"로그인 실패: {str(e)}")
            return False

    def find_and_click_write_button(self):
        try:
            self.driver.get("https://blog.naver.com")
            time.sleep(3)
            
            write_button_selectors = [
                "//a[contains(text(), '글쓰기')]",
                "//a[@class='btn_write']",
                "//a[contains(@class, 'write')]"
            ]
            
            write_button = None
            for selector in write_button_selectors:
                try:
                    write_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if write_button and self.safe_click(write_button):
                time.sleep(3)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                print("새 창으로 포커스 전환 성공")
                return True
            else:
                print("글쓰기 버튼을 찾을 수 없습니다")
                return False
            
        except Exception as e:
            print(f"'글쓰기' 버튼 클릭 실패: {str(e)}")
            return False

    def wait_for_editor_load(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "mainFrame")))
            self.driver.switch_to.frame("mainFrame")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".se-component-content")))
            print("에디터 로드 성공")
            return True
        except Exception as e:
            print(f"에디터 로드 실패: {str(e)}")
            return False

    def click_publish_button(self):
        try:
            self.driver.switch_to.default_content()
            time.sleep(2)
            
            self.driver.switch_to.frame("mainFrame")
            
            publish_button_selectors = [
                "button.publish_btn__m9KHH",
                "button[class*='publish']",
                "//button[contains(@class, 'publish_btn__m9KHH')]",
                "//button[.//span[contains(text(), '발행')]]"
            ]
            
            publish_button = None
            for selector in publish_button_selectors:
                try:
                    if selector.startswith("//"):
                        publish_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        publish_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if publish_button and publish_button.is_displayed():
                        print("발행 버튼 발견:", selector)
                        break
                except:
                    continue
            
            if not publish_button:
                print("첫 번째 발행 버튼을 찾을 수 없습니다.")
                self.driver.save_screenshot("first_publish_button_not_found.png")
                return False

            self.driver.execute_script("arguments[0].scrollIntoView(true);", publish_button)
            time.sleep(1)
            
            self.safe_click(publish_button)
            print("첫 번째 발행 버튼 클릭 성공")
            time.sleep(2)

            # 두 번째 발행 버튼이 있는 레이어를 기다리고 클릭
            second_publish_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='seOnePublishBtn']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", second_publish_button)
            time.sleep(1)

            if self.safe_click(second_publish_button):
                print("두 번째 발행 버튼 클릭 성공")
                time.sleep(3)
                return True
            else:
                print("두 번째 발행 버튼 클릭 실패")
                self.driver.save_screenshot("second_publish_button_not_found.png")
                return False
                    
        except Exception as e:
            print(f"발행 버튼 클릭 과정 중 오류: {str(e)}")
            self.driver.save_screenshot("error_screenshot.png")
            return False


    def write_and_publish_post(self, title="test", content="test"):
        try:
            if not self.wait_for_editor_load():
                return False

            title_placeholder = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".se-placeholder"))
            )
            title_placeholder.click()
            time.sleep(1)
            
            active_element = self.driver.switch_to.active_element
            pyperclip.copy(title)
            active_element.send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            
            active_element.send_keys(Keys.ENTER)
            time.sleep(1)
            
            active_element = self.driver.switch_to.active_element
            pyperclip.copy(content)
            active_element.send_keys(Keys.CONTROL, 'v')
            time.sleep(2)
            
            return self.click_publish_button()
            
        except Exception as e:
            print(f"게시글 작성 실패: {str(e)}")
            self.driver.save_screenshot("error_screenshot.png")
            return False

    def close(self):
        if self.driver:
            self.driver.quit()

# JSON 파일에서 읽기
def read_post_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            title = data.get("title", "")
            content = data.get("content", "")
        return title, content
    except Exception as e:
        print(f"JSON 파일 읽기 실패: {str(e)}")
        return None, None

def main():
    print("작업을 바로 시작합니다.")
    
    output_folder = "blog"  # JSON 파일이 저장된 폴더
    json_files = [f for f in os.listdir(output_folder) if f.endswith(".json")]

    if not json_files:
        print("출력 폴더에 JSON 파일이 없습니다.")
        return

    # 환경 변수에서 아이디와 비밀번호 가져오기
    naver_id = os.getenv("NAVER_ID")
    naver_pw = os.getenv("NAVER_PW")
    
    manager = NaverSessionManager()
    manager.setup_driver()
    
    try:
        if manager.auto_login(naver_id, naver_pw):
            time.sleep(2)
            for json_file in json_files:
                file_path = os.path.join(output_folder, json_file)
                title, content = read_post_from_json(file_path)

                if not title or not content:
                    print(f"파일 {json_file}에서 제목 또는 내용을 읽는 데 실패했습니다.")
                    continue

                if manager.find_and_click_write_button():
                    time.sleep(2)
                    result = manager.write_and_publish_post(
                        title=title, 
                        content=content
                    )
                    if not result:
                        print(f"파일 {json_file}의 발행 프로세스 실패")
                else:
                    print("글쓰기 버튼 클릭 실패")
        else:
            print("로그인 실패")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {str(e)}")
    finally:
        manager.close()

if __name__ == "__main__":
    main()
