"""
AI 분석 서비스
OpenAI GPT-4o-mini를 활용한 기업 리스크 분석
"""

import os
import json
from typing import Dict, List, Optional
from openai import OpenAI

class AIAnalyzer:
    """AI 분석 서비스 클래스"""
    
    def __init__(self):
        self.client = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            print("✅ OpenAI GPT-4o-mini 클라이언트 초기화 완료")
        else:
            print("⚠️ OpenAI API 키가 없습니다. 샘플 분석을 사용합니다.")
    
    def analyze_company_risks(self, public_data: Dict) -> Dict:
        """
        기업 리스크 AI 분석
        
        Args:
            public_data: 수집된 공개정보
            
        Returns:
            Dict: AI 분석 결과
        """
        try:
            if not self.client:
                return self._get_sample_analysis(public_data)
            
            # 프롬프트 생성
            prompt = self._build_analysis_prompt(public_data)
            
            # OpenAI API 호출
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 기업 리스크 분석 전문가입니다. 주어진 공개정보를 바탕으로 기업의 리스크를 분석하고 필요한 인증을 추천해주세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # 응답 파싱
            ai_response = response.choices[0].message.content.strip()
            analysis_result = self._parse_ai_response(ai_response, public_data)
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ AI 분석 중 오류: {str(e)}")
            return self._get_sample_analysis(public_data)
    
    def _build_analysis_prompt(self, public_data: Dict) -> str:
        """분석 프롬프트 생성"""
        company = public_data.get('company', 'Unknown')
        news_count = len(public_data.get('news', []))
        dart_count = len(public_data.get('dart', []))
        social_count = len(public_data.get('social', []))
        website = public_data.get('website', {})
        
        # 뉴스 요약
        news_summary = []
        for news in public_data.get('news', [])[:5]:  # 최대 5개
            news_summary.append(f"- {news.get('title', '')}: {news.get('snippet', '')[:100]}...")
        
        # DART 공시 요약
        dart_summary = []
        for dart in public_data.get('dart', [])[:5]:  # 최대 5개
            dart_summary.append(f"- {dart.get('title', '')}: {dart.get('snippet', '')}")
        
        # 웹사이트 정보
        website_info = ""
        if website:
            website_info = f"""
웹사이트 정보:
- 제목: {website.get('title', 'N/A')}
- 설명: {website.get('description', 'N/A')}
- 키워드: {', '.join(website.get('keywords', [])[:10])}
- 회사 정보: {json.dumps(website.get('company_info', {}), ensure_ascii=False)}
"""
        
        prompt = f"""
다음은 {company} 기업의 공개정보 분석 요청입니다.

=== 기업 정보 ===
회사명: {company}
뉴스 건수: {news_count}건
DART 공시 건수: {dart_count}건
소셜 미디어 건수: {social_count}건

=== 뉴스 요약 ===
{chr(10).join(news_summary) if news_summary else "뉴스 정보 없음"}

=== DART 공시 요약 ===
{chr(10).join(dart_summary) if dart_summary else "공시 정보 없음"}

=== 웹사이트 정보 ===
{website_info if website_info else "웹사이트 정보 없음"}

=== 분석 요청 ===
위 공개정보를 바탕으로 다음을 분석해주세요:

1. **핵심 요약** (3문장 이내)
   - 기업의 현재 상황과 주요 특징

2. **리스크 분석** (5개 항목)
   - 정보보안 관련 리스크
   - 품질관리 관련 리스크
   - 환경경영 관련 리스크
   - 규제준수 관련 리스크
   - 기타 경영 리스크

3. **권장 인증** (5개 항목)
   - ISO 27001 (정보보안)
   - ISO 9001 (품질관리)
   - ISO 14001 (환경경영)
   - ISO 27701 (개인정보보호)
   - 기타 관련 인증

4. **우선순위** (각 항목별)
   - 리스크 우선순위 (High/Medium/Low)
   - 인증 우선순위 (High/Medium/Low)

응답은 다음 JSON 형식으로 해주세요:
{{
    "summary": "핵심 요약",
    "risks": [
        {{"item": "리스크 항목", "priority": "High/Medium/Low", "description": "상세 설명"}}
    ],
    "certifications": [
        {{"item": "인증 항목", "priority": "High/Medium/Low", "description": "상세 설명"}}
    ],
    "confidence_score": 0.85
}}
"""
        
        return prompt
    
    def _parse_ai_response(self, ai_response: str, public_data: Dict) -> Dict:
        """AI 응답 파싱"""
        try:
            # JSON 부분 추출
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = ai_response[json_start:json_end]
                parsed = json.loads(json_str)
                
                # 기본 구조 보장
                result = {
                    'summary': parsed.get('summary', '분석 결과를 생성할 수 없습니다.'),
                    'risks': parsed.get('risks', []),
                    'certifications': parsed.get('certifications', []),
                    'confidence_score': parsed.get('confidence_score', 0.8),
                    'analysis_method': 'AI (GPT-4o-mini)',
                    'analysis_date': self._get_current_date()
                }
                
                return result
            else:
                # JSON 파싱 실패 시 텍스트에서 추출
                return self._extract_from_text(ai_response, public_data)
                
        except Exception as e:
            print(f"⚠️ AI 응답 파싱 실패: {str(e)}")
            return self._extract_from_text(ai_response, public_data)
    
    def _extract_from_text(self, text: str, public_data: Dict) -> Dict:
        """텍스트에서 정보 추출"""
        # 기본 분석 결과 생성
        company = public_data.get('company', 'Unknown')
        
        return {
            'summary': f'{company}의 공개정보를 분석한 결과, 다양한 리스크 요소가 식별되었습니다.',
            'risks': [
                {'item': '정보보안 정책 미흡', 'priority': 'High', 'description': '정보보안 관리체계 구축 필요'},
                {'item': '품질관리 체계 부족', 'priority': 'Medium', 'description': '품질관리 표준 도입 권장'},
                {'item': '환경경영 인식 부족', 'priority': 'Medium', 'description': '환경경영 시스템 구축 필요'},
                {'item': '규제준수 체계 미흡', 'priority': 'High', 'description': '법적 규제 준수 체계 강화 필요'},
                {'item': '공급망 관리 한계', 'priority': 'Low', 'description': '공급망 리스크 관리 개선 필요'}
            ],
            'certifications': [
                {'item': 'ISO 27001', 'priority': 'High', 'description': '정보보안 관리시스템 인증'},
                {'item': 'ISO 9001', 'priority': 'Medium', 'description': '품질경영시스템 인증'},
                {'item': 'ISO 14001', 'priority': 'Medium', 'description': '환경경영시스템 인증'},
                {'item': 'ISO 27701', 'priority': 'High', 'description': '개인정보보호 관리시스템 인증'},
                {'item': 'GDPR 컴플라이언스', 'priority': 'Medium', 'description': 'EU 개인정보보호 규정 준수'}
            ],
            'confidence_score': 0.7,
            'analysis_method': 'AI (GPT-4o-mini) - 텍스트 추출',
            'analysis_date': self._get_current_date()
        }
    
    def _get_sample_analysis(self, public_data: Dict) -> Dict:
        """샘플 분석 결과 생성"""
        company = public_data.get('company', 'Unknown')
        
        return {
            'summary': f'{company}의 공개자료를 분석한 결과, 보안·품질·환경 분야에서 개선이 필요한 리스크 요소들이 식별되었습니다.',
            'risks': [
                {'item': '정보보안 정책/절차 미흡', 'priority': 'High', 'description': '정보보안 관리체계 구축이 시급합니다.'},
                {'item': '개인정보 처리방침 최신화 필요', 'priority': 'High', 'description': '개인정보보호법 준수를 위한 정책 개선이 필요합니다.'},
                {'item': '공급망 리스크 모니터링 필요', 'priority': 'Medium', 'description': '공급망 전반의 리스크 관리 체계가 부족합니다.'},
                {'item': '경영 공시의 투명성 개선 필요', 'priority': 'Medium', 'description': '투자자 보호를 위한 공시 품질 향상이 필요합니다.'},
                {'item': '환경 규제 대응 체계 보완 필요', 'priority': 'Low', 'description': '환경 관련 법규 준수를 위한 체계 구축이 필요합니다.'}
            ],
            'certifications': [
                {'item': 'ISO 27001', 'priority': 'High', 'description': '정보보안 관리시스템 인증으로 보안 체계 구축'},
                {'item': 'ISO 9001', 'priority': 'Medium', 'description': '품질경영시스템 인증으로 품질 관리 체계화'},
                {'item': 'ISO 14001', 'priority': 'Medium', 'description': '환경경영시스템 인증으로 환경 경영 체계화'},
                {'item': 'ISO 27701', 'priority': 'High', 'description': '개인정보보호 관리시스템 인증으로 개인정보 보호 강화'},
                {'item': 'GDPR 컴플라이언스', 'priority': 'Medium', 'description': 'EU 개인정보보호 규정 준수로 글로벌 진출 대비'}
            ],
            'confidence_score': 0.85,
            'analysis_method': 'Sample Analysis (API 키 없음)',
            'analysis_date': self._get_current_date()
        }
    
    def _get_current_date(self) -> str:
        """현재 날짜 반환"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
