#!/usr/bin/env python3
"""
906개 페이지 일괄 수정:
1. 3번째 이미지 추가 (비용 안내 아래, "왜 제우스시설관리인가?" 위)
2. "30분~1시간 이내 긴급출동" → "28분 내 출동"
"""
import os
import re

AREA_DIR = "docs/area"
BASE_IMG_URL = "https://drainkorea.com/images"

# 키워드별 이미지 매핑 (3장씩)
KEYWORD_IMG_MAP = {
    "hasugumaghim": ["sewer.jpg", "pipes.jpg", "tools.jpg"],
    "byeongimaghim": ["toilet.jpg", "plumber-fix.jpg", "tools.jpg"],
    "singkeudaemaghim": ["kitchen-sink.jpg", "sink-drain.jpg", "plumber-sink.jpg"],
    "hasugwanseceog": ["sewer.jpg", "pipes.jpg", "hero-plumber.jpg"],
    "baegwancheongso": ["pipes.jpg", "tools.jpg", "hero-plumber.jpg"],
    "jeonghwajocheongso": ["sewer.jpg", "hero-plumber.jpg", "tools.jpg"],
    "maenholcheongso": ["sewer.jpg", "pipes.jpg", "hero-plumber.jpg"],
    "hwajangsirmaghim": ["toilet.jpg", "plumber-fix.jpg", "pipes.jpg"],
    "baesugumaghim": ["sink-drain.jpg", "pipes.jpg", "tools.jpg"],
    "yokjomaghim": ["plumber-fix.jpg", "sink-drain.jpg", "pipes.jpg"],
    "semyeondaemaghim": ["sink-drain.jpg", "plumber-sink.jpg", "tools.jpg"],
    "hasugunaemse": ["sewer.jpg", "pipes.jpg", "hero-plumber.jpg"],
    "baegwanyeogru": ["pipes.jpg", "sewer.jpg", "plumber-fix.jpg"],
    "osugwanmaghim": ["sewer.jpg", "pipes.jpg", "tools.jpg"],
    "hasuguttulgi": ["sewer.jpg", "hero-plumber.jpg", "tools.jpg"],
    "baegwannusu": ["pipes.jpg", "plumber-fix.jpg", "tools.jpg"],
    "geuriseuteulaebcheongso": ["kitchen-sink.jpg", "sink-drain.jpg", "tools.jpg"],
    "hasudogongsa": ["sewer.jpg", "pipes.jpg", "hero-plumber.jpg"],
    "baegwangyoche": ["pipes.jpg", "plumber-fix.jpg", "tools.jpg"],
    "usugwanmaghim": ["sewer.jpg", "pipes.jpg", "hero-plumber.jpg"],
}

# 키워드별 한글 이름
KEYWORD_KR = {
    "hasugumaghim": "하수구막힘",
    "byeongimaghim": "변기막힘",
    "singkeudaemaghim": "싱크대막힘",
    "hasugwanseceog": "하수관세척",
    "baegwancheongso": "배관청소",
    "jeonghwajocheongso": "정화조청소",
    "maenholcheongso": "맨홀청소",
    "hwajangsirmaghim": "화장실막힘",
    "baesugumaghim": "배수구막힘",
    "yokjomaghim": "욕조막힘",
    "semyeondaemaghim": "세면대막힘",
    "hasugunaemse": "하수구냄새",
    "baegwanyeogru": "배관역류",
    "osugwanmaghim": "오수관막힘",
    "hasuguttulgi": "하수구뚫기",
    "baegwannusu": "배관누수",
    "geuriseuteulaebcheongso": "그리스트랩청소",
    "hasudogongsa": "하수도공사",
    "baegwangyoche": "배관교체",
    "usugwanmaghim": "우수관막힘",
}

def get_city_keyword(folder_name):
    parts = folder_name.split("-", 1)
    city_en = parts[0] if len(parts) > 0 else ""
    keyword_en = parts[1] if len(parts) > 1 else ""
    return city_en, keyword_en

def get_city_kr(content):
    """HTML에서 한글 도시명 추출"""
    m = re.search(r'<h1>(\S+)\s', content)
    if m:
        return m.group(1)
    return ""

def fix_page(html_path, folder_name):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    city_en, keyword_en = get_city_keyword(folder_name)
    city_kr = get_city_kr(content)
    keyword_kr = KEYWORD_KR.get(keyword_en, "배관작업")
    images = KEYWORD_IMG_MAP.get(keyword_en, ["hero-plumber.jpg", "pipes.jpg", "tools.jpg"])

    # 1. "30분~1시간 이내 긴급출동" → "28분 내 출동"
    content = content.replace("30분~1시간 이내 긴급출동", "28분 내 출동")

    # 2. 3번째 이미지가 없으면 추가 (비용 안내 섹션 아래에)
    img_count = content.count('<img ')
    if img_count < 3:
        third_img = images[2]
        third_img_html = f"""
<div class="img-wrap">
<img src="{BASE_IMG_URL}/{third_img}" alt="{city_kr} {keyword_kr} 작업 완료 - 제우스시설관리" loading="lazy">
<p class="img-caption">▲ {city_kr} {keyword_kr} 전문 장비 투입 작업 현장</p>
</div>

"""
        # "왜 제우스시설관리인가?" 섹션 앞에 삽입
        insert_point = '<h2>왜 제우스시설관리인가?</h2>'
        if insert_point in content:
            content = content.replace(insert_point, third_img_html + insert_point)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 실행
counter = 0
folders = sorted(os.listdir(AREA_DIR))

for folder in folders:
    html_path = os.path.join(AREA_DIR, folder, "index.html")
    if os.path.exists(html_path):
        fix_page(html_path, folder)
        counter += 1
        if counter % 100 == 0:
            print(f"  진행: {counter}/{len(folders)} 완료...")

print(f"\n✅ 총 {counter}개 페이지 수정 완료 (3번째 이미지 추가 + 28분 내 출동)")
