import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# 스크래핑할 URL
url = "https://trends24.in/korea/"
response = requests.get(url)
response.encoding = 'utf-8'  # UTF-8 인코딩 보장

soup = BeautifulSoup(response.text, "html.parser")

# 메인 타임라인 컨테이너 찾기
timeline_container = soup.find(id="timeline-container")

# 현재 시간 (KST)
kst_offset = timedelta(hours=9)  # UTC+9
def get_kst_time(utc_time):
    return utc_time + kst_offset

current_time = datetime.utcnow()
kst_time = get_kst_time(current_time)
print(f"현재 한국 시간: {kst_time.strftime('%Y-%m-%d %H:%M:%S')}")  # 현재 한국 시간 출력

# "data" 폴더 생성
base_folder = "data"
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# 로그 파일 생성
log_file_path = os.path.join(base_folder, "scraping.log")
def write_log(message):
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

# 각 시간별 데이터 추출
for list_container in timeline_container.find_all(class_="list-container"):
    # <h3 class="title" data-timestamp="...">에서 타임스탬프 추출
    timestamp_tag = list_container.find("h3", class_="title")
    if timestamp_tag and "data-timestamp" in timestamp_tag.attrs:
        unix_timestamp = float(timestamp_tag["data-timestamp"])
        data_time_utc = datetime.utcfromtimestamp(unix_timestamp)
        data_time_kst = get_kst_time(data_time_utc)
        print(f"데이터 타임스탬프 (KST): {data_time_kst.strftime('%Y-%m-%d %H:%M:%S')}")  # 데이터 타임스탬프 출력

        # 날짜 기반 폴더 이름 결정
        folder_name = os.path.join(base_folder, data_time_kst.strftime("%Y-%m-%d"))
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # 시간 기반 파일 이름 결정 (분 제거)
        file_name = f"{data_time_kst.strftime('%H')}.json"
        full_path = os.path.join(folder_name, file_name)

        # 파일 존재 여부 확인
        if os.path.exists(full_path):
            message = f"파일이 이미 존재합니다: {full_path}. 스크래핑을 건너뜁니다."
            print(message)
            write_log(message)
            continue  # 파일이 존재하면 스크래핑 건너뛰기
    else:
        folder_name = os.path.join(base_folder, "unknown_time")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        full_path = os.path.join(folder_name, "unknown_time.json")

    # 해당 시간의 트렌드 추출
    trends = []
    for item in list_container.find_all("li"):
        trend_name = item.find("a").text.strip()
        tweet_count_tag = item.find("span", class_="tweet-count")
        # data-count 속성이 있으면 사용, 없으면 텍스트 사용
        tweet_count = (
            tweet_count_tag["data-count"]
            if tweet_count_tag and "data-count" in tweet_count_tag.attrs
            else tweet_count_tag.text.strip() if tweet_count_tag else "N/A"
        )

        trends.append({
            "키워드": trend_name,
            "트윗 수": tweet_count
        })

    # 추출된 데이터를 JSON 파일로 저장
    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(trends, file, ensure_ascii=False, indent=4)

    message = f"데이터가 성공적으로 저장되었습니다: {full_path}"
    print(message)
    write_log(message)

# 완료 메시지 출력
completion_message = "스크래핑 및 파일 저장이 완료되었습니다!"
print(completion_message)
write_log(completion_message)