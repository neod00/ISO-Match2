# InsightMatch2

AI 기반 기업 리스크 분석과 최적 컨설턴트 매칭 서비스

## 프로젝트 개요

InsightMatch2는 기업의 홈페이지 URL만 입력하면 AI가 공개정보를 분석하여 리스크를 파악하고, 필요한 인증과 최적의 컨설턴트를 자동으로 매칭해주는 B2B SaaS 서비스입니다.

## 주요 기능

- **AI 기반 기업 분석**: 공개정보 자동 수집 및 리스크 분석
- **전문 컨설턴트 매칭**: 업종별, 인증별 전문가 자동 매칭
- **자동 제안서 생성**: 분석 결과를 PDF로 자동 생성
- **실시간 알림**: 이메일을 통한 분석 결과 전송

## 기술 스택

### 프론트엔드
- HTML/CSS/JavaScript
- Netlify (호스팅)

### 백엔드
- Python Flask
- Railway (호스팅)

### 데이터베이스
- Supabase (PostgreSQL)

### 외부 API
- OpenAI GPT API
- DART API
- Google Sheets API

## 프로젝트 구조

```
InsightMatch2/
├── frontend/          # 프론트엔드 코드
├── backend/           # 백엔드 API 서버
├── docs/             # 문서 (PRD, TASKS)
└── README.md         # 프로젝트 설명
```

## 설치 및 실행

### 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 프론트엔드 실행
```bash
cd frontend
# 정적 파일 서빙 또는 Netlify 배포
```

## 환경 변수

백엔드 실행을 위해 다음 환경 변수를 설정해야 합니다:

- `OPENAI_API_KEY`: OpenAI API 키
- `DART_API_KEY`: DART API 키
- `SUPABASE_URL`: Supabase 프로젝트 URL
- `SUPABASE_KEY`: Supabase API 키

## 라이선스

MIT License
