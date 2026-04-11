#!/usr/bin/env python3
"""
900개 페이지의 이미지 src를 로컬 고유 이미지로 교체
/images/xxx.jpg → 각 페이지 폴더의 img1.jpg, img2.jpg, img3.jpg
"""
import os
import re

AREA_DIR = "docs/area"

counter = 0
folders = sorted(os.listdir(AREA_DIR))

for folder in folders:
    html_path = os.path.join(AREA_DIR, folder, "index.html")
    if not os.path.exists(html_path):
        continue

    # 로컬 이미지가 있는지 확인
    has_local = all(
        os.path.exists(os.path.join(AREA_DIR, folder, f"img{i}.jpg"))
        for i in [1, 2, 3]
    )
    if not has_local:
        continue

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 이미지 src 교체 (순서대로 1, 2, 3번째 img 태그)
    img_index = [0]
    def replace_img_src(match):
        img_index[0] += 1
        idx = img_index[0]
        if idx <= 3:
            # 상대 경로로 변경
            return f'src="img{idx}.jpg"'
        return match.group(0)

    new_content = re.sub(
        r'src="https://drainkorea\.com/images/[^"]*"',
        replace_img_src,
        content
    )

    # og:image도 첫 번째 로컬 이미지로 변경 (절대 경로 유지)
    new_content = re.sub(
        r'(og:image" content=")[^"]*"',
        f'\\1https://drainkorea.com/area/{folder}/img1.jpg"',
        new_content
    )

    # Schema.org image도 변경
    new_content = re.sub(
        r'("image":\s*")[^"]*"',
        f'\\1https://drainkorea.com/area/{folder}/img1.jpg"',
        new_content
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    counter += 1
    if counter % 100 == 0:
        print(f"  진행: {counter}")

print(f"\n✅ {counter}개 페이지 이미지 경로 업데이트 완료")
