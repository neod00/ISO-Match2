"""
AI 분석 프롬프트 템플릿
다양한 분석 시나리오에 대한 프롬프트 템플릿
"""

class PromptTemplates:
    """프롬프트 템플릿 클래스"""
    
    @staticmethod
    def get_risk_analysis_prompt(company_data: dict) -> str:
        """리스크 분석 프롬프트"""
        return f"""
당신은 기업 리스크 분석 전문가입니다. 다음 기업 정보를 바탕으로 리스크를 분석해주세요.

기업명: {company_data.get('company', 'Unknown')}
업종: {company_data.get('industry', 'Unknown')}
규모: {company_data.get('size', 'Unknown')}

다음 관점에서 리스크를 분석해주세요:
1. 정보보안 리스크
2. 품질관리 리스크
3. 환경경영 리스크
4. 규제준수 리스크
5. 경영 리스크

각 리스크에 대해 우선순위(High/Medium/Low)와 상세 설명을 제공해주세요.
"""
    
    @staticmethod
    def get_certification_recommendation_prompt(risks: list) -> str:
        """인증 추천 프롬프트"""
        return f"""
다음 리스크 분석 결과를 바탕으로 적절한 인증을 추천해주세요.

식별된 리스크:
{chr(10).join([f"- {risk}" for risk in risks])}

다음 인증 중에서 적절한 것을 추천해주세요:
- ISO 27001 (정보보안)
- ISO 9001 (품질관리)
- ISO 14001 (환경경영)
- ISO 27701 (개인정보보호)
- ISO 45001 (안전보건)
- GDPR 컴플라이언스
- 기타 관련 인증

각 인증에 대해 우선순위와 추천 이유를 설명해주세요.
"""
    
    @staticmethod
    def get_compliance_analysis_prompt(company_data: dict) -> str:
        """규제준수 분석 프롬프트"""
        return f"""
다음 기업의 규제준수 현황을 분석해주세요.

기업 정보:
- 기업명: {company_data.get('company', 'Unknown')}
- 업종: {company_data.get('industry', 'Unknown')}
- 규모: {company_data.get('size', 'Unknown')}

다음 규제 영역에서의 준수 현황을 분석해주세요:
1. 개인정보보호법
2. 정보통신망법
3. 전자상거래법
4. 환경법
5. 노동법
6. 기타 관련 규제

각 영역별로 준수 수준과 개선 방안을 제시해주세요.
"""
    
    @staticmethod
    def get_industry_specific_prompt(industry: str, company_data: dict) -> str:
        """업종별 특화 분석 프롬프트"""
        industry_prompts = {
            'IT': """
IT 기업의 특성을 고려한 리스크 분석:
1. 정보보안 (데이터 유출, 해킹 등)
2. 소프트웨어 품질 (버그, 보안 취약점 등)
3. 개인정보보호 (GDPR, 개인정보보호법 등)
4. 지적재산권 (소프트웨어 라이선스, 특허 등)
5. 클라우드 보안 (AWS, Azure 등)
""",
            '제조': """
제조업의 특성을 고려한 리스크 분석:
1. 품질관리 (불량품, 리콜 등)
2. 환경경영 (폐기물, 오염 등)
3. 안전보건 (산업재해, 작업환경 등)
4. 공급망 관리 (원자재, 부품 등)
5. 제품 안전 (소비자 안전, 인증 등)
""",
            '금융': """
금융업의 특성을 고려한 리스크 분석:
1. 금융보안 (사이버 공격, 사기 등)
2. 규제준수 (금융감독원, FSC 등)
3. 개인정보보호 (금융정보보호법 등)
4. 리스크관리 (신용리스크, 시장리스크 등)
5. 내부통제 (내부감사, 컴플라이언스 등)
""",
            '의료': """
의료업의 특성을 고려한 리스크 분석:
1. 의료정보보호 (환자정보, 의료데이터 등)
2. 의료기기 품질 (FDA, KFDA 인증 등)
3. 개인정보보호 (의료법, 개인정보보호법 등)
4. 의료사고 (의료과실, 의료분쟁 등)
5. 의료윤리 (의료윤리, 환자권리 등)
"""
        }
        
        base_prompt = industry_prompts.get(industry, """
일반적인 기업 리스크 분석:
1. 정보보안 리스크
2. 품질관리 리스크
3. 환경경영 리스크
4. 규제준수 리스크
5. 경영 리스크
""")
        
        return f"""
{industry} 업종의 특성을 고려한 리스크 분석을 수행해주세요.

기업 정보:
- 기업명: {company_data.get('company', 'Unknown')}
- 업종: {industry}

{base_prompt}

각 리스크에 대해 구체적인 분석과 개선 방안을 제시해주세요.
"""
    
    @staticmethod
    def get_summary_prompt(analysis_results: dict) -> str:
        """분석 결과 요약 프롬프트"""
        return f"""
다음 분석 결과를 바탕으로 기업의 핵심 요약을 작성해주세요.

분석 결과:
- 식별된 리스크: {len(analysis_results.get('risks', []))}개
- 추천 인증: {len(analysis_results.get('certifications', []))}개
- 신뢰도: {analysis_results.get('confidence_score', 0.8)}

다음 형식으로 요약해주세요:
1. 기업 현황 (2-3문장)
2. 주요 리스크 (3-4개 핵심 리스크)
3. 권장 조치 (3-4개 우선 조치)
4. 예상 효과 (개선 후 기대 효과)

간결하고 명확하게 작성해주세요.
"""
