# InsightMatch2 - PRD

## 1. Problem
중소기업과 스타트업들이 복잡한 규제와 인증 요구사항을 파악하고, 필요한 전문 컨설턴트를 찾는 과정이 비효율적이고 시간이 많이 소요됨. 수동으로 공개정보를 수집하고 분석하는 과정에서 누락이나 오류가 발생할 수 있음.

## 2. Goals & Success Metrics
- **주요 목표**: AI가 기업의 공개정보를 자동 분석하여 리스크를 파악하고 최적의 컨설턴트를 매칭
- **성공 지표**: 
  - 월 100건 이상의 기업 분석 완료
  - 분석 정확도 90% 이상
  - 컨설턴트 매칭 성공률 80% 이상
  - 사용자 만족도 4.5/5 이상

## 3. Non-Goals
- 실시간 채팅 기능
- 결제 시스템 통합
- 다국어 지원 (초기)
- 모바일 앱 개발

## 4. Users & Use Cases
- **중소기업**: 리스크 관리 및 인증 준비
- **스타트업**: 빠른 성장을 위한 리스크 파악
- **기존 기업**: 디지털 전환과 규제 준수
- **컨설턴트**: 전문 분야별 기업 요청 수신
- **관리자**: 컨설턴트 승인 및 매칭 관리

## 5. Assumptions & Constraints
- **기술 제약**: Railway 무료 플랜, Netlify 호스팅
- **API 제약**: DART API, OpenAI GPT API 사용량 제한
- **성능 제약**: 크롤링 시간 60초 이내
- **보안 제약**: 개인정보 보호, API 키 보안

## 6. Dependencies
- Railway (백엔드 호스팅)
- Netlify (프론트엔드 호스팅)
- Supabase (인증 및 데이터베이스)
- OpenAI GPT API
- DART API
- Google Sheets API

## 7. Interfaces
- **API**: RESTful API (Flask)
- **데이터베이스**: Supabase PostgreSQL
- **외부 API**: DART, OpenAI, Google Sheets
- **인증**: Supabase OAuth

## 8. Acceptance Criteria
- [ ] 홈페이지 URL 입력 시 공개정보 자동 수집
- [ ] AI가 리스크 요소 자동 식별 및 인증 추천
- [ ] 컨설턴트 필터링 및 매칭 기능
- [ ] 분석 결과 PDF 제안서 생성
- [ ] 이메일 자동 발송 기능
- [ ] 사용자 인증 및 권한 관리
- [ ] 실시간 분석 진행 상황 표시
- [ ] 에러 핸들링 및 로깅

## 9. Risks & Mitigations
- **API 제한**: 사용량 모니터링 및 캐싱 전략
- **크롤링 실패**: 폴백 데이터 및 재시도 로직
- **성능 이슈**: 비동기 처리 및 최적화
- **보안 취약점**: 입력 검증 및 API 키 보안

## 10. Rollout & Monitoring
- **배포**: Railway + Netlify 연동
- **모니터링**: Railway 대시보드, Supabase 로그
- **알림**: 에러 발생 시 이메일 알림
- **백업**: 정기적 데이터 백업

## 11. Open Questions (ASK)
- [ ] DART API 사용량 제한 정책 확인 필요
- [ ] OpenAI GPT 모델 선택 (gpt-4o-mini vs gpt-4)
- [ ] 컨설턴트 데이터 초기 입력 방법
- [ ] 분석 결과 저장 기간 정책
- [ ] 사용자별 분석 횟수 제한 여부
