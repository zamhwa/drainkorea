#!/usr/bin/env python3
"""
SEO 강화 스크립트
1. 각 페이지에 고유 FAQ 섹션 + FAQPage Schema.org 추가
2. 관련 페이지 내부 링크 추가 (같은 도시 다른 서비스, 같은 서비스 인근 도시)
3. 서비스별 고유 콘텐츠 단락 추가
4. Breadcrumb 네비게이션 추가
"""
import os
import re
import hashlib
import random

AREA_DIR = "docs/area"

# ===== 매핑 데이터 =====

# 서비스 영문→한글
SERVICE_KR = {
    "hasugumaghim": "하수구막힘",
    "singkeudaemaghim": "싱크대막힘",
    "byeongimaghim": "변기막힘",
    "hwajangsirmaghim": "화장실막힘",
    "baesugumaghim": "배수구막힘",
    "yokjomaghim": "욕조막힘",
    "osugwanmaghim": "오수관막힘",
    "usugwanmaghim": "우수관막힘",
    "hasuguttulgi": "하수구뚫기",
    "hasugunaemse": "하수구냄새",
    "hasugwanseceog": "하수관세척",
    "baegwancheongso": "배관청소",
    "baegwangyoche": "배관교체",
    "baegwannusu": "배관누수",
    "baegwanyeogru": "배관역류",
    "geuriseuteulaebcheongso": "그리스트랩청소",
    "jeonghwajocheongso": "정화조청소",
    "maenholcheongso": "맨홀청소",
    "hasudogongsa": "하수도공사",
    "semyeondaemaghim": "세면대막힘",
}

# 20개 서비스 종류
SERVICES_EN = list(SERVICE_KR.keys())

# 서비스별 FAQ (각 서비스당 3~4개 고유 질문)
SERVICE_FAQ = {
    "hasugumaghim": [
        ("하수구가 막히면 직접 뚫어도 되나요?", "가정용 도구로 일시적 해소는 가능하지만, 근본 원인(배관 내 이물질 축적, 관 파손 등)을 해결하지 못하면 반복됩니다. 전문 장비(드레인 기계, 내시경 카메라)를 사용해야 정확한 진단과 완전한 해결이 가능합니다."),
        ("하수구막힘 비용은 얼마인가요?", "막힘 정도와 위치에 따라 다르지만, 기본 출장비 무료이며 작업 전 현장 견적을 정확히 안내합니다. 미해결 시 비용 0원 정책을 운영하고 있어 안심하실 수 있습니다."),
        ("야간에도 하수구막힘 출동 가능한가요?", "네, 제우스시설관리는 24시간 365일 운영합니다. 야간, 주말, 공휴일에도 추가 요금 없이 동일한 서비스를 제공하며, 28분 내 현장 도착을 목표로 합니다."),
        ("하수구막힘을 예방하는 방법이 있나요?", "음식물 찌꺼기 거름망 사용, 기름류 직접 배수 금지, 머리카락 트랩 설치, 정기적인 배관 세척(6개월~1년 주기)이 효과적입니다. 특히 오래된 건물은 연 1회 전문 점검을 권장합니다."),
    ],
    "singkeudaemaghim": [
        ("싱크대 물이 천천히 빠지는 것도 막힘인가요?", "네, 배수 속도가 느려진 것은 배관 내부에 기름때와 음식물 찌꺼기가 축적되고 있다는 초기 신호입니다. 방치하면 완전히 막힐 수 있으므로 조기에 전문가 점검을 받는 것이 좋습니다."),
        ("싱크대막힘은 왜 자주 발생하나요?", "식용유, 기름기가 배관 내벽에 응고되어 점차 쌓이고, 여기에 음식물 찌꺼기가 걸려 막힘이 발생합니다. 특히 겨울철에는 찬물로 기름이 더 빨리 응고되어 빈도가 높아집니다."),
        ("싱크대막힘 해결에 걸리는 시간은?", "일반적인 기름때 막힘은 30분~1시간 내 해결됩니다. 배관 깊숙한 곳의 심한 막힘이나 배관 노후로 인한 경우 추가 시간이 필요할 수 있으며, 현장에서 정확한 소요 시간을 안내합니다."),
    ],
    "byeongimaghim": [
        ("변기에 이물질이 빠졌는데 어떻게 해야 하나요?", "손이 닿지 않는 곳으로 이물질이 넘어갔다면 무리하게 밀어넣지 마세요. 전문 장비(관로 내시경)로 위치를 확인한 후 안전하게 제거합니다. 무리한 시도는 배관 파손을 유발할 수 있습니다."),
        ("변기 물이 역류하는데 왜 그런가요?", "변기 역류는 변기 자체의 막힘 또는 하수 본관의 문제일 수 있습니다. 특히 1층이나 지하에서 자주 발생하며, 정확한 원인 파악을 위해 내시경 카메라 진단이 필요합니다."),
        ("변기막힘 작업 시 화장실 사용이 불가한가요?", "작업 중에는 해당 변기 사용이 제한되지만, 대부분 1시간 이내 해결됩니다. 다른 화장실이 있다면 병행 사용 가능하며, 작업 완료 후 즉시 정상 사용할 수 있습니다."),
    ],
    "hwajangsirmaghim": [
        ("화장실 배수구에서 냄새가 나는데 막힘과 관련 있나요?", "네, 배수 트랩의 봉수(물 차단막)가 마르거나, 배관 내 이물질이 부패하면서 악취가 발생합니다. 이는 부분적 막힘의 전조 증상일 수 있으므로 점검을 권장합니다."),
        ("화장실 바닥 배수구가 막혔는데 직접 해결 가능한가요?", "표면의 머리카락이나 비누 찌꺼기 제거는 가능하지만, 배관 내부 깊숙한 곳의 막힘은 전문 장비가 필요합니다. 무리한 와이어 사용은 배관을 손상시킬 수 있습니다."),
        ("오래된 아파트인데 화장실이 자주 막혀요", "20년 이상 된 건물은 배관 노후로 내부 스케일(석회 침전물)이 쌓여 관 지름이 좁아집니다. 고압세척으로 내부를 청소하거나, 상태에 따라 배관 교체를 검토해야 합니다."),
    ],
    "baesugumaghim": [
        ("배수구에서 꾸르륵 소리가 나는데 막힘 신호인가요?", "네, 배관 내부가 부분적으로 막혀 공기가 지나가면서 소리가 발생합니다. 이 단계에서 조치하면 비용과 시간을 크게 절약할 수 있습니다."),
        ("배수구막힘과 하수구막힘은 다른 건가요?", "배수구는 세면대, 싱크대, 욕조 등의 개별 배수 지점을 말하고, 하수구는 이들이 합쳐지는 본관을 의미합니다. 증상은 유사하지만 작업 방법과 범위가 다를 수 있습니다."),
        ("배수구 거름망을 사용해도 막히는 이유는?", "거름망은 큰 이물질만 걸러내며, 기름기, 비누 찌꺼기, 미세 음식물은 통과하여 배관 내벽에 축적됩니다. 정기적인 배관 세척이 근본적인 예방법입니다."),
    ],
    "yokjomaghim": [
        ("욕조 배수가 느려진 것이 막힘의 시작인가요?", "맞습니다. 욕조 배수구는 머리카락과 비누 찌꺼기가 주원인입니다. 배수 속도가 눈에 띄게 느려졌다면 이미 상당량이 축적된 상태이므로 전문 청소를 권장합니다."),
        ("욕조 배수구에 머리카락이 걸렸는데 제거가 안 돼요", "표면의 머리카락은 집게로 제거할 수 있지만, 배관 내부 깊숙이 뭉친 머리카락은 드레인 기계의 스프링 와이어로 감아 빼내야 합니다. 화학 세정제는 배관 부식을 유발할 수 있어 주의가 필요합니다."),
        ("욕조 교체 없이 막힘 해결이 가능한가요?", "대부분의 욕조막힘은 배관 문제이므로 욕조 교체 없이 해결 가능합니다. 드레인 기계와 고압세척기로 배관만 처리하면 됩니다. 단, 욕조 자체 배수구 부품이 파손된 경우 부분 교체가 필요할 수 있습니다."),
    ],
    "osugwanmaghim": [
        ("오수관과 우수관의 차이가 뭔가요?", "오수관은 생활하수(주방, 화장실, 세탁 등)를 배출하는 관로이고, 우수관은 빗물을 배출하는 관로입니다. 오수관은 이물질 축적이 많아 막힘이 더 자주 발생합니다."),
        ("오수관이 막히면 어떤 증상이 나타나나요?", "여러 곳의 배수가 동시에 느려지거나, 1층 변기에서 역류가 발생하며, 하수구 악취가 심해집니다. 이는 개별 배수구가 아닌 공용 오수관의 문제를 의미합니다."),
        ("오수관막힘은 건물 전체에 영향을 주나요?", "네, 오수관은 건물의 각 세대 배수가 합쳐지는 본관이므로, 막히면 저층부터 역류 등의 피해가 발생합니다. 빠른 조치가 필요하며, 관로 내시경으로 정확한 위치를 파악한 후 고압세척으로 해결합니다."),
    ],
    "usugwanmaghim": [
        ("비가 올 때 배수가 안 되면 우수관 문제인가요?", "네, 우수관에 낙엽, 흙, 모래 등이 축적되어 막힌 경우가 많습니다. 특히 가을철 낙엽이 많은 시기와 봄철 황사 이후 우수관 점검을 권장합니다."),
        ("우수관 막힘을 방치하면 어떻게 되나요?", "폭우 시 건물 주변에 물이 고여 지하실 침수, 건물 기초 침하, 토양 침식 등 심각한 피해가 발생할 수 있습니다. 정기적인 점검과 청소가 중요합니다."),
        ("우수관 청소 주기는 어떻게 되나요?", "일반적으로 연 1~2회, 특히 장마철 전과 낙엽이 진 후 점검하는 것을 권장합니다. 주변에 나무가 많은 건물은 더 자주 점검이 필요합니다."),
    ],
    "hasuguttulgi": [
        ("하수구뚫기와 하수구막힘 해결은 같은 서비스인가요?", "기본적으로 같은 서비스입니다. '하수구뚫기'는 막힌 하수구를 뚫어 정상 배수를 회복하는 작업을 말하며, 드레인 기계, 고압세척기 등 전문 장비를 사용합니다."),
        ("하수구를 뚫어도 또 막히는 이유는?", "일시적으로 뚫기만 하고 배관 내벽의 오염물을 완전히 제거하지 않으면 재발합니다. 제우스시설관리는 내시경으로 원인을 확인한 후 고압세척까지 병행하여 재발률을 최소화합니다."),
        ("하수구뚫기 작업 중 배관이 손상될 수 있나요?", "전문 장비와 숙련된 기술자가 작업하면 배관 손상 위험은 매우 낮습니다. 작업 전 내시경으로 배관 상태를 확인하고, 배관 재질과 상태에 맞는 적절한 장비와 압력을 사용합니다."),
    ],
    "hasugunaemse": [
        ("하수구 냄새가 나는데 막힘이 아닐 수도 있나요?", "네, 악취의 원인은 다양합니다. 배수 트랩의 봉수 증발, 배관 연결부 틈새, 통기관 문제, 하수관 파손 등이 원인일 수 있습니다. 정확한 원인 파악을 위해 전문 진단이 필요합니다."),
        ("하수구 냄새를 임시로 막는 방법이 있나요?", "사용하지 않는 배수구에 물을 부어 트랩의 봉수를 유지하세요. 배수구 덮개를 밀봉하거나, 식초+베이킹소다로 배관 내부를 세척하는 것도 임시 방법입니다. 근본 해결은 전문 점검이 필요합니다."),
        ("하수구 냄새가 건강에 해로운가요?", "하수 가스에는 황화수소, 메탄 등 유해 가스가 포함되어 있어 두통, 메스꺼움, 호흡기 문제를 유발할 수 있습니다. 특히 밀폐된 공간에서는 위험할 수 있으므로 빠른 조치가 중요합니다."),
    ],
    "hasugwanseceog": [
        ("하수관세척은 얼마나 자주 해야 하나요?", "일반 가정은 2~3년에 1회, 음식점이나 상업시설은 6개월~1년에 1회 세척을 권장합니다. 배수 속도가 느려지거나 악취가 발생하면 즉시 세척이 필요합니다."),
        ("하수관세척과 하수구뚫기는 다른 건가요?", "하수구뚫기는 막힌 부분을 관통시키는 응급 처치이고, 하수관세척은 배관 내벽의 오염물을 고압수로 완전히 제거하는 예방적 관리입니다. 세척이 더 포괄적인 작업입니다."),
        ("고압세척 시 배관에 무리가 가지 않나요?", "전문가가 배관 재질과 상태에 맞는 적절한 수압(100~200bar)을 조절하므로 안전합니다. 오히려 정기적 세척은 배관 수명을 연장시킵니다. 단, 심하게 노후된 배관은 사전 내시경 점검 후 진행합니다."),
    ],
    "baegwancheongso": [
        ("배관청소와 하수관세척은 같은 건가요?", "유사하지만 범위가 다릅니다. 배관청소는 급수관, 배수관, 난방관 등 건물 내 모든 배관을 대상으로 하며, 하수관세척은 하수 배출관에 한정됩니다. 필요에 따라 적합한 서비스를 안내합니다."),
        ("오래된 건물인데 배관청소만으로 해결될까요?", "30년 이상 된 배관은 내부 스케일과 녹이 심할 수 있습니다. 내시경 진단 후 청소로 충분한지, 부분 교체가 필요한지 정확히 판단합니다. 청소만으로도 배수 성능이 크게 개선되는 경우가 많습니다."),
        ("배관청소 후 바로 사용 가능한가요?", "네, 고압세척 방식은 화학 약품을 사용하지 않으므로 작업 완료 즉시 안전하게 사용할 수 있습니다. 작업 후 내시경으로 청소 상태를 확인하여 결과를 보여드립니다."),
    ],
    "baegwangyoche": [
        ("배관교체는 언제 해야 하나요?", "배관 수명은 재질에 따라 다르지만, 일반적으로 아연도금관 15~20년, PVC관 30~40년입니다. 누수가 빈번하거나, 녹물이 나오거나, 막힘이 반복되면 교체를 검토해야 합니다."),
        ("배관교체 시 벽이나 바닥을 뜯어야 하나요?", "매립 배관의 경우 부분적인 철거가 필요할 수 있지만, 관로탐지기로 정확한 위치를 파악하여 최소한의 범위만 작업합니다. 노출 배관은 철거 없이 교체 가능합니다."),
        ("배관교체 비용은 어떻게 산정되나요?", "배관 길이, 재질(PVC, PE, 스테인레스 등), 매립 여부, 층수 등에 따라 달라집니다. 현장 실측 후 정확한 견적을 무료로 제공하며, 작업 후 추가 비용은 발생하지 않습니다."),
    ],
    "baegwannusu": [
        ("배관 누수를 방치하면 어떻게 되나요?", "수도요금 급증, 벽/바닥 곰팡이 발생, 건물 구조체 손상, 층간 누수 분쟁 등 심각한 문제로 확대됩니다. 초기에 발견하여 수리하는 것이 비용과 피해를 최소화하는 방법입니다."),
        ("눈에 보이지 않는 누수도 찾을 수 있나요?", "관로탐지기와 음향탐지 장비로 매립 배관의 누수 위치를 정밀하게 탐지합니다. 벽이나 바닥을 뜯지 않고도 누수 지점을 찾을 수 있어 불필요한 공사를 방지합니다."),
        ("누수 수리 후 재발 가능성은?", "원인을 정확히 파악하고 적절한 방법으로 수리하면 재발률은 매우 낮습니다. 배관 노후가 원인인 경우 해당 구간 교체를 권장하며, 수리 후 누수 보증을 제공합니다."),
    ],
    "baegwanyeogru": [
        ("배관 역류가 발생하는 원인은 뭔가요?", "하수 본관 막힘, 역류 방지 밸브 고장, 폭우로 인한 하수관 과부하, 배관 구배(기울기) 불량 등이 주요 원인입니다. 정확한 원인 파악을 위해 내시경 진단이 필요합니다."),
        ("1층에서만 역류가 발생하는데 왜 그런가요?", "하수 본관이 막히면 수압이 가장 낮은 1층이나 지하로 역류가 발생합니다. 이는 건물 전체의 하수관 문제이므로 본관 점검과 세척이 필요합니다."),
        ("역류 방지 밸브 설치로 예방할 수 있나요?", "네, 역류 방지 밸브(체크밸브)를 설치하면 하수 역류를 효과적으로 차단할 수 있습니다. 특히 1층, 지하 화장실, 반지하 주택에 설치를 강력 권장합니다."),
    ],
    "geuriseuteulaebcheongso": [
        ("그리스트랩 청소 주기는 어떻게 되나요?", "업종과 규모에 따라 다르지만, 일반 음식점은 주 1~2회 간이 청소, 월 1회 전문 청소를 권장합니다. 튀김류를 많이 다루는 곳은 더 자주 청소가 필요합니다."),
        ("그리스트랩을 청소하지 않으면 어떻게 되나요?", "배수관 막힘, 하수구 역류, 심한 악취, 해충 발생의 원인이 됩니다. 또한 환경부 규정에 따라 관리 의무가 있어 미이행 시 과태료가 부과될 수 있습니다."),
        ("그리스트랩 전문 청소와 직접 청소의 차이는?", "직접 청소는 표면의 기름을 걷어내는 수준이지만, 전문 청소는 그리스트랩 내부는 물론 연결 배관까지 고압세척으로 완전히 세척합니다. 배수 성능과 위생 상태가 확연히 달라집니다."),
    ],
    "jeonghwajocheongso": [
        ("정화조 청소는 법적 의무인가요?", "네, 하수도법에 따라 정화조는 연 1회 이상 청소가 의무입니다. 미이행 시 과태료가 부과되며, 방류수 수질 기준 초과 시 추가 제재를 받을 수 있습니다."),
        ("정화조에서 냄새가 심한데 정상인가요?", "정상 작동하는 정화조에서도 약간의 냄새가 날 수 있지만, 심한 악취는 청소 시기 경과, 미생물 사멸, 통기관 막힘 등의 문제를 의미합니다. 점검이 필요합니다."),
        ("정화조 청소와 준설은 다른 건가요?", "청소는 정화조 내부의 슬러지(침전물)를 수거하는 정기 관리이고, 준설은 오랜 기간 방치되어 고형화된 슬러지를 제거하는 집중 작업입니다. 정기 청소를 하면 준설이 불필요합니다."),
    ],
    "maenholcheongso": [
        ("맨홀 청소는 왜 필요한가요?", "맨홀은 하수관로의 점검구로, 내부에 토사, 쓰레기, 기름 등이 축적됩니다. 방치하면 하수 흐름을 방해하여 주변 건물에 역류나 침수 피해를 줄 수 있습니다."),
        ("맨홀 청소 주기는 어떻게 되나요?", "상업 밀집 지역은 분기 1회, 주거 지역은 반기~연 1회 청소를 권장합니다. 주변에 음식점이 많거나 공사가 잦은 지역은 더 자주 점검이 필요합니다."),
        ("맨홀에서 악취가 나는데 해결 방법은?", "맨홀 내부 세척과 함께 연결 배관 점검이 필요합니다. 악취는 하수관 내 이물질 부패, 통기 불량, 맨홀 뚜껑 밀봉 불량 등이 원인일 수 있습니다."),
    ],
    "hasudogongsa": [
        ("하수도공사가 필요한 경우는 언제인가요?", "배관 노후로 반복적 누수/막힘 발생, 건물 증축이나 용도 변경, 신축 건물의 하수 연결, 하수관 파손이나 침하 등의 경우에 하수도공사가 필요합니다."),
        ("하수도공사 시 도로 굴착이 필요한가요?", "건물 외부 하수관 작업 시 부분적 굴착이 필요할 수 있습니다. 관로탐지기로 정확한 위치를 파악하여 최소 범위만 작업하며, 비굴착 공법(관 갱생)이 가능한 경우 도로 훼손 없이 진행합니다."),
        ("하수도공사 인허가는 어떻게 하나요?", "공공 하수관 연결 공사는 지자체 허가가 필요합니다. 제우스시설관리는 인허가 서류 작성부터 시공, 준공 검사까지 원스톱으로 지원합니다."),
    ],
    "semyeondaemaghim": [
        ("세면대 배수가 느려졌는데 막힘 초기 증상인가요?", "네, 세면대는 치약, 비누, 머리카락, 피부 각질 등이 혼합되어 서서히 막힙니다. 배수 속도가 눈에 띄게 느려졌다면 조기에 전문 청소를 받으시는 것이 좋습니다."),
        ("세면대 팝업(배수구 마개) 아래가 막힌 것 같아요", "팝업 아래쪽에 머리카락과 이물질이 걸려 막히는 경우가 매우 흔합니다. 팝업을 분리하여 청소하면 해결되는 경우도 있지만, 배관 내부까지 막혔다면 전문 장비가 필요합니다."),
        ("세면대 교체 없이 막힘 해결이 가능한가요?", "대부분의 세면대막힘은 배관 문제이므로 세면대 교체 없이 해결 가능합니다. 드레인 기계와 고압세척기로 배관을 청소하면 원래 배수 성능을 회복합니다."),
    ],
}

# 서비스별 고유 추가 콘텐츠
SERVICE_EXTRA_CONTENT = {
    "hasugumaghim": [
        "하수구막힘은 가장 흔한 배관 문제 중 하나로, 음식물 찌꺼기, 기름때, 머리카락, 이물질 등이 복합적으로 작용하여 발생합니다. 특히 오래된 건물에서는 배관 내부의 스케일(석회 침전물)이 관 지름을 좁혀 막힘이 더 자주 발생합니다.",
        "제우스시설관리의 하수구막힘 해결 프로세스는 ①내시경 진단→②원인 파악→③드레인 기계 투입→④고압세척→⑤최종 점검의 5단계로 진행됩니다. 이 체계적인 접근 방식으로 재발률을 최소화합니다.",
    ],
    "singkeudaemaghim": [
        "싱크대 배수관은 U자형 트랩 구조로 되어 있어 기름기와 음식물이 특히 잘 쌓입니다. 뜨거운 물로 기름을 녹이는 것은 일시적일 뿐, 하류에서 다시 응고되어 문제가 반복됩니다.",
        "주방 싱크대의 경우 배수관 굵기가 보통 50mm로, 욕실 배수관(75~100mm)보다 좁아 막힘에 더 취약합니다. 음식물 분쇄기(디스포저) 사용 가구에서는 분쇄된 미세 입자가 배관에 축적되는 경우도 많습니다.",
    ],
    "byeongimaghim": [
        "변기막힘의 주요 원인은 과도한 화장지 사용, 물티슈나 생리대 같은 비분해성 이물질 투입, 그리고 배관 노후입니다. 특히 물티슈는 '수세식 가능'이라는 표시가 있더라도 실제로는 분해되지 않아 막힘의 주범입니다.",
        "양변기의 트랩 구조는 S자 또는 P자 형태로, 이 곡선 부분에서 이물질이 걸려 막힙니다. 전문 장비 없이 무리하게 뚫으려 하면 도기(변기 본체)가 파손되거나 배관이 손상될 수 있으므로 전문가 도움을 받는 것이 안전합니다.",
    ],
}

# 기본 추가 콘텐츠 (위에 없는 서비스용)
DEFAULT_EXTRA = [
    "제우스시설관리는 서울·경기·인천 전 지역에서 24시간 긴급 출동 서비스를 제공합니다. 출장비 무료, 미해결 시 비용 0원이라는 파격적인 정책으로 고객 부담을 최소화합니다.",
    "숙련된 전문 기술자가 최첨단 장비(드레인 기계, 관로 내시경 카메라, 고압세척기, 관로탐지기)를 직접 가지고 출동하여 현장에서 즉시 문제를 해결합니다.",
]

# 도시 영문→한글 (추출 시 사용)
# HTML에서 직접 추출하므로 별도 매핑 불필요

# ===== 메인 처리 =====

folders = sorted([f for f in os.listdir(AREA_DIR) if os.path.isdir(os.path.join(AREA_DIR, f))])
print(f"📁 총 {len(folders)}개 페이지 처리 시작")

# 도시→폴더 매핑, 서비스→폴더 매핑 구축
city_folders = {}  # city_en -> [folder1, folder2, ...]
service_folders = {}  # service_en -> [folder1, folder2, ...]

for folder in folders:
    # 서비스 추출 (마지막 하이픈 이후)
    for svc_en in SERVICES_EN:
        if folder.endswith(svc_en):
            city_en = folder[:-(len(svc_en)+1)]
            if city_en not in city_folders:
                city_folders[city_en] = []
            city_folders[city_en].append(folder)
            if svc_en not in service_folders:
                service_folders[svc_en] = []
            service_folders[svc_en].append(folder)
            break

counter = 0
for folder in folders:
    html_path = os.path.join(AREA_DIR, folder, "index.html")
    if not os.path.exists(html_path):
        continue

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 이미 FAQ가 있으면 스킵
    if 'faq-section' in content or 'FAQPage' in content:
        counter += 1
        continue

    # 도시명(한글), 서비스명(한글) 추출
    region_m = re.search(r'"addressRegion":\s*"(.+?)"', content)
    service_m = re.search(r'"serviceType":\s*"(.+?)"', content)
    if not region_m or not service_m:
        counter += 1
        continue

    city_kr = region_m.group(1)
    service_kr = service_m.group(1)

    # 서비스 영문 키 찾기
    service_en = None
    for svc_en in SERVICES_EN:
        if folder.endswith(svc_en):
            service_en = svc_en
            city_en = folder[:-(len(svc_en)+1)]
            break
    if not service_en:
        counter += 1
        continue

    # === 1. FAQ 생성 ===
    faqs = SERVICE_FAQ.get(service_en, SERVICE_FAQ.get("hasugumaghim"))
    # 해시 기반으로 FAQ 순서 셔플 (각 페이지마다 다른 순서)
    seed = int(hashlib.md5(folder.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    faq_list = list(faqs)
    rng.shuffle(faq_list)
    # 3개만 선택
    selected_faqs = faq_list[:3]

    faq_html = '\n<div class="faq-section">\n<h2>{} {} 자주 묻는 질문</h2>\n'.format(city_kr, service_kr)
    for q, a in selected_faqs:
        # 질문에 도시명 포함
        q_with_city = q.replace("하수구", f"{city_kr} 하수구") if city_kr not in q and "하수구" in q else q
        if city_kr not in q_with_city:
            q_with_city = f"{city_kr} 지역 - {q}"
        faq_html += f'<div class="service-box" style="margin:15px 0">\n'
        faq_html += f'<h3 style="color:#1a237e;margin-bottom:8px">Q. {q_with_city}</h3>\n'
        faq_html += f'<p><strong>A.</strong> {a}</p>\n'
        faq_html += f'</div>\n'
    faq_html += '</div>\n'

    # FAQ Schema.org
    faq_schema_items = []
    for q, a in selected_faqs:
        q_with_city = q if city_kr in q else f"{city_kr} 지역 - {q}"
        faq_schema_items.append(f'''    {{
      "@type": "Question",
      "name": "{q_with_city}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a}"
      }}
    }}''')
    faq_schema = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{}
  ]
}}
</script>'''.format(',\n'.join(faq_schema_items))

    # === 2. 내부 링크 생성 ===
    internal_links_html = '\n<div class="internal-links">\n'

    # 같은 도시 다른 서비스 (최대 5개)
    same_city = [f for f in city_folders.get(city_en, []) if f != folder]
    rng.shuffle(same_city)
    if same_city:
        internal_links_html += f'<h2>{city_kr} 지역 다른 서비스</h2>\n<div class="area-tags">\n'
        for related in same_city[:5]:
            for s_en, s_kr in SERVICE_KR.items():
                if related.endswith(s_en):
                    internal_links_html += f'<a href="/area/{related}/" class="area-tag" style="text-decoration:none">{city_kr} {s_kr}</a>\n'
                    break
        internal_links_html += '</div>\n'

    # 같은 서비스 인근 도시 (최대 5개)
    same_service = [f for f in service_folders.get(service_en, []) if f != folder]
    rng.shuffle(same_service)
    if same_service:
        internal_links_html += f'<h2>인근 지역 {service_kr} 서비스</h2>\n<div class="area-tags">\n'
        for related in same_service[:5]:
            for s_en in SERVICES_EN:
                if related.endswith(s_en):
                    r_city_en = related[:-(len(s_en)+1)]
                    # 해당 페이지 HTML에서 한글 도시명 추출
                    r_html_path = os.path.join(AREA_DIR, related, "index.html")
                    if os.path.exists(r_html_path):
                        try:
                            r_content = open(r_html_path, 'r', encoding='utf-8').read()[:500]
                            r_region = re.search(r'"addressRegion":\s*"(.+?)"', r_content)
                            r_city_kr = r_region.group(1) if r_region else r_city_en
                        except:
                            r_city_kr = r_city_en
                    else:
                        r_city_kr = r_city_en
                    internal_links_html += f'<a href="/area/{related}/" class="area-tag" style="text-decoration:none">{r_city_kr} {service_kr}</a>\n'
                    break
        internal_links_html += '</div>\n'

    internal_links_html += '</div>\n'

    # === 3. 추가 콘텐츠 ===
    extra_contents = SERVICE_EXTRA_CONTENT.get(service_en, DEFAULT_EXTRA)
    extra_html = '\n<h2>{} {} 전문가 조언</h2>\n'.format(city_kr, service_kr)
    for para in extra_contents:
        extra_html += f'<p>{para}</p>\n'

    # === 4. Breadcrumb ===
    breadcrumb_html = '<nav style="padding:10px 20px;font-size:0.9em;color:#666"><a href="/" style="color:#1a237e;text-decoration:none">홈</a> &gt; <a href="/area/" style="color:#1a237e;text-decoration:none">서비스 지역</a> &gt; <span>{} {}</span></nav>\n'.format(city_kr, service_kr)

    # === HTML에 삽입 ===

    # Breadcrumb: <body> 바로 뒤에
    content = content.replace('<body>\n', '<body>\n' + breadcrumb_html, 1)

    # FAQ Schema: 기존 </script> 다음, </head> 전에
    content = content.replace('</head>', faq_schema + '\n</head>', 1)

    # FAQ + 내부링크 + 추가콘텐츠: contact-box 바로 앞에
    insert_before = '<div class="contact-box">'
    if insert_before in content:
        content = content.replace(
            insert_before,
            extra_html + faq_html + internal_links_html + '\n' + insert_before,
            1
        )

    # Copyright 연도 업데이트
    content = content.replace('&copy; 2024', '&copy; 2025')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    counter += 1
    if counter % 100 == 0:
        print(f"  진행: {counter}/{len(folders)}")

print(f"\n✅ {counter}개 페이지 SEO 강화 완료!")
print("  - FAQ 섹션 + FAQPage Schema.org 추가")
print("  - 내부 링크 (같은 도시/같은 서비스) 추가")
print("  - 서비스별 고유 콘텐츠 추가")
print("  - Breadcrumb 네비게이션 추가")
