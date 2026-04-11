#!/usr/bin/env python3
"""
drainkorea.com 홈페이지용 1000개 SEO 페이지 생성기
도시(50개) × 키워드(20개) = 1000개 조합
"""
import os
import json
from datetime import datetime

# ===== 도시 목록 (50개) =====
CITIES = [
    # 경기도 (30개)
    {"ko": "수원", "en": "suwon", "sub": "영통구, 장안구, 권선구, 팔달구"},
    {"ko": "성남", "en": "seongnam", "sub": "분당구, 수정구, 중원구"},
    {"ko": "용인", "en": "yongin", "sub": "수지구, 기흥구, 처인구"},
    {"ko": "안양", "en": "anyang", "sub": "만안구, 동안구"},
    {"ko": "안산", "en": "ansan", "sub": "상록구, 단원구"},
    {"ko": "부천", "en": "bucheon", "sub": "원미구, 소사구, 오정구"},
    {"ko": "화성", "en": "hwaseong", "sub": "동탄, 봉담, 향남, 남양"},
    {"ko": "평택", "en": "pyeongtaek", "sub": "평택역, 송탄, 안중, 포승"},
    {"ko": "시흥", "en": "siheung", "sub": "정왕동, 배곧, 월곶"},
    {"ko": "광명", "en": "gwangmyeong", "sub": "철산동, 하안동, 소하동"},
    {"ko": "하남", "en": "hanam", "sub": "미사, 풍산동, 감일동"},
    {"ko": "의정부", "en": "uijeongbu", "sub": "의정부역, 민락동, 호원동"},
    {"ko": "김포", "en": "gimpo", "sub": "장기동, 풍무동, 운양동, 구래동"},
    {"ko": "고양", "en": "goyang", "sub": "일산동구, 일산서구, 덕양구"},
    {"ko": "파주", "en": "paju", "sub": "운정, 금촌, 교하, 문산"},
    {"ko": "이천", "en": "icheon", "sub": "증포동, 창전동, 관고동"},
    {"ko": "광주", "en": "gwangju-gg", "sub": "경안동, 송정동, 오포읍"},
    {"ko": "양주", "en": "yangju", "sub": "양주역, 덕계동, 옥정"},
    {"ko": "오산", "en": "osan", "sub": "오산역, 세교동, 원동"},
    {"ko": "구리", "en": "guri", "sub": "갈매동, 인창동, 수택동"},
    {"ko": "군포", "en": "gunpo", "sub": "산본동, 금정동, 당정동"},
    {"ko": "의왕", "en": "uiwang", "sub": "내손동, 오전동, 포일동"},
    {"ko": "남양주", "en": "namyangju", "sub": "다산, 별내, 호평, 평내"},
    {"ko": "동두천", "en": "dongducheon", "sub": "생연동, 지행동, 보산동"},
    {"ko": "과천", "en": "gwacheon", "sub": "별양동, 부림동, 중앙동"},
    # 서울 (20개 주요 구)
    {"ko": "강남구", "en": "gangnam", "sub": "역삼동, 삼성동, 논현동, 대치동"},
    {"ko": "서초구", "en": "seocho", "sub": "서초동, 방배동, 반포동, 잠원동"},
    {"ko": "송파구", "en": "songpa", "sub": "잠실동, 가락동, 문정동, 위례"},
    {"ko": "강동구", "en": "gangdong", "sub": "천호동, 길동, 명일동, 상일동"},
    {"ko": "마포구", "en": "mapo", "sub": "합정동, 상수동, 연남동, 망원동"},
    {"ko": "영등포구", "en": "yeongdeungpo", "sub": "여의도, 영등포동, 당산동"},
    {"ko": "구로구", "en": "guro", "sub": "구로동, 개봉동, 고척동, 신도림"},
    {"ko": "관악구", "en": "gwanak", "sub": "신림동, 봉천동, 서울대입구"},
    {"ko": "동작구", "en": "dongjak", "sub": "사당동, 노량진, 흑석동"},
    {"ko": "서대문구", "en": "seodaemun", "sub": "연희동, 홍제동, 신촌"},
    {"ko": "은평구", "en": "eunpyeong", "sub": "응암동, 역촌동, 불광동"},
    {"ko": "성동구", "en": "seongdong", "sub": "성수동, 왕십리, 금호동"},
    {"ko": "노원구", "en": "nowon", "sub": "상계동, 중계동, 하계동"},
    {"ko": "강서구", "en": "gangseo", "sub": "화곡동, 마곡동, 발산동, 가양동"},
    {"ko": "양천구", "en": "yangcheon", "sub": "목동, 신정동, 신월동"},
    # 인천 (5개 주요 구)
    {"ko": "인천남동구", "en": "incheon-namdong", "sub": "구월동, 논현동, 만수동"},
    {"ko": "인천부평구", "en": "incheon-bupyeong", "sub": "부평역, 삼산동, 갈산동"},
    {"ko": "인천연수구", "en": "incheon-yeonsu", "sub": "송도, 연수동, 청학동"},
    {"ko": "인천서구", "en": "incheon-seo", "sub": "검단, 청라, 가좌동"},
    {"ko": "인천계양구", "en": "incheon-gyeyang", "sub": "계산동, 작전동, 효성동"},
]

# ===== 키워드 목록 (20개) =====
KEYWORDS = [
    {"ko": "하수구막힘", "en": "hasugumaghim", "desc": "하수구가 막혀 물이 내려가지 않는 문제를 전문 드레인 기계와 고압세척기로 해결"},
    {"ko": "변기막힘", "en": "byeongimaghim", "desc": "변기가 막혀 물이 넘치는 긴급 상황을 전문 장비로 신속 해결"},
    {"ko": "싱크대막힘", "en": "singkeudaemaghim", "desc": "주방 싱크대 배수구가 막혀 물이 빠지지 않는 문제를 전문 해결"},
    {"ko": "하수관세척", "en": "hasugwanseceog", "desc": "하수관 내부 오염물을 고압세척기로 깨끗하게 세척"},
    {"ko": "배관청소", "en": "baegwancheongso", "desc": "노후 배관 내부의 이물질과 스케일을 전문 장비로 청소"},
    {"ko": "정화조청소", "en": "jeonghwajocheongso", "desc": "정화조 내부 슬러지를 전문 장비로 청소하고 관리"},
    {"ko": "맨홀청소", "en": "maenholcheongso", "desc": "맨홀 내부 이물질 제거 및 하수도 정비"},
    {"ko": "화장실막힘", "en": "hwajangsirmaghim", "desc": "화장실 배수 시스템 막힘을 전문 장비로 완벽 해결"},
    {"ko": "배수구막힘", "en": "baesugumaghim", "desc": "바닥 배수구 막힘 문제를 드레인 기계로 해결"},
    {"ko": "욕조막힘", "en": "yokjomaghim", "desc": "욕조 배수구 막힘을 전문 장비로 신속 해결"},
    {"ko": "세면대막힘", "en": "semyeondaemaghim", "desc": "세면대 배수구 막힘을 전문 도구로 해결"},
    {"ko": "하수구냄새", "en": "hasugunaemse", "desc": "하수구에서 올라오는 악취 원인을 진단하고 해결"},
    {"ko": "배관역류", "en": "baegwanyeogru", "desc": "배관 역류 현상의 원인을 파악하고 전문 장비로 해결"},
    {"ko": "오수관막힘", "en": "osugwanmaghim", "desc": "오수관 막힘을 관로 내시경으로 진단하고 해결"},
    {"ko": "하수구뚫기", "en": "hasuguttulgi", "desc": "막힌 하수구를 전문 드레인 기계로 뚫어 해결"},
    {"ko": "배관누수", "en": "baegwannusu", "desc": "배관 누수 위치를 관로탐지기로 정확히 찾아 수리"},
    {"ko": "그리스트랩청소", "en": "geuriseuteulaebcheongso", "desc": "음식점 그리스트랩 청소 및 관리 전문 서비스"},
    {"ko": "하수도공사", "en": "hasudogongsa", "desc": "하수도 시설 보수 및 교체 공사 전문"},
    {"ko": "배관교체", "en": "baegwangyoche", "desc": "노후 배관을 새 배관으로 교체하는 전문 시공"},
    {"ko": "우수관막힘", "en": "usugwanmaghim", "desc": "빗물 우수관 막힘을 고압세척으로 해결"},
]

# 이미지 URL 목록
IMAGES = [
    "https://www.genspark.ai/api/files/s/8d8VcPcp?cache_control=3600",
    "https://www.genspark.ai/api/files/s/CXoQL4re?cache_control=3600",
    "https://www.genspark.ai/api/files/s/N6x6qZdH?cache_control=3600",
    "https://www.genspark.ai/api/files/s/6mhUOyn7?cache_control=3600",
    "https://www.genspark.ai/api/files/s/0eASCDBe?cache_control=3600",
]

def generate_content(city, keyword, img1, img2):
    """각 도시+키워드에 맞는 고유 콘텐츠 생성"""
    city_ko = city["ko"]
    sub = city["sub"]
    kw_ko = keyword["ko"]
    kw_desc = keyword["desc"]

    # 키워드별 서비스 설명 다양화
    service_sections = {
        "하수구막힘": f"""
        <h2>{city_ko} 하수구막힘 원인과 해결</h2>
        <p>{city_ko} 지역의 하수구막힘은 주로 기름때, 음식물 찌꺼기, 머리카락, 이물질 등이 배관 내부에 축적되어 발생합니다. 특히 오래된 건물이 많은 {sub} 일대에서는 배관 노후화로 인한 막힘이 빈번합니다.</p>
        <p>제우스시설관리는 <strong>관로 내시경 카메라</strong>로 막힘의 정확한 원인과 위치를 파악한 후, <strong>드레인 기계</strong>와 <strong>고압세척기</strong>를 투입하여 완벽하게 해결합니다. 단순히 뚫는 것이 아니라 배관 내벽까지 깨끗하게 세척하여 재발을 방지합니다.</p>""",
        "변기막힘": f"""
        <h2>{city_ko} 변기막힘 긴급 해결</h2>
        <p>변기막힘은 긴급한 상황입니다. {city_ko} {sub} 지역에서 변기가 막히면 <strong>제우스시설관리</strong>에 즉시 연락하세요. 물티슈, 생리대, 기저귀 등 이물질로 인한 막힘부터 배관 노후로 인한 구조적 문제까지 모두 해결합니다.</p>
        <p>저희는 <strong>전문 드레인 기계</strong>로 이물질을 안전하게 제거하고, <strong>내시경 카메라</strong>로 배관 상태를 확인하여 추가 문제가 없는지 점검합니다.</p>""",
        "싱크대막힘": f"""
        <h2>{city_ko} 싱크대막힘 전문 해결</h2>
        <p>{city_ko} {sub} 지역의 가정과 음식점에서 싱크대 막힘 문제가 자주 발생합니다. 기름때가 배관 내벽에 굳어붙고 음식물 찌꺼기가 쌓이면서 점점 물 빠짐이 느려지다 완전히 막히게 됩니다.</p>
        <p><strong>고압세척기</strong>로 배관 내부의 기름때를 완벽하게 제거하고, <strong>드레인 기계</strong>로 고착된 이물질을 물리적으로 파쇄합니다.</p>""",
    }

    # 기본 서비스 섹션 (위에 없는 키워드용)
    default_section = f"""
        <h2>{city_ko} {kw_ko} 전문 서비스</h2>
        <p>{city_ko} {sub} 지역에서 {kw_ko} 문제가 발생하면 <strong>제우스시설관리</strong>가 해결합니다. {kw_desc}하는 전문 서비스를 제공합니다.</p>
        <p>20년 이상의 현장 경험과 <strong>드레인 기계, 관로 내시경, 고압세척기, 관로탐지기</strong> 등 최첨단 장비를 보유하고 있어 어떤 상황에서도 정확한 진단과 완벽한 해결이 가능합니다.</p>"""

    section = service_sections.get(kw_ko, default_section)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{city_ko}{kw_ko} | 24시간 긴급출동 | 제우스시설관리</title>
<meta name="description" content="{city_ko} {kw_ko} 전문 해결. 24시간 응급 상황 대응, 출장비 무료, 미해결시 비용 0원. 010-4406-1788 긴급 출동.">
<meta name="keywords" content="{city_ko}{kw_ko},{city_ko}하수구막힘,{city_ko}변기막힘,{city_ko}배관청소,하수구뚫기,배수구막힘">
<link rel="canonical" href="https://drainkorea.com/area/{city['en']}-{keyword['en']}/">
<meta property="og:type" content="article">
<meta property="og:title" content="{city_ko}{kw_ko} 전문 해결 | 24시간 긴급출동">
<meta property="og:description" content="{city_ko} {kw_ko} 문제를 24시간 빠르게 해결합니다. 출장비 무료, 미해결시 비용 0원">
<meta property="og:url" content="https://drainkorea.com/area/{city['en']}-{keyword['en']}/">
<meta property="og:image" content="{img1}">
<meta property="og:locale" content="ko_KR">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{city_ko} {kw_ko} | 제우스시설관리",
  "image": "{img1}",
  "description": "{city_ko}에서 {kw_ko} 문제 해결. 24시간 긴급출동, 출장비 무료",
  "address": {{
    "@type": "PostalAddress",
    "addressRegion": "{city_ko}",
    "addressCountry": "KR"
  }},
  "telephone": "01044061788",
  "url": "https://drainkorea.com/area/{city['en']}-{keyword['en']}/",
  "priceRange": "₩80,000~₩300,000",
  "areaServed": "{city_ko}",
  "serviceType": "{kw_ko}"
}}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,'Malgun Gothic',sans-serif;color:#333;line-height:1.8}}
.hero{{background:linear-gradient(135deg,#1a237e,#0d47a1);color:#fff;padding:60px 20px;text-align:center}}
.hero h1{{font-size:2em;margin-bottom:15px}}
.hero p{{font-size:1.1em;opacity:0.9}}
.cta-btn{{display:inline-block;background:#ff6f00;color:#fff;padding:15px 40px;border-radius:50px;text-decoration:none;font-size:1.2em;font-weight:bold;margin:20px 10px;transition:0.3s}}
.cta-btn:hover{{background:#e65100;transform:scale(1.05)}}
.container{{max-width:900px;margin:0 auto;padding:40px 20px}}
h2{{color:#1a237e;font-size:1.6em;margin:30px 0 15px;border-left:4px solid #ff6f00;padding-left:15px}}
h3{{color:#0d47a1;font-size:1.3em;margin:25px 0 10px}}
.img-wrap{{margin:30px 0;text-align:center}}
.img-wrap img{{max-width:100%;border-radius:10px;box-shadow:0 4px 15px rgba(0,0,0,0.15)}}
.img-caption{{color:#888;font-size:0.9em;margin-top:8px}}
.service-box{{background:#f5f5f5;border-radius:12px;padding:25px;margin:20px 0}}
.price-table{{width:100%;border-collapse:collapse;margin:20px 0}}
.price-table th,.price-table td{{border:1px solid #ddd;padding:12px;text-align:center}}
.price-table th{{background:#1a237e;color:#fff}}
.contact-box{{background:linear-gradient(135deg,#1a237e,#0d47a1);color:#fff;border-radius:15px;padding:35px;text-align:center;margin:40px 0}}
.contact-box a{{color:#ffcc02;text-decoration:none;font-size:1.5em;font-weight:bold}}
.area-tags{{display:flex;flex-wrap:wrap;gap:8px;margin:15px 0}}
.area-tag{{background:#e3f2fd;color:#1a237e;padding:6px 14px;border-radius:20px;font-size:0.9em}}
footer{{background:#222;color:#aaa;text-align:center;padding:30px;font-size:0.9em}}
footer a{{color:#ffcc02;text-decoration:none}}
</style>
</head>
<body>

<div class="hero">
<h1>{city_ko} {kw_ko} 전문 해결</h1>
<p>24시간 긴급출동 | 출장비 무료 | 미해결시 비용 0원</p>
<a href="tel:010-4406-1788" class="cta-btn">📞 010-4406-1788 즉시 연결</a>
</div>

<div class="container">
{section}

<div class="img-wrap">
<img src="{img1}" alt="{city_ko} {kw_ko} 전문 해결 현장 - 제우스시설관리" loading="lazy">
<p class="img-caption">▲ {city_ko} 현장에서 전문 장비로 {kw_ko} 해결 작업 중</p>
</div>

<h2>제우스시설관리 전문 장비</h2>
<div class="service-box">
<p>✅ <strong>드레인 기계</strong> - 스프링 와이어로 배관 내 이물질을 물리적으로 파쇄·제거</p>
<p>✅ <strong>관로 내시경 카메라</strong> - 배관 내부를 실시간 영상으로 확인하여 정확한 진단</p>
<p>✅ <strong>고압세척기</strong> - 최대 200bar 고압수로 배관 내벽 오염물 완벽 세척</p>
<p>✅ <strong>관로탐지기</strong> - 매설 배관의 위치와 깊이를 정확히 탐지</p>
</div>

<div class="img-wrap">
<img src="{img2}" alt="{city_ko} {kw_ko} 고압세척 작업 - 제우스시설관리" loading="lazy">
<p class="img-caption">▲ 고압세척기를 이용한 배관 내부 청소 작업</p>
</div>

<h2>{city_ko} 서비스 지역</h2>
<div class="area-tags">
{"".join(f'<span class="area-tag">{s.strip()}</span>' for s in sub.split(","))}
</div>
<p>{city_ko} 전 지역에 <strong>30분~1시간 이내 긴급출동</strong>합니다. 야간·주말·공휴일 추가 요금 없이 동일한 서비스를 제공합니다.</p>

<h2>서비스 요금 안내</h2>
<table class="price-table">
<tr><th>서비스 항목</th><th>기본 요금</th><th>비고</th></tr>
<tr><td>하수구/변기/싱크대 막힘</td><td>80,000원~</td><td>현장 상태에 따라 변동</td></tr>
<tr><td>배관 고압세척</td><td>150,000원~</td><td>길이/상태에 따라 변동</td></tr>
<tr><td>관로 내시경 진단</td><td>100,000원~</td><td>진단 후 작업시 할인</td></tr>
<tr><td>정화조/맨홀 청소</td><td>200,000원~</td><td>용량에 따라 변동</td></tr>
</table>
<p>※ 출장비 무료 / 미해결시 비용 0원 / 정확한 견적은 현장 확인 후 안내</p>

<h2>왜 제우스시설관리인가?</h2>
<p><strong>20년 이상 현장 경험</strong>으로 어떤 복잡한 상황에서도 해결합니다. {city_ko} 지역에서 {kw_ko} 문제가 발생하면 전화 한 통으로 전문가가 출동합니다.</p>
<ul>
<li>24시간 365일 긴급출동 가능</li>
<li>최첨단 전문 장비 완비 (드레인 기계, 내시경, 고압세척기, 관로탐지기)</li>
<li>투명한 견적 - 작업 전 정확한 비용 안내</li>
<li>A/S 보장 - 동일 증상 재발시 무상 재시공</li>
<li>출장비 무료, 미해결시 비용 0원</li>
</ul>

<div class="contact-box">
<h3>지금 바로 전화하세요!</h3>
<p style="margin:15px 0"><a href="tel:010-4406-1788">📞 010-4406-1788</a></p>
<p>🌐 <a href="https://drainkorea.com">drainkorea.com</a></p>
<p style="margin-top:10px;opacity:0.8">서울특별시 구로구 개봉로3길 (개봉동 403-2)</p>
</div>
</div>

<footer>
<p>&copy; 2024 제우스시설관리 | <a href="https://drainkorea.com">drainkorea.com</a> | 010-4406-1788</p>
<p>{city_ko} {kw_ko} 전문 | 24시간 긴급출동</p>
</footer>

</body>
</html>"""


def main():
    base_dir = "docs/area"
    count = 0
    total = len(CITIES) * len(KEYWORDS)

    print(f"총 {total}개 페이지 생성 시작...")
    print(f"도시: {len(CITIES)}개, 키워드: {len(KEYWORDS)}개")
    print("=" * 50)

    for ci, city in enumerate(CITIES):
        for ki, keyword in enumerate(KEYWORDS):
            idx = ci * len(KEYWORDS) + ki
            img1 = IMAGES[idx % len(IMAGES)]
            img2 = IMAGES[(idx + 2) % len(IMAGES)]

            folder_name = f"{city['en']}-{keyword['en']}"
            folder_path = os.path.join(base_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            html = generate_content(city, keyword, img1, img2)

            with open(os.path.join(folder_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)

            count += 1
            if count % 50 == 0:
                print(f"  [{count}/{total}] 생성 완료...")

    print(f"\n✅ 총 {count}개 페이지 생성 완료!")

    # sitemap 업데이트
    print("\nsitemap.xml 업데이트 중...")
    generate_sitemap(base_dir)
    print("✅ sitemap.xml 업데이트 완료!")


def generate_sitemap(base_dir):
    """sitemap.xml 생성"""
    today = datetime.now().strftime("%Y-%m-%d")

    urls = []
    # 메인 페이지
    urls.append(f"""  <url>
    <loc>https://drainkorea.com/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""")

    # area 페이지들
    for dirname in sorted(os.listdir(base_dir)):
        dirpath = os.path.join(base_dir, dirname)
        if os.path.isdir(dirpath) and os.path.exists(os.path.join(dirpath, "index.html")):
            urls.append(f"""  <url>
    <loc>https://drainkorea.com/area/{dirname}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    # guide, blog 등 기존 페이지
    for section in ["guide", "blog"]:
        section_path = os.path.join("docs", section)
        if os.path.exists(section_path):
            for dirname in sorted(os.listdir(section_path)):
                dirpath = os.path.join(section_path, dirname)
                if os.path.isdir(dirpath):
                    urls.append(f"""  <url>
    <loc>https://drainkorea.com/{section}/{dirname}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

    with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

    print(f"  sitemap에 {len(urls)}개 URL 등록")


if __name__ == "__main__":
    main()
