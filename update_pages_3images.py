#!/usr/bin/env python3
"""
기존 900개 페이지에 이미지 3개씩 업데이트
현재 확보된 이미지 URL을 조합해서 각 페이지마다 다른 3개 배치
"""
import os, re

# 확보된 이미지 URL 목록 (지금까지 생성한 것들)
IMAGES = [
    "https://www.genspark.ai/api/files/s/8d8VcPcp?cache_control=3600",   # 고압세척 하수관
    "https://www.genspark.ai/api/files/s/CXoQL4re?cache_control=3600",   # 싱크대 작업
    "https://www.genspark.ai/api/files/s/N6x6qZdH?cache_control=3600",   # 싱크대 작업2
    "https://www.genspark.ai/api/files/s/6mhUOyn7?cache_control=3600",   # 드레인 기계
    "https://www.genspark.ai/api/files/s/0eASCDBe?cache_control=3600",   # 드레인 기계2
    "https://www.genspark.ai/api/files/s/odIUnii1?cache_control=3600",   # 주방 드레인 기계 (NEW)
]

base_dir = "docs/area"
count = 0

for i, dirname in enumerate(sorted(os.listdir(base_dir))):
    filepath = os.path.join(base_dir, dirname, "index.html")
    if not os.path.isfile(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 각 페이지마다 3개의 서로 다른 이미지 배정
    img1 = IMAGES[i % len(IMAGES)]
    img2 = IMAGES[(i + 2) % len(IMAGES)]
    img3 = IMAGES[(i + 4) % len(IMAGES)]
    
    # 기존 img src 교체 (첫번째, 두번째)
    # og:image도 교체
    img_pattern = re.compile(r'(https://www\.genspark\.ai/api/files/s/[^"?]+\?cache_control=3600)')
    
    found_imgs = img_pattern.findall(html)
    
    # 3번째 이미지 섹션 추가 (서비스 요금 안내 전에)
    if '<h2>서비스 요금 안내</h2>' in html and html.count('img-wrap') < 3:
        third_img_section = f'''
<div class="img-wrap">
<img src="{img3}" alt="전문 장비 클로즈업 - 제우스시설관리" loading="lazy">
<p class="img-caption">▲ 제우스시설관리 전문 장비 클로즈업</p>
</div>

'''
        html = html.replace('<h2>서비스 요금 안내</h2>', third_img_section + '<h2>서비스 요금 안내</h2>')
    
    # 기존 이미지 URL 교체 (1번째 → img1, 2번째 → img2)
    replacements = 0
    def replace_img(match):
        nonlocal replacements
        replacements += 1
        if replacements == 1:
            return img1
        elif replacements == 2:
            return img2
        elif replacements == 3:
            return img3
        else:
            return IMAGES[replacements % len(IMAGES)]
    
    html = img_pattern.sub(replace_img, html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    count += 1
    if count % 100 == 0:
        print(f"  [{count}] 업데이트 완료...")

print(f"\n✅ 총 {count}개 페이지에 이미지 3개씩 업데이트 완료!")
