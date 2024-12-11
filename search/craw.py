from logic.x_crawling import fetch_and_extract_trends
from dotenv import load_dotenv
import os

# 최상위 .env 파일 로드
base_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=base_env_path)

def main():
    # 크롤링할 URL
    url = os.getenv("TRENDS24_URL", "https://trends24.in/korea/")  # 기본 URL 설정

    try:
        fetch_and_extract_trends(url)
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()