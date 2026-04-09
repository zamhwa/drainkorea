# GA4 설정 체크리스트

아래 순서대로 진행하면 전화 클릭 추적이 전환까지 연결됩니다.

## 1) 이벤트 확인

- GA4 `실시간`에서 아래 이벤트가 들어오는지 확인
  - `call_click`
  - `generate_lead`

## 2) 맞춤 측정기준 등록

GA4 > 관리자 > 맞춤 정의 > 맞춤 측정기준 만들기

- `region` (이벤트 매개변수)
- `service` (이벤트 매개변수)
- `intent` (이벤트 매개변수)
- `source` (이벤트 매개변수)
- `medium` (이벤트 매개변수)
- `campaign` (이벤트 매개변수)
- `phone_number` (이벤트 매개변수)

## 3) 전환 설정

GA4 > 관리자 > 이벤트에서 `generate_lead`를 전환으로 표시

## 4) 보고서 확인

- 획득 > 트래픽 획득: source/medium별 유입 확인
- 참여도 > 이벤트: `call_click`, `generate_lead` 추이 확인
- 탐색 보고서: region/service 조합별 전환 비교

## 5) 주간 최적화 루틴

- `docs/gsc-weekly.csv`에 Search Console URL 데이터 반영
- `npm run publish:weekly` 실행
- `docs/weekly-optimization-report.md` 확인
