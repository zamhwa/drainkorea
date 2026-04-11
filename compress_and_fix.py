#!/usr/bin/env python3
"""
1. 이미지 압축 (2MB → 200-300KB)
2. 네이버 사이트 인증 메타태그 추가
3. 전 페이지 일괄 적용
"""
import os
import re
from PIL import Image

IMG_DIR = "docs/images"
AREA_DIR = "docs/area"

NAVER_META = '<meta name="naver-site-verification" content="5ffb7ec3cbd3c0f2b1d78d498a5f69a2aa367a3b" />'

# 1. 이미지 압축
print("=== 이미지 압축 시작 ===")
for fname in os.listdir(IMG_DIR):
    if not fname.endswith('.jpg'):
        continue
    fpath = os.path.join(IMG_DIR, fname)
    size_before = os.path.getsize(fpath)
    if size_before < 500000:  # 500KB 미만이면 스킵
        print(f"  {fname}: {size_before//1024}KB - 이미 작음, 스킵")
        continue

    try:
        img = Image.open(fpath)
        # 가로 1200px로 리사이즈 (SEO 최적 크기)
        if img.width > 1200:
            ratio = 1200 / img.width
            new_size = (1200, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        # JPEG 품질 75로 저장
        img.save(fpath, 'JPEG', quality=75, optimize=True)
        size_after = os.path.getsize(fpath)
        print(f"  {fname}: {size_before//1024}KB → {size_after//1024}KB ({(1-size_after/size_before)*100:.0f}% 감소)")
    except Exception as e:
        print(f"  {fname}: 오류 - {e}")

# 2. 네이버 인증 메타태그 + 메인 페이지에도 추가
print("\n=== 네이버 인증 메타태그 추가 ===")

# 메인 페이지
main_index = "docs/index.html"
if os.path.exists(main_index):
    with open(main_index, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'naver-site-verification' not in content:
        content = content.replace('<meta charset="UTF-8">', f'<meta charset="UTF-8">\n{NAVER_META}')
        with open(main_index, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  docs/index.html에 추가 완료")

# 906개 area 페이지
counter = 0
folders = sorted(os.listdir(AREA_DIR))
for folder in folders:
    html_path = os.path.join(AREA_DIR, folder, "index.html")
    if not os.path.exists(html_path):
        continue

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'naver-site-verification' not in content:
        content = content.replace('<meta charset="UTF-8">', f'<meta charset="UTF-8">\n{NAVER_META}')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)

    counter += 1
    if counter % 100 == 0:
        print(f"  진행: {counter}/{len(folders)}")

print(f"\n✅ 이미지 압축 + 네이버 인증 메타태그 {counter}개 페이지에 추가 완료")
