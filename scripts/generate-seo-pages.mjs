import fs from "node:fs";
import path from "node:path";

const rootDir = path.resolve(process.cwd());
const docsDir = path.join(rootDir, "docs");
const siteUrl = "https://drainkorea.com";
const phone = "010-4406-1788";

const seoPageInitial = 1000;
const blogPostInitial = 120;
const seoGrowPerRun = 30;
const blogGrowPerRun = 6;
const abTestTopLimit = 100;
const growthStatePath = path.join(docsDir, ".growth-state.json");

const services = [
  { slug: "drain-blocked", keyword: "하수구 막힘" },
  { slug: "toilet-blocked", keyword: "변기 막힘" },
  { slug: "sink-blocked", keyword: "싱크대 막힘" },
  { slug: "sewer-cleaning", keyword: "배관 고압세척" },
  { slug: "backflow", keyword: "하수구 역류" }
];

const intents = [
  { slug: "urgent", keyword: "긴급 출동", titleToken: "긴급" },
  { slug: "24hour", keyword: "24시간", titleToken: "24시간" },
  { slug: "cost", keyword: "비용", titleToken: "비용" },
  { slug: "company", keyword: "업체", titleToken: "업체" },
  { slug: "same-day", keyword: "당일 해결", titleToken: "당일" },
  { slug: "weekend", keyword: "주말 출동", titleToken: "주말" }
];

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function hashText(text) {
  let hash = 0;
  for (let i = 0; i < text.length; i += 1) {
    hash = (hash * 31 + text.charCodeAt(i)) >>> 0;
  }
  return hash;
}

function pick(text, list, offset = 0) {
  const idx = (hashText(text) + offset) % list.length;
  return list[idx];
}

function slugifyKoreanTerm(text) {
  return text
    .replace(/\s+/g, "-")
    .replace(/[^\w\-가-힣]/g, "")
    .toLowerCase();
}

function buildRegionTerm(item) {
  if (item.siName === "서울특별시") {
    return `${item.guName} ${item.name}`;
  }
  return `${item.siName.replace("광역시", "").replace("특별시", "").replace("도", "")} ${item.guName} ${item.name}`;
}

function buildSeoBody({ regionTerm, serviceKeyword, intentKeyword, keySeed }) {
  const urgencyLines = [
    "배수 장애는 시간이 지날수록 피해가 커지기 때문에 접수 직후 가장 가까운 기사팀을 우선 배정합니다.",
    "악취, 역류, 누수 징후가 동반되는 경우 1차 차단 조치를 먼저 하고 본 작업으로 이어갑니다.",
    "심야 시간대에도 동일 프로세스로 배차해 대기 시간을 줄이고 추가 피해를 막습니다."
  ];
  const causeLines = [
    "주요 원인은 기름 슬러지, 비누 찌꺼기, 머리카락, 음식물 미세입자 누적입니다.",
    "노후 배관의 단차 구간이나 굴곡 구간에서 이물질이 뭉치며 유속이 급격히 떨어집니다.",
    "우수관/오수관 연결부 오염은 비가 오지 않아도 내부 압력 변화를 만들어 역류를 유발할 수 있습니다."
  ];
  const processLines = [
    "내시경 진단으로 문제 구간을 특정한 뒤 장비 압력 값을 상황에 맞게 조정해 단계적으로 제거합니다.",
    "분해 가능한 부속을 먼저 정리하고 메인 배관은 세척 장비로 단면을 복원합니다.",
    "작업 완료 후 유량 테스트와 냄새 점검을 진행해 재막힘 가능성을 낮춥니다."
  ];
  const preventionLines = [
    "주방 기름류 분리 배출, 거름망 관리, 월 단위 점검만 지켜도 재발 빈도를 크게 줄일 수 있습니다.",
    "상가/오피스텔처럼 사용량이 많은 공간은 정기 점검 주기를 더 짧게 운영하는 것이 안전합니다.",
    "재발 패턴이 있는 현장은 배관 구간별 사용 기록을 남기면 원인 추적 속도가 빨라집니다."
  ];

  const line1 = pick(keySeed, urgencyLines, 1);
  const line2 = pick(keySeed, causeLines, 2);
  const line3 = pick(keySeed, processLines, 3);
  const line4 = pick(keySeed, preventionLines, 4);

  const p1 = `${regionTerm} ${serviceKeyword} 검색으로 문의 주시는 분들은 대체로 갑작스러운 배수 지연, 악취, 역류 문제를 동시에 겪고 있습니다. ${regionTerm} 현장은 건물 연식과 사용 패턴이 다양해서 같은 증상이라도 원인이 달라집니다. ${line1}`;
  const p2 = `${regionTerm} ${serviceKeyword}의 핵심은 원인 구간을 정확히 찾는 것입니다. ${line2} ${regionTerm} ${serviceKeyword} 작업은 임시 조치가 아니라 재발 방지까지 설계해야 실제 만족도가 높습니다.`;
  const p3 = `${regionTerm} ${intentKeyword} 수요가 많은 이유는 피해 확산 속도 때문입니다. ${line3} 현장에서는 작업 전 예상 범위를 먼저 설명하고, 완료 후 점검 결과를 고객에게 바로 안내합니다.`;
  const p4 = `${regionTerm} ${serviceKeyword} ${intentKeyword} 문의 시 비용과 시간은 현장 상태에 따라 달라질 수 있지만, 초기 진단 품질이 결과를 좌우합니다. 배관 단면 복원까지 진행하면 단기 재발 확률을 크게 낮출 수 있습니다.`;
  const p5 = `${regionTerm} 지역은 주거형, 상가형, 복합건물형 현장이 혼재되어 있어 동일 장비를 고정 사용하지 않습니다. ${serviceKeyword} 작업은 현장별 압력값과 장비 타입을 달리 적용하는 것이 안전합니다.`;
  const p6 = `${regionTerm} ${serviceKeyword} 재발 방지 단계에서는 사용자 습관 점검이 필수입니다. ${line4} 특히 ${regionTerm}처럼 유동 인구가 많은 지역은 정기 점검 계획을 함께 운영하는 것이 비용 관리에 유리합니다.`;

  return [p1, p2, p3, p4, p5, p6];
}

function buildTitleVariants(page) {
  const { regionTerm, serviceKeyword, titleToken } = page;
  const titleA = `${regionTerm} ${serviceKeyword} ${titleToken} | 30분 출동 24시간 상담`;
  const titleB = `${regionTerm} ${serviceKeyword} ${titleToken} 전문 업체 | 당일 방문 가능`;
  return { titleA, titleB };
}

function renderSeoPage(page, relatedLinks, titleOverride) {
  const { regionTerm, serviceKeyword, intentKeyword, titleToken, slug } = page;
  const titleTemplates = [
    `${regionTerm} ${serviceKeyword} ${titleToken} | 30분 출동 24시간 상담`,
    `${regionTerm} ${serviceKeyword} ${titleToken} 빠른 해결 | 비용 안내`,
    `${regionTerm} ${serviceKeyword} ${titleToken} 전문 업체 | 당일 방문 가능`
  ];
  const title = titleOverride ?? titleTemplates[hashText(slug) % titleTemplates.length];
  const description = `${regionTerm} ${serviceKeyword} ${intentKeyword} 문의 대응. 원인 진단부터 재발 방지까지 현장 맞춤으로 처리합니다.`;
  const canonical = `${siteUrl}/seo/${slug}/`;
  const keySeed = `${slug}-${serviceKeyword}-${intentKeyword}`;
  const sections = buildSeoBody({ regionTerm, serviceKeyword, intentKeyword, keySeed });
  const faqQ1 = `${regionTerm} ${serviceKeyword} 문의 시 정말 30분 내 출동이 가능한가요?`;
  const faqQ2 = `${regionTerm} ${serviceKeyword} 작업 비용은 어떻게 결정되나요?`;
  const faqQ3 = `${regionTerm} ${serviceKeyword} 작업 후 재발 가능성은 어느 정도인가요?`;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    name: `${regionTerm} 배관 긴급 출동`,
    areaServed: regionTerm,
    description,
    telephone: phone,
    url: canonical
  };

  return `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title}</title>
  <meta name="description" content="${description}">
  <link rel="canonical" href="${canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${title}">
  <meta property="og:description" content="${description}">
  <meta property="og:url" content="${canonical}">
  <script type="application/ld+json">${JSON.stringify(jsonLd)}</script>
  <style>
    * { box-sizing: border-box; }
    body { font-family: 'Noto Sans KR', Arial, sans-serif; max-width: 980px; margin: 0 auto; padding: 24px; color: #0f172a; line-height: 1.75; }
    h1 { font-size: 32px; margin-bottom: 8px; }
    h2 { margin-top: 22px; margin-bottom: 8px; font-size: 24px; }
    h3 { margin-top: 16px; margin-bottom: 6px; font-size: 20px; }
    .badge { display: inline-block; background: #fee2e2; color: #b91c1c; border-radius: 999px; padding: 6px 14px; font-weight: 700; }
    .card { margin: 16px 0; padding: 16px; border: 1px solid #e2e8f0; border-radius: 12px; background: #f8fafc; }
    .cta { display: inline-block; margin-top: 8px; background: #dc2626; color: #fff; padding: 12px 18px; text-decoration: none; border-radius: 10px; font-weight: 700; }
    .links a { display: block; margin: 6px 0; color: #0369a1; text-decoration: none; }
    .faq-item { margin: 12px 0; }
  </style>
</head>
<body>
  <h1>${regionTerm} ${serviceKeyword}</h1>
  <p class="badge">긴급성: 30분 출동 / 24시간 상담</p>

  <section class="card">
    <h2>문제 상황 설명</h2>
    <p>${sections[0]}</p>
    <h2>원인 분석</h2>
    <p>${sections[1]}</p>
    <h2>해결 방법</h2>
    <p>${sections[2]}</p>
    <h2>작업 과정 (스토리형)</h2>
    <p>${sections[3]}</p>
    <h2>재발 방지 방법</h2>
    <p>${sections[4]}</p>
    <h2>${intentKeyword} 체크 포인트</h2>
    <p>${sections[5]}</p>
  </section>

  <section class="card">
    <h2>CTA</h2>
    <p>${regionTerm} ${serviceKeyword} 문의는 접수 즉시 기사 배차를 시작합니다.</p>
    <a class="cta js-call-cta" data-region="${regionTerm}" data-service="${serviceKeyword}" data-intent="${intentKeyword}" href="tel:${phone.replaceAll("-", "")}">전화 상담 ${phone}</a>
  </section>

  <section class="card">
    <h2>FAQ</h2>
    <article class="faq-item"><h3>${faqQ1}</h3><p>근접 기사 우선 배정 방식으로 평균 도착 시간을 단축해 안내합니다.</p></article>
    <article class="faq-item"><h3>${faqQ2}</h3><p>막힘 위치, 오염 범위, 장비 사용 범위를 기준으로 현장 설명 후 확정합니다.</p></article>
    <article class="faq-item"><h3>${faqQ3}</h3><p>원인 구간 제거 후 유량 테스트와 사용 가이드까지 제공해 재발률을 낮춥니다.</p></article>
  </section>

  <section class="card links">
    <h2>내부 링크</h2>
    ${relatedLinks.map((link) => `<a href="${link.href}">${link.label}</a>`).join("")}
    <a href="/seo/">지역/서비스 전체 페이지 보기</a>
    <a href="/blog/">배관 관리 블로그 보기</a>
    <a href="/">메인 페이지 이동</a>
  </section>
  <script>
    (function () {
      var links = document.querySelectorAll('.js-call-cta');
      var GA_ID = 'G-LYP8WVVCQY';
      function getAttribution() {
        var params = new URLSearchParams(window.location.search);
        var source = params.get('utm_source') || sessionStorage.getItem('utm_source') || '(direct)';
        var medium = params.get('utm_medium') || sessionStorage.getItem('utm_medium') || '(none)';
        var campaign = params.get('utm_campaign') || sessionStorage.getItem('utm_campaign') || '';
        if (params.get('utm_source')) sessionStorage.setItem('utm_source', source);
        if (params.get('utm_medium')) sessionStorage.setItem('utm_medium', medium);
        if (params.get('utm_campaign')) sessionStorage.setItem('utm_campaign', campaign);
        return { source: source, medium: medium, campaign: campaign };
      }
      function trackEvent(name, data) {
        if (typeof window.gtag === 'function') {
          window.gtag('event', name, data);
        }
      }
      if (GA_ID && !window.__gaBooted) {
        window.__gaBooted = true;
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
        document.head.appendChild(s);
        window.dataLayer = window.dataLayer || [];
        function gtag(){window.dataLayer.push(arguments);}
        window.gtag = window.gtag || gtag;
        gtag('js', new Date());
        gtag('config', GA_ID);
      }
      links.forEach(function (link) {
        var clicked = false;
        link.addEventListener('click', function () {
          if (clicked) return;
          clicked = true;
          var attr = getAttribution();
          var payload = {
            region: link.getAttribute('data-region') || '',
            service: link.getAttribute('data-service') || '',
            intent: link.getAttribute('data-intent') || '',
            phone_number: '${phone}',
            page_path: location.pathname,
            source: attr.source,
            medium: attr.medium,
            campaign: attr.campaign
          };
          trackEvent('call_click', payload);
          trackEvent('generate_lead', payload);
        });
      });
    })();
  </script>
</body>
</html>`;
}

function renderSeoHub(cards) {
  return `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>수도권 배관 SEO 페이지 모음</title>
  <meta name="description" content="수도권 지역별 하수구, 변기, 싱크대, 고압세척, 역류 페이지 모음">
  <style>
    body{font-family:'Noto Sans KR',Arial,sans-serif;max-width:1080px;margin:0 auto;padding:24px}
    .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
    a{display:block;padding:10px;border:1px solid #e2e8f0;border-radius:10px;text-decoration:none;color:#0369a1}
    @media(max-width:780px){.grid{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <h1>수도권 지역 + 서비스 페이지</h1>
  <p>실검색형 키워드 기준으로 구성한 페이지 모음입니다.</p>
  <div class="grid">${cards.join("")}</div>
  <p><a href="/blog/">블로그 보기</a> | <a href="/">메인으로</a></p>
</body>
</html>`;
}

function renderBlogPost(post) {
  const canonical = `${siteUrl}/blog/${post.slug}/`;
  return `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${post.title}</title>
  <meta name="description" content="${post.description}">
  <link rel="canonical" href="${canonical}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="${post.title}">
  <meta property="og:description" content="${post.description}">
  <meta property="og:url" content="${canonical}">
  <style>
    body{font-family:'Noto Sans KR',Arial,sans-serif;max-width:900px;margin:0 auto;padding:24px;line-height:1.8}
    h1{font-size:30px} h2{font-size:22px;margin-top:20px}
    .box{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px;margin:14px 0}
    a{color:#0369a1}
  </style>
</head>
<body>
  <h1>${post.title}</h1>
  <p>${post.description}</p>
  <section class="box"><h2>핵심 요약</h2><p>${post.p1}</p></section>
  <section class="box"><h2>문제 원인</h2><p>${post.p2}</p></section>
  <section class="box"><h2>현장 대응</h2><p>${post.p3}</p></section>
  <section class="box"><h2>비용/시간 포인트</h2><p>${post.p4}</p></section>
  <section class="box"><h2>재발 방지</h2><p>${post.p5}</p></section>
  <section class="box"><h2>체크리스트</h2><p>${post.p6}</p></section>
  <p><a href="/blog/">블로그 목록</a> | <a href="/seo/">SEO 페이지 모음</a> | <a href="/">메인</a></p>
</body>
</html>`;
}

function renderBlogIndex(cards) {
  return `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>배관 관리 블로그</title>
  <meta name="description" content="하수구, 변기, 싱크대, 고압세척, 역류 관련 실전 블로그">
  <style>
    body{font-family:'Noto Sans KR',Arial,sans-serif;max-width:980px;margin:0 auto;padding:24px}
    article{border:1px solid #e2e8f0;border-radius:12px;padding:14px;margin:10px 0}
    a{color:#0369a1}
  </style>
</head>
<body>
  <h1>배관 관리 블로그</h1>
  <p>지역 기반 검색 의도에 맞춘 실전 가이드 글입니다.</p>
  ${cards.join("")}
  <p><a href="/seo/">SEO 페이지 모음</a> | <a href="/">메인</a></p>
</body>
</html>`;
}

function prepareGeneratedDirectories() {
  ensureDir(path.join(docsDir, "seo"));
  ensureDir(path.join(docsDir, "blog"));
}

function toSiPriority(siName) {
  if (siName === "서울특별시") return 1;
  if (siName === "경기도") return 2;
  if (siName === "인천광역시") return 3;
  return 4;
}

function buildSeoCandidates(activeDongs, seoLimit) {
  const sortedDongs = activeDongs.sort((a, b) => {
    const pA = toSiPriority(a.siName);
    const pB = toSiPriority(b.siName);
    if (pA !== pB) return pA - pB;
    return `${a.guName}${a.name}`.localeCompare(`${b.guName}${b.name}`, "ko");
  });

  const candidates = [];
  for (const dong of sortedDongs) {
    const regionTerm = buildRegionTerm(dong);
    for (const service of services) {
      for (const intent of intents) {
        const slug = `${dong.code}-${service.slug}-${intent.slug}-${slugifyKoreanTerm(regionTerm)}`;
        candidates.push({
          slug,
          regionTerm,
          serviceKeyword: service.keyword,
          intentKeyword: intent.keyword,
          titleToken: intent.titleToken,
          siName: dong.siName,
          guName: dong.guName
        });
      }
    }
  }
  return candidates.slice(0, seoLimit);
}

function makeRelatedLinks(current, pages) {
  const sameGu = pages.filter((p) => p.guName === current.guName && p.slug !== current.slug).slice(0, 4);
  const sameService = pages.filter((p) => p.serviceKeyword === current.serviceKeyword && p.slug !== current.slug).slice(0, 4);
  const deduped = [];
  const seen = new Set();
  for (const item of [...sameGu, ...sameService]) {
    if (!seen.has(item.slug)) {
      seen.add(item.slug);
      deduped.push(item);
    }
    if (deduped.length >= 8) {
      break;
    }
  }
  return deduped.map((item) => ({
    href: `/seo/${item.slug}/`,
    label: `${item.regionTerm} ${item.serviceKeyword} ${item.intentKeyword}`
  }));
}

function buildBlogPostsFromPages(pages, blogLimit) {
  const posts = [];
  for (let i = 0; i < blogLimit; i += 1) {
    const seedPage = pages[(i * 7) % pages.length];
    const topic = `(${i + 1}) ${seedPage.regionTerm} ${seedPage.serviceKeyword} ${seedPage.intentKeyword}`;
    const title = `${seedPage.regionTerm} ${seedPage.serviceKeyword} 실전 가이드 ${i + 1}`;
    const slug = `seo-guide-${i + 1}-${seedPage.slug.slice(0, 12)}`;
    const description = `${seedPage.regionTerm} ${seedPage.serviceKeyword} 문의 시 실제로 필요한 점검 포인트와 대응 순서를 정리했습니다.`;
    const baseSeed = `${slug}-${topic}`;
    const p1 = `${seedPage.regionTerm} ${seedPage.serviceKeyword} 문의는 증상이 비슷해 보여도 원인 구간이 다른 경우가 많습니다. 초기 접수 단계에서 발생 시점, 사용 공간, 악취/역류 동반 여부를 함께 확인하면 진단 정확도가 크게 올라갑니다.`;
    const p2 = `${seedPage.regionTerm} 현장에서 반복 확인되는 원인은 기름 슬러지, 음식물 입자, 머리카락, 비누 찌꺼기 누적입니다. ${pick(baseSeed, ["특히 상가형 건물은 사용량 편차가 커서 막힘이 갑자기 심해질 수 있습니다.", "주거형 현장은 장기간 누적 후 특정 시간대에 증상이 한 번에 터지는 패턴이 많습니다.", "노후 배관 구간은 단차 부위에서 이물질이 고착되기 쉬워 재발률이 높습니다."], 1)}`;
    const p3 = `${seedPage.regionTerm} ${seedPage.serviceKeyword} 대응은 원인 구간 특정, 단계별 제거, 세척, 유량 테스트 순서로 진행해야 재작업을 줄일 수 있습니다. 임시 뚫음만 반복하면 단기적으로는 해결되어도 동일 문제가 빠르게 재발합니다.`;
    const p4 = `${seedPage.intentKeyword} 관점에서 보면 비용은 작업 범위와 장비 시간에 따라 달라집니다. 따라서 정확한 진단 없이 가격만 비교하기보다, 작업 후 재발 방지 계획까지 포함해 비교하는 것이 장기적으로 유리합니다.`;
    const p5 = `${seedPage.regionTerm} ${seedPage.serviceKeyword} 재발 방지를 위해서는 거름망 관리, 기름류 분리 배출, 월 단위 점검 루틴이 핵심입니다. 이 세 가지를 유지하면 긴급 출동 빈도와 유지 비용을 동시에 낮출 수 있습니다.`;
    const p6 = `${seedPage.regionTerm}에서 ${seedPage.serviceKeyword} 관련 정보를 찾는 사용자에게 중요한 것은 빠른 출동만이 아니라, 원인 설명의 투명성과 사후 점검 체계입니다. 점검 기록을 남기면 다음 문제가 생겨도 대응 속도가 크게 빨라집니다.`;
    posts.push({ title, slug, description, p1, p2, p3, p4, p5, p6 });
  }
  return posts;
}

async function run() {
  prepareGeneratedDirectories();

  const dongData = await (await fetch("https://kr-legal-dong.github.io/data/dong.json")).json();
  const activeDongs = dongData.filter(
    (item) => item.active && (item.siName === "서울특별시" || item.siName === "경기도" || item.siName === "인천광역시")
  );

  const allPossibleSeo = activeDongs.length * services.length * intents.length;
  const existingSeoCount = fs.existsSync(path.join(docsDir, "seo"))
    ? fs.readdirSync(path.join(docsDir, "seo"), { withFileTypes: true }).filter((d) => d.isDirectory()).length
    : 0;
  const existingBlogCount = fs.existsSync(path.join(docsDir, "blog"))
    ? fs.readdirSync(path.join(docsDir, "blog"), { withFileTypes: true }).filter((d) => d.isDirectory()).length
    : 0;

  const state = fs.existsSync(growthStatePath)
    ? JSON.parse(fs.readFileSync(growthStatePath, "utf8"))
    : { seoTarget: seoPageInitial, blogTarget: blogPostInitial, runCount: 0 };

  const prevSeoTarget = Math.max(state.seoTarget || seoPageInitial, existingSeoCount, seoPageInitial);
  const prevBlogTarget = Math.max(state.blogTarget || blogPostInitial, existingBlogCount, blogPostInitial);
  const nextSeoTarget = Math.min(prevSeoTarget + seoGrowPerRun, allPossibleSeo);
  const nextBlogTarget = prevBlogTarget + blogGrowPerRun;

  const pages = buildSeoCandidates(activeDongs, nextSeoTarget);
  const sitemapUrls = ["/", "/seo/", "/blog/"];
  const seoCards = [];
  const abRows = ["url,title_a,title_b,applied_variant,applied_title"];

  for (let i = 0; i < pages.length; i += 1) {
    const page = pages[i];
    const { titleA, titleB } = buildTitleVariants(page);
    const appliedVariant = i < abTestTopLimit ? (i % 2 === 0 ? "A" : "B") : "A";
    const appliedTitle = appliedVariant === "A" ? titleA : titleB;
    const relatedLinks = makeRelatedLinks(page, pages);
    const html = renderSeoPage(page, relatedLinks, appliedTitle);
    const targetDir = path.join(docsDir, "seo", page.slug);
    ensureDir(targetDir);
    fs.writeFileSync(path.join(targetDir, "index.html"), html, "utf8");
    seoCards.push(`<a href="/seo/${page.slug}/">${page.regionTerm} ${page.serviceKeyword} ${page.intentKeyword}</a>`);
    sitemapUrls.push(`/seo/${page.slug}/`);
    if (i < Math.min(abTestTopLimit, pages.length)) {
      const pageUrl = `${siteUrl}/seo/${page.slug}/`;
      const csvSafe = (value) => `"${String(value).replaceAll("\"", "\"\"")}"`;
      abRows.push(
        [pageUrl, titleA, titleB, appliedVariant, appliedTitle].map(csvSafe).join(",")
      );
    }
  }

  fs.writeFileSync(path.join(docsDir, "seo", "index.html"), renderSeoHub(seoCards), "utf8");

  const blogPosts = buildBlogPostsFromPages(pages, nextBlogTarget);
  const blogCards = [];
  for (const post of blogPosts) {
    const targetDir = path.join(docsDir, "blog", post.slug);
    ensureDir(targetDir);
    fs.writeFileSync(path.join(targetDir, "index.html"), renderBlogPost(post), "utf8");
    blogCards.push(`<article><h2><a href="/blog/${post.slug}/">${post.title}</a></h2><p>${post.description}</p></article>`);
    sitemapUrls.push(`/blog/${post.slug}/`);
  }
  fs.writeFileSync(path.join(docsDir, "blog", "index.html"), renderBlogIndex(blogCards), "utf8");
  fs.writeFileSync(path.join(docsDir, "seo-title-ab.csv"), `${abRows.join("\n")}\n`, "utf8");

  const nextState = {
    seoTarget: pages.length,
    blogTarget: blogPosts.length,
    runCount: (state.runCount || 0) + 1,
    updatedAt: new Date().toISOString()
  };
  fs.writeFileSync(growthStatePath, JSON.stringify(nextState, null, 2), "utf8");

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemapUrls.map((url) => `  <url><loc>${siteUrl}${url}</loc></url>`).join("\n")}
</urlset>`;
  fs.writeFileSync(path.join(docsDir, "sitemap.xml"), sitemapXml, "utf8");

  console.log(`Total possible SEO combinations (region x service x intent): ${allPossibleSeo}`);
  console.log(`SEO target: ${pages.length} (+${Math.max(pages.length - existingSeoCount, 0)} vs existing)`);
  console.log(`Blog target: ${blogPosts.length} (+${Math.max(blogPosts.length - existingBlogCount, 0)} vs existing)`);
  console.log(`SEO pages generated: ${pages.length}`);
  console.log(`Blog pages generated: ${blogPosts.length}`);
  console.log(`AB title test rows generated: ${abRows.length - 1}`);
  console.log("Generated files: docs/seo, docs/blog, docs/sitemap.xml, docs/seo-title-ab.csv, docs/.growth-state.json");
}

run().catch((error) => {
  console.error("Generation failed:", error);
  process.exit(1);
});
