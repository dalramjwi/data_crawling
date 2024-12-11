import os
import json
from datetime import datetime

# 블로그 템플릿 파일 저장 경로
TEMPLATE_FOLDER = os.path.join("template")
TEMPLATE_FILE = os.path.join(TEMPLATE_FOLDER, "blog_template.txt")

# 가장 늦은 날짜와 시간의 JSON 파일 찾기
def find_latest_json(folder):
    latest_date_folder = max([os.path.join(folder, d) for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))], key=os.path.getmtime)
    latest_json_file = max([os.path.join(latest_date_folder, f) for f in os.listdir(latest_date_folder) if f.endswith(".json")], key=os.path.getmtime)
    return latest_date_folder, latest_json_file

# JSON 파일 읽기
def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 템플릿 파일 읽기
def read_template():
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"템플릿 파일이 없습니다: {TEMPLATE_FILE}")
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
        return file.read()

# 블로그 글 생성
def create_blog_post(data, template):
    if not data:
        return {}

    # 첫 번째 데이터를 중심으로 작성
    first_item = data[0]
    keyword = first_item.get("keyword", "알 수 없음")
    tweet_count = first_item.get("tweet_count", "알 수 없음")

    # 나머지 키워드 열거
    other_keywords = [item.get("keyword", "알 수 없음") for item in data[1:]]
    other_keywords_text = "\n".join([f"- {kw}" for kw in other_keywords]) if other_keywords else "없음"

    # 템플릿 채우기
    blog_post = template.format(
        키워드=keyword, 
        트윗_수=tweet_count, 
        다른_키워드=other_keywords_text
    )

    return {
        "title": f"# {keyword} - 지금 트위터에서 화제인 이유",
        "content": blog_post
    }

# 메인 실행
if __name__ == "__main__":
    data_folder = os.path.join("data")  # JSON 데이터 폴더
    latest_date_folder, latest_file = find_latest_json(data_folder)

    if latest_file:
        print(f"가장 최근 파일: {latest_file}")
        trends_data = read_json(latest_file)

        try:
            template = read_template()
        except FileNotFoundError as e:
            print(e)
            exit(1)

        blog_post_data = create_blog_post(trends_data, template)

        # JSON 형태로 저장
        timestamp = os.path.basename(latest_file).split(".")[0]
        output_dir = os.path.join("blog", os.path.basename(latest_date_folder))
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{timestamp}_blog_post.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(blog_post_data, file, ensure_ascii=False, indent=4)

        print(f"블로그 글이 저장되었습니다: {output_file}")
    else:
        print("JSON 데이터를 찾을 수 없습니다.")
