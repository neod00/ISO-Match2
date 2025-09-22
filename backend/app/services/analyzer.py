"""
기업 분석 서비스
"""

import re
from urllib.parse import urlparse
from typing import Dict, List, Optional

class CompanyAnalyzer:
    """기업 분석 서비스 클래스"""
    
    def __init__(self):
        self.analyzer_name = "InsightMatch2 Analyzer"
    
    def analyze(self, homepage: str, email: str) -> Dict:
        """
        기업 분석 실행
        
        Args:
            homepage: 기업 홈페이지 URL
            email: 사용자 이메일
            
        Returns:
            Dict: 분석 결과
        """
        try:
            # 기업명 추출
            company_name = self.extract_company_name(homepage)
            
            # 기본 분석 결과 (더미 데이터)
            result = {
                'company': company_name,
                'homepage': homepage,
                'email': email,
                'summary': f'{company_name}의 공개자료 기반으로 보안·품질·환경 리스크가 식별되었습니다.',
                'risks': [
                    '정보보안 정책/절차 미흡',
                    '개인정보 처리방침 최신화 필요',
                    '공급망 리스크 모니터링 필요',
                    '경영 공시의 투명성 개선 필요',
                    '환경 규제 대응 체계 보완 필요'
                ],
                'certifications': [
                    'ISO 27001',
                    'ISO 9001',
                    'ISO 14001',
                    'ISO 27701',
                    'GDPR 컴플라이언스'
                ],
                'news': self._get_sample_news(company_name),
                'dart': self._get_sample_dart(company_name),
                'social': self._get_sample_social(company_name),
                'analysis_date': self._get_current_date(),
                'confidence_score': 0.85
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"분석 중 오류가 발생했습니다: {str(e)}")
    
    def extract_company_name(self, homepage_url: str) -> str:
        """
        홈페이지 URL에서 기업명 추출
        
        Args:
            homepage_url: 홈페이지 URL
            
        Returns:
            str: 추출된 기업명
        """
        try:
            parsed = urlparse(homepage_url)
            domain = parsed.netloc or parsed.path
            
            # www 제거
            domain = domain.replace('www.', '')
            
            # 도메인에서 기업명 추출
            parts = domain.split('.')
            if len(parts) >= 2:
                company_name = parts[0]
                # 특수문자 제거 및 대문자 변환
                company_name = re.sub(r'[^a-zA-Z0-9가-힣]', '', company_name)
                return company_name.capitalize()
            
            return domain.capitalize()
            
        except Exception:
            return 'Unknown Company'
    
    def _get_sample_news(self, company_name: str) -> List[Dict]:
        """샘플 뉴스 데이터 생성"""
        return [
            {
                'title': f'{company_name} 관련 보도 1',
                'url': f'https://news.example.com/{company_name}/1',
                'snippet': f'{company_name}의 최근 동향과 리스크 요인 분석 요약.',
                'source': 'news',
                'date': '2024-01-15'
            },
            {
                'title': f'{company_name} 관련 보도 2',
                'url': f'https://news.example.com/{company_name}/2',
                'snippet': f'{company_name}의 경영 현황과 향후 전망.',
                'source': 'news',
                'date': '2024-01-10'
            }
        ]
    
    def _get_sample_dart(self, company_name: str) -> List[Dict]:
        """샘플 DART 공시 데이터 생성"""
        return [
            {
                'title': '정기공시',
                'url': f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20240115000001',
                'snippet': f'{company_name} · 2024-01-15',
                'source': 'dart',
                'date': '2024-01-15'
            },
            {
                'title': '수시공시',
                'url': f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20240110000002',
                'snippet': f'{company_name} · 2024-01-10',
                'source': 'dart',
                'date': '2024-01-10'
            }
        ]
    
    def _get_sample_social(self, company_name: str) -> List[Dict]:
        """샘플 소셜 미디어 데이터 생성"""
        return [
            {
                'title': f'{company_name} 소셜 언급 1',
                'url': f'https://social.example.com/{company_name}/1',
                'snippet': '고객 만족/불만, 평판 이슈 요약.',
                'source': 'social',
                'date': '2024-01-12'
            }
        ]
    
    def _get_current_date(self) -> str:
        """현재 날짜 반환"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
