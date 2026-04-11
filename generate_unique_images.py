#!/usr/bin/env python3
"""
900개 페이지별 고유 이미지 3장씩 생성
- 기존 9개 이미지를 베이스로
- 도시명+키워드 오버레이 텍스트 삽입
- 색온도/밝기 미세 조정으로 시각적 차별화
- 각 페이지 폴더에 img1.jpg, img2.jpg, img3.jpg 저장
"""
import os
import random
import hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

AREA_DIR = "docs/area"
BASE_IMG_DIR = "docs/images"
FONT_PATH = "/tmp/NotoSansCJKkr-Bold.otf"

# 키워드별 이미지 매핑
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

# 도시별 한글명
CITY_KR = {}

def get_city_kr_from_html(html_path):
    """HTML 파일에서 도시 한글명 추출"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        import re
        m = re.search(r'<h1>(\S+)\s', content)
        if m:
            return m.group(1)
    except:
        pass
    return ""

def create_overlay_image(base_img_path, city_kr, keyword_kr, seed, output_path):
    """베이스 이미지에 오버레이를 추가하여 고유 이미지 생성"""
    random.seed(seed)

    img = Image.open(base_img_path).convert('RGB')

    # 1. 미세 크롭 (2-8% 랜덤 크롭으로 구도 변경)
    w, h = img.size
    crop_pct = random.uniform(0.02, 0.08)
    left = int(w * random.uniform(0, crop_pct))
    top = int(h * random.uniform(0, crop_pct))
    right = w - int(w * random.uniform(0, crop_pct))
    bottom = h - int(h * random.uniform(0, crop_pct))
    img = img.crop((left, top, right, bottom))

    # 리사이즈를 800x600으로 통일
    img = img.resize((800, 600), Image.LANCZOS)

    # 2. 색온도/밝기 미세 조정
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(random.uniform(0.92, 1.08))

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(random.uniform(0.95, 1.05))

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(random.uniform(0.9, 1.1))

    # 3. 텍스트 오버레이 (반투명 배너)
    draw = ImageDraw.Draw(img)

    # 하단 배너
    banner_h = 60
    banner_y = 600 - banner_h
    overlay = Image.new('RGBA', (800, banner_h), (0, 0, 0, 160))
    img_rgba = img.convert('RGBA')
    img_rgba.paste(overlay, (0, banner_y), overlay)
    img = img_rgba.convert('RGB')

    draw = ImageDraw.Draw(img)

    # 텍스트
    try:
        font_large = ImageFont.truetype(FONT_PATH, 28)
        font_small = ImageFont.truetype(FONT_PATH, 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    text_main = f"{city_kr} {keyword_kr} 전문"
    text_sub = "제우스시설관리 | 010-4406-1788"

    # 텍스트 중앙 배치
    bbox = draw.textbbox((0, 0), text_main, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((800 - tw) // 2, banner_y + 5), text_main, fill=(255, 255, 255), font=font_large)

    bbox2 = draw.textbbox((0, 0), text_sub, font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((800 - tw2) // 2, banner_y + 36), text_sub, fill=(255, 204, 2), font=font_small)

    # 4. 저장
    img.save(output_path, 'JPEG', quality=80, optimize=True)

# 메인 실행
print("=== 페이지별 고유 이미지 생성 시작 ===")

# 베이스 이미지 캐시
base_images = {}
for fname in os.listdir(BASE_IMG_DIR):
    if fname.endswith('.jpg'):
        base_images[fname] = os.path.join(BASE_IMG_DIR, fname)

folders = sorted(os.listdir(AREA_DIR))
counter = 0
total_images = 0

for folder in folders:
    html_path = os.path.join(AREA_DIR, folder, "index.html")
    if not os.path.exists(html_path):
        continue

    parts = folder.split("-", 1)
    city_en = parts[0] if len(parts) > 0 else ""
    keyword_en = parts[1] if len(parts) > 1 else ""

    city_kr = get_city_kr_from_html(html_path)
    keyword_kr = KEYWORD_KR.get(keyword_en, "배관작업")
    images = KEYWORD_IMG_MAP.get(keyword_en, ["hero-plumber.jpg", "pipes.jpg", "tools.jpg"])

    # 각 페이지에 3장의 고유 이미지 생성
    img_dir = os.path.join(AREA_DIR, folder)
    for i, base_fname in enumerate(images):
        if base_fname not in base_images:
            continue

        # seed를 폴더명+인덱스로 만들어 결정적이면서 고유하게
        seed = int(hashlib.md5(f"{folder}-{i}".encode()).hexdigest()[:8], 16)
        output_path = os.path.join(img_dir, f"img{i+1}.jpg")

        create_overlay_image(
            base_images[base_fname],
            city_kr,
            keyword_kr,
            seed,
            output_path
        )
        total_images += 1

    counter += 1
    if counter % 50 == 0:
        print(f"  진행: {counter}/{len(folders)} ({total_images}장 생성)")

print(f"\n✅ {counter}개 페이지에 총 {total_images}장 고유 이미지 생성 완료")
