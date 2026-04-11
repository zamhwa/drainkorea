#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 45 city-specific SEO landing pages for drainkorea.com
15 cities × 3 keywords = 45 pages
"""

import os
import json
from pathlib import Path

# Configuration
DOCS_FOLDER = "/sessions/elegant-loving-heisenberg/jesus/docs"
AREA_FOLDER = os.path.join(DOCS_FOLDER, "area")

# City romanization mapping
CITIES = {
    "수원": {"roman": "suwan", "districts": ["영통구", "장안구", "권선구", "팔달구"]},
    "용인": {"roman": "yongin", "districts": ["수지구", "기흥구", "처인구"]},
    "성남": {"roman": "seongnam", "districts": ["분당구", "수정구", "중원구"]},
    "부천": {"roman": "bucheon", "districts": ["원미구", "소사구", "오정구"]},
    "인천": {"roman": "incheon", "districts": ["남동구", "부평구", "계양구", "서구", "연수구"]},
    "안양": {"roman": "anyang", "districts": ["만안구", "동안구"]},
    "안산": {"roman": "ansan", "districts": ["상록구", "단원구"]},
    "고양": {"roman": "goyang", "districts": ["일산동구", "일산서구", "덕양구"]},
    "파주": {"roman": "paju", "districts": ["운정", "금촌", "문산"]},
    "김포": {"roman": "gimpo", "districts": ["장기동", "풍무동", "구래동"]},
    "화성": {"roman": "hwaseong", "districts": ["동탄", "병점", "봉담"]},
    "의정부": {"roman": "uijeongbu", "districts": ["의정부동", "민락동", "가능동"]},
    "남양주": {"roman": "namyangju", "districts": ["다산", "별내", "호평"]},
    "하남": {"roman": "hanam", "districts": ["미사", "감일", "신장동"]},
    "광명": {"roman": "gwangmyeong", "districts": ["철산동", "하안동", "소하동"]},
}

# Keywords mapping
KEYWORDS = {
    "하수구막힘": {
        "roman": "hasugumaghim",
        "display": "하수구막힘",
        "problem": "하수구 막힘",
        "description": "하수구가 막혀 물이 제대로 빠지지 않는 문제",
        "causes": "음식물 찌꺼기, 기름때, 머리카락 등으로 인한 배관 폐색"
    },
    "변기막힘": {
        "roman": "byeongimaghim",
        "display": "변기막힘",
        "problem": "변기 막힘",
        "description": "화장실 변기가 막혀 물이 내려가지 않는 문제",
        "causes": "물티슈, 생리대, 과도한 화장지 등으로 인한 배관 폐색"
    },
    "싱크대막힘": {
        "roman": "singkeudaemaghim",
        "display": "싱크대 막힘",
        "problem": "주방 싱크대 막힘",
        "description": "주방 싱크대 배수구가 막혀 물이 빠지지 않는 문제",
        "causes": "음식물 찌꺼기, 기름때, 비누 찌꺼기 등으로 인한 배관 폐색"
    },
}

AI_IMAGES = [
    "https://www.genspark.ai/api/files/s/CXoQL4re?cache_control=3600",
    "https://www.genspark.ai/api/files/s/6mhUOyn7?cache_control=3600",
]

PHONE = "010-4406-1788"
COMPANY = "제우스시설관리"
DOMAIN = "https://drainkorea.com"


def create_local_business_schema(city_korean, city_roman, keyword_korean, keyword_roman):
    """Generate LocalBusiness schema"""
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": f"{city_korean} {keyword_korean} | {COMPANY}",
        "image": AI_IMAGES[0],
        "description": f"{city_korean}에서 {keyword_korean} 문제 해결. 24시간 긴급출동, 출장비 무료",
        "address": {
            "@type": "PostalAddress",
            "addressRegion": city_korean,
            "addressCountry": "KR"
        },
        "telephone": PHONE.replace("-", ""),
        "url": f"{DOMAIN}/area/{city_roman}-{keyword_roman}/",
        "priceRange": "₩80,000~₩200,000",
        "areaServed": city_korean,
        "serviceType": keyword_korean,
    }


def create_article_schema(city_korean, keyword_korean):
    """Generate Article schema"""
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{city_korean} {keyword_korean} 전문 해결 | 24시간 긴급출동",
        "description": f"{city_korean}의 {keyword_korean} 문제를 전문가가 빠르게 해결합니다",
        "author": {"@type": "Organization", "name": COMPANY},
        "publisher": {
            "@type": "Organization",
            "name": COMPANY,
            "url": DOMAIN,
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/logo.png"
            }
        },
        "datePublished": "2026-04-11",
        "dateModified": "2026-04-11",
        "mainEntityOfPage": f"{DOMAIN}/area/{city_korean}-{keyword_korean}/"
    }


def generate_html_content(city_korean, city_roman, keyword_korean, keyword_roman, keyword_info, city_info):
    """Generate complete HTML page content"""

    districts = ", ".join(city_info["districts"][:3]) + ("..." if len(city_info["districts"]) > 3 else "")

    local_business_schema = create_local_business_schema(city_korean, city_roman, keyword_korean, keyword_roman)
    article_schema = create_article_schema(city_korean, keyword_korean)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{city_korean}{keyword_korean} | 24시간 긴급출동 | {COMPANY}</title>
<meta name="description" content="{city_korean} {keyword_korean} 전문 해결. 24시간 응급 상황 대응, 출장비 무료, 미해결시 비용 0원. {PHONE} 긴급 출동.">
<meta name="keywords" content="{city_korean}{keyword_korean},{city_korean}변기막힘,{city_korean}하수구,싱크대막힘,배관막힘,화장실막힘">
<link rel="canonical" href="{DOMAIN}/area/{city_roman}-{keyword_roman}/">
<meta property="og:type" content="article">
<meta property="og:title" content="{city_korean}{keyword_korean} 전문 해결 | 24시간 긴급출동">
<meta property="og:description" content="{city_korean} {keyword_korean} 문제를 24시간 빠르게 해결합니다. 출장비 무료, 미해결시 비용 0원">
<meta property="og:url" content="{DOMAIN}/area/{city_roman}-{keyword_roman}/">
<meta property="og:image" content="{AI_IMAGES[0]}">
<meta property="og:locale" content="ko_KR">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<script type="application/ld+json">
{json.dumps(local_business_schema, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(article_schema, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "홈", "item": "{DOMAIN}/"}},
    {{"@type": "ListItem", "position": 2, "name": "지역별 서비스", "item": "{DOMAIN}/area/"}},
    {{"@type": "ListItem", "position": 3, "name": "{city_korean} {keyword_korean}"}}
  ]
}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Noto Sans KR',-apple-system,sans-serif;color:#1a1a1a;line-height:1.85;background:#fff;-webkit-font-smoothing:antialiased}}
a{{color:#2563eb;text-decoration:none}}
a:hover{{text-decoration:underline}}
img{{max-width:100%;display:block;border-radius:12px}}

.top-bar{{background:#dc2626;color:#fff;text-align:center;padding:10px 16px;font-size:13px;font-weight:700}}
.top-bar .blink{{animation:blink 1s step-end infinite}}
@keyframes blink{{50%{{opacity:0}}}}

.header{{background:#fff;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;box-shadow:0 2px 10px rgba(0,0,0,0.08);max-width:100%}}
.logo{{display:flex;align-items:center;gap:8px;text-decoration:none;color:inherit}}
.logo-icon{{width:32px;height:32px;background:#2563eb;border-radius:8px;display:flex;align-items:center;justify-content:center}}
.logo-text{{font-size:17px;font-weight:800;color:#1a1a1a}}
.logo-text em{{font-style:normal;color:#2563eb}}
.hdr-call{{display:flex;align-items:center;gap:5px;background:#dc2626;color:#fff;padding:9px 16px;border-radius:50px;font-weight:700;font-size:14px;text-decoration:none}}

.article-wrap{{max-width:800px;margin:0 auto;padding:32px 20px 80px}}
.breadcrumb{{font-size:13px;color:#64748b;margin-bottom:20px}}
.breadcrumb a{{color:#64748b}}
.breadcrumb a:hover{{color:#2563eb}}

h1{{font-size:32px;font-weight:900;line-height:1.3;margin-bottom:16px;color:#0f172a;letter-spacing:-1px}}
.article-meta{{font-size:13px;color:#64748b;margin-bottom:28px;padding-bottom:20px;border-bottom:1px solid #e2e8f0}}

.hero-image{{width:100%;height:auto;margin:24px 0;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.1)}}

h2{{font-size:24px;font-weight:800;color:#0f172a;margin:40px 0 16px;padding-top:16px;border-top:2px solid #f1f5f9}}
h3{{font-size:19px;font-weight:700;color:#1e293b;margin:28px 0 12px}}
p{{margin-bottom:16px;font-size:16px;color:#334155}}

.highlight-box{{background:#fef3c7;border-left:4px solid #f59e0b;padding:16px 20px;border-radius:0 10px 10px 0;margin:20px 0}}
.highlight-box p{{margin-bottom:0;color:#92400e;font-weight:500}}

.emergency-box{{background:#fef2f2;border-left:4px solid #dc2626;padding:16px 20px;border-radius:0 10px 10px 0;margin:20px 0}}
.emergency-box p{{margin-bottom:0;color:#991b1b}}

.tip-box{{background:#f0fdf4;border-left:4px solid #16a34a;padding:16px 20px;border-radius:0 10px 10px 0;margin:20px 0}}
.tip-box p{{margin-bottom:0;color:#166534}}

.equipment-list{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin:20px 0}}
.equipment-item{{background:#f1f5f9;padding:16px;border-radius:10px;border:1px solid #e2e8f0}}
.equipment-item h4{{margin:0 0 8px;color:#1e293b;font-size:15px}}
.equipment-item p{{margin:0;font-size:14px;color:#475569}}

.cta-banner{{background:linear-gradient(135deg,#1e3a5f,#0f172a);color:#fff;padding:32px 24px;border-radius:16px;text-align:center;margin:40px 0}}
.cta-banner h2{{color:#fff;border:none;margin:0 0 8px;padding:0;font-size:22px}}
.cta-banner p{{color:#cbd5e1;margin-bottom:16px;font-size:15px}}
.cta-phone{{display:inline-flex;align-items:center;gap:8px;background:#dc2626;color:#fff;padding:16px 32px;border-radius:60px;font-size:24px;font-weight:900;text-decoration:none;box-shadow:0 4px 20px rgba(220,38,38,.4);transition:transform .2s}}
.cta-phone:hover{{transform:scale(1.03);text-decoration:none;color:#fff}}
.cta-sub{{font-size:12px;color:#64748b;margin-top:10px}}

.related-links{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:20px 0}}
.related-link{{display:block;padding:14px 16px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;font-size:14px;font-weight:600;color:#1e293b;text-decoration:none;transition:all .2s}}
.related-link:hover{{background:#eff6ff;border-color:#93c5fd;text-decoration:none}}
.related-link .arrow{{float:right;color:#94a3b8}}

.bottom-bar{{position:fixed;bottom:0;left:0;right:0;z-index:999;display:flex;box-shadow:0 -4px 20px rgba(0,0,0,.15)}}
.bottom-bar a{{flex:1;display:flex;align-items:center;justify-content:center;gap:6px;padding:14px;font-weight:800;font-size:15px;text-align:center;text-decoration:none}}
.bb-call{{background:#dc2626;color:#fff;flex:1.5!important}}
.bb-home{{background:#2563eb;color:#fff}}

ul.feature-list{{margin:16px 0 16px 24px;color:#334155}}
ul.feature-list li{{margin-bottom:8px;line-height:1.6}}

@media(min-width:768px){{
  h1{{font-size:40px}}
  .bottom-bar{{display:none}}
}}
@media(max-width:374px){{
  h1{{font-size:26px}}
  .cta-phone{{font-size:20px;padding:14px 24px}}
}}
</style>
</head>
<body>

<div class="top-bar">
  <span class="blink">&#x26A0;</span> {city_korean} {keyword_korean} 긴급 상황 <strong>{PHONE}</strong> 24시간 상담
</div>

<header class="header">
  <a href="/" class="logo">
    <div class="logo-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-4H7l5-8v4h4l-5 8z"/></svg>
    </div>
    <div class="logo-text">제우스<em>시설관리</em></div>
  </a>
  <a href="tel:01044061788" class="hdr-call">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="#fff"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24 11.36 11.36 0 003.58.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.58a1 1 0 01-.24 1.01l-2.2 2.2z"/></svg>
    전화하기
  </a>
</header>

<article class="article-wrap">
  <nav class="breadcrumb">
    <a href="/">홈</a> &rsaquo; <a href="/area/">지역별 서비스</a> &rsaquo; {city_korean} {keyword_korean}
  </nav>

  <h1>{city_korean} {keyword_korean} 전문 해결<br><small style="font-size:18px;font-weight:600;color:#64748b">24시간 응급 상황 대응 · 출장비 무료 · 미해결시 비용 0원</small></h1>

  <div class="article-meta">
    2026년 4월 11일 업데이트 · {COMPANY} 기술팀
  </div>

  <img src="{AI_IMAGES[0]}" alt="{city_korean} {keyword_korean} 응급 서비스" class="hero-image">

  <p><strong>{city_korean}에서 {keyword_korean} 문제가 발생하셨나요?</strong> {keyword_info['description']}. 저희 {COMPANY}는 24시간 365일 응급 서비스를 제공하며, 현장에서 정확한 진단 후 최적의 해결책을 제시합니다. 출장비는 무료이며, 문제를 해결하지 못하면 비용을 받지 않습니다.</p>

  <div class="emergency-box">
    <p><strong>{city_korean} {keyword_korean} 긴급 상황이신가요?</strong> 지금 바로 전화하세요. 최단 시간 내에 전문 기사가 출동하여 문제를 해결해 드립니다. <a href="tel:01044061788" style="color:#dc2626;font-weight:800">{PHONE}</a></p>
  </div>

  <h2>서비스 지역: {city_korean} 전역</h2>
  <p>{city_korean}의 {", ".join(city_info['districts'])} 등 모든 지역에서 빠른 응급 서비스를 제공합니다. 어느 지역이든 최단 시간에 현장에 도착하여 전문적으로 문제를 해결합니다.</p>

  <h2>{keyword_korean}의 주요 원인</h2>
  <p>{keyword_info['description']} {keyword_info['causes']}는 방치하면 악취, 역류, 배관 손상 등으로 이어질 수 있습니다. 초기 증상이 보이면 빠르게 대처하는 것이 중요합니다.</p>

  <h3>{city_korean}에서 {keyword_korean} 문제의 특징</h3>
  <ul class="feature-list">
    <li><strong>물이 천천히 빠지거나 아예 안 빠짐</strong> — 배관 폐색의 가장 흔한 초기 증상</li>
    <li><strong>악취(하수 냄새)가 올라옴</strong> — 배관 내 오염물 축적 신호</li>
    <li><strong>배수구에서 꿀꿀거리는 소리</strong> — 배관 내부 공기 갇힘 신호</li>
    <li><strong>다른 배수구로 물이 역류</strong> — 메인 배관 막힘 가능성</li>
    <li><strong>변기 물이 제대로 내려가지 않음</strong> — 변기 자체 또는 하수관 폐색</li>
  </ul>

  <h2>전문 장비로 빠르게 해결</h2>
  <div class="equipment-list">
    <div class="equipment-item">
      <h4>배관 내시경 (CCTV)</h4>
      <p>배관 내부를 직접 촬영하여 정확한 원인을 진단하고 최적의 해결 방법을 결정합니다.</p>
    </div>
    <div class="equipment-item">
      <h4>드레인 기계</h4>
      <p>배관 내의 이물질과 축적물을 안전하게 제거하는 전문 장비입니다.</p>
    </div>
    <div class="equipment-item">
      <h4>고압 세척기</h4>
      <p>강력한 수압으로 배관 내벽의 모든 오염물을 제거하고 배관을 완전히 복원합니다.</p>
    </div>
    <div class="equipment-item">
      <h4>관로 탐지기</h4>
      <p>배관의 위치, 깊이, 방향을 정확하게 탐지하여 효율적인 작업을 진행합니다.</p>
    </div>
  </div>

  <img src="{AI_IMAGES[1]}" alt="{city_korean} 배관 작업 장비" class="hero-image">

  <h2>{city_korean} {keyword_korean} 해결 비용 (2026년 기준)</h2>
  <p>{city_korean}에서 {keyword_korean} 문제를 전문가가 해결할 때의 평균 비용입니다. 정확한 견적은 현장 진단 후 제시합니다.</p>

  <ul class="feature-list">
    <li><strong>배관 내시경 진단:</strong> 8~10만원 (30분)</li>
    <li><strong>드레인 기계 작업:</strong> 10~15만원 (30~60분)</li>
    <li><strong>고압 세척:</strong> 12~18만원 (1~2시간)</li>
    <li><strong>배관 부분 교체:</strong> 20~50만원+ (2~4시간)</li>
  </ul>

  <div class="tip-box">
    <p><strong>비용 절약 팁:</strong> 출장비 0원, 현장 견적 후 시공, 미해결시 비용 0원 정책입니다. 초기 진단 후 예상 비용을 명확하게 안내드립니다.</p>
  </div>

  <h2>{city_korean}에서 믿을 수 있는 업체 선택 기준</h2>
  <ul class="feature-list">
    <li><strong>출장비 무료:</strong> 방문 비용을 따로 청구하지 않는 곳</li>
    <li><strong>현장 견적:</strong> 전화로 확정 금액을 말하지 않고 직접 방문하여 진단 후 견적</li>
    <li><strong>미해결시 환불:</strong> 문제를 해결하지 못하면 비용을 받지 않는 정책</li>
    <li><strong>24시간 운영:</strong> 새벽이나 야간 응급 상황에도 대응</li>
    <li><strong>전문 장비:</strong> 배관 내시경, 고압 세척기 등 최신 장비 보유</li>
    <li><strong>실제 후기:</strong> 지역 사용자들의 실제 이용 후기 확인</li>
  </ul>

  <h2>{city_korean} {keyword_korean} 예방 방법</h2>
  <p>문제가 발생한 후 해결하는 것보다 예방하는 것이 중요합니다. 다음의 방법들을 실천하면 {keyword_korean} 문제를 크게 줄일 수 있습니다.</p>

  <ul class="feature-list">
    <li><strong>정기적 배관 청소:</strong> 3~6개월마다 고압 세척으로 배관 내부 청소</li>
    <li><strong>적절한 습관:</strong> 음식물 찌꺼기와 기름을 직접 버리지 않기</li>
    <li><strong>배수구 보호:</strong> 배수구 망을 설치하여 이물질 차단</li>
    <li><strong>초기 증상 대처:</strong> 물 빠짐이 느려지면 즉시 전문가 상담</li>
  </ul>

  <div class="cta-banner">
    <h2>{city_korean} {keyword_korean} 전문 해결</h2>
    <p>24시간 긴급 응대, 정확한 진단, 빠른 해결</p>
    <a href="tel:01044061788" class="cta-phone">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="#fff"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24 11.36 11.36 0 003.58.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.58a1 1 0 01-.24 1.01l-2.2 2.2z"/></svg>
      {PHONE}
    </a>
    <p class="cta-sub">24시간 상담 가능 · 출장비 0원 · 미해결시 0원</p>
  </div>

  <h2>자주 묻는 질문</h2>

  <h3>{city_korean}에서 {keyword_korean} 발생 시 가장 먼저 할 일은?</h3>
  <p>물의 흐름을 멈추고 바닥에 오수가 넘칠 위험을 제거합니다. 그 다음 배수구 주변을 정리하고 {PHONE}으로 전문가에게 연락하세요. 전문 기사가 신속하게 도착하여 원인을 진단하고 해결합니다.</p>

  <h3>응급 상황이 아니어도 전화해도 되나요?</h3>
  <p>물론입니다. 물이 조금 느리게 빠지거나 냄새가 나는 초기 증상 단계에 전화하시면, 더 빠르고 저렴하게 해결할 수 있습니다. 응급 상황으로 악화되기 전에 상담을 받으세요.</p>

  <h3>{city_korean}의 어느 지역이든 서비스를 받을 수 있나요?</h3>
  <p>{city_korean}의 모든 지역({", ".join(city_info['districts'])} 등)에서 서비스를 제공합니다. 지역에 관계없이 최단 시간 내에 전문 기사가 출동합니다.</p>

  <h3>야간이나 새벽에도 가능한가요?</h3>
  <p>24시간 365일 운영하므로 야간과 새벽, 휴일에도 응급 출동이 가능합니다. {PHONE}으로 언제든 전화하세요.</p>

  <h3>견적은 무료인가요?</h3>
  <p>네, 현장 방문과 초기 진단은 무료입니다. 진단 후 예상 비용을 명확하게 안내하고, 비용에 동의하신 경우에만 작업을 진행합니다.</p>

  <h2>{city_korean} 지역 {keyword_korean} 서비스</h2>
  <p>저희 {COMPANY}는 {city_korean}의 {", ".join(city_info['districts'])} 등 모든 지역에서 전문적인 {keyword_korean} 해결 서비스를 제공합니다. 수십 년의 경험과 최신 장비로 신속하고 정확하게 문제를 해결하며, 고객 만족을 최우선으로 합니다.</p>

  <div class="related-links">
    <a href="/" class="related-link">홈으로 돌아가기 <span class="arrow">→</span></a>
    <a href="/guide/hasugumaghim/" class="related-link">하수구막힘 가이드 <span class="arrow">→</span></a>
  </div>

</article>

<div class="bottom-bar">
  <a href="/" class="bb-home">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
    홈
  </a>
  <a href="tel:01044061788" class="bb-call">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24 11.36 11.36 0 003.58.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.58a1 1 0 01-.24 1.01l-2.2 2.2z"/></svg>
    {PHONE}
  </a>
</div>

</body>
</html>
"""
    return html


def main():
    """Generate all city-specific SEO pages"""

    # Create area folder if it doesn't exist
    os.makedirs(AREA_FOLDER, exist_ok=True)

    pages_created = 0

    # Iterate through all cities and keywords
    for city_korean, city_info in CITIES.items():
        city_roman = city_info["roman"]

        for keyword_korean, keyword_info in KEYWORDS.items():
            keyword_roman = keyword_info["roman"]

            # Create city-keyword folder
            folder_name = f"{city_roman}-{keyword_roman}"
            folder_path = os.path.join(AREA_FOLDER, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # Generate HTML content
            html_content = generate_html_content(
                city_korean, city_roman,
                keyword_korean, keyword_roman,
                keyword_info, city_info
            )

            # Write index.html
            index_path = os.path.join(folder_path, "index.html")
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            pages_created += 1
            print(f"✓ Created: /area/{folder_name}/index.html")

    print(f"\n✅ Total pages created: {pages_created}")
    print(f"📁 Folder: {AREA_FOLDER}")


if __name__ == "__main__":
    main()
