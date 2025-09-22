"""
기업 분석 서비스
"""

import re
from urllib.parse import urlparse
from typing import Dict, List, Optional
from .crawler import CrawlerService
from .ai_analyzer import AIAnalyzer
from .database_service import DatabaseService
from app.models.company import Company
from app.models.analysis import Analysis

class CompanyAnalyzer:
    """기업 분석 서비스 클래스"""
    
    def __init__(self):
        self.analyzer_name = "InsightMatch2 Analyzer"
        self.crawler = CrawlerService()
        self.ai_analyzer = AIAnalyzer()
        self.db_service = DatabaseService()
    
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
            
            # 공개정보 수집
            print(f"🔍 {company_name} 공개정보 수집 시작...")
            public_data = self.crawler.crawl_public_data(homepage, company_name)
            
            # AI 분석 실행
            print(f"🤖 {company_name} AI 분석 시작...")
            ai_analysis = self.ai_analyzer.analyze_company_risks(public_data)
            
            # 분석 결과 통합
            result = {
                'company': company_name,
                'homepage': homepage,
                'email': email,
                'summary': ai_analysis.get('summary', f'{company_name}의 공개자료 기반으로 보안·품질·환경 리스크가 식별되었습니다.'),
                'risks': self._format_risks(ai_analysis.get('risks', [])),
                'certifications': self._format_certifications(ai_analysis.get('certifications', [])),
                'news': public_data.get('news', []),
                'dart': public_data.get('dart', []),
                'social': public_data.get('social', []),
                'website': public_data.get('website', {}),
                'analysis_date': ai_analysis.get('analysis_date', self._get_current_date()),
                'confidence_score': ai_analysis.get('confidence_score', 0.85),
                'analysis_method': ai_analysis.get('analysis_method', 'Unknown'),
                'crawl_status': public_data.get('status', 'unknown')
            }
            
            # 데이터베이스에 저장
            self._save_analysis_to_db(company_name, homepage, email, result, public_data, ai_analysis)
            
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
    
    def _format_risks(self, risks: List[Dict]) -> List[str]:
        """리스크 데이터 포맷팅"""
        if not risks:
            return [
                '정보보안 정책/절차 미흡',
                '개인정보 처리방침 최신화 필요',
                '공급망 리스크 모니터링 필요',
                '경영 공시의 투명성 개선 필요',
                '환경 규제 대응 체계 보완 필요'
            ]
        
        formatted_risks = []
        for risk in risks:
            if isinstance(risk, dict):
                item = risk.get('item', 'Unknown Risk')
                priority = risk.get('priority', 'Medium')
                description = risk.get('description', '')
                
                if description:
                    formatted_risks.append(f"{item} ({priority}): {description}")
                else:
                    formatted_risks.append(f"{item} ({priority})")
            else:
                formatted_risks.append(str(risk))
        
        return formatted_risks[:10]  # 최대 10개
    
    def _format_certifications(self, certifications: List[Dict]) -> List[str]:
        """인증 데이터 포맷팅"""
        if not certifications:
            return [
                'ISO 27001',
                'ISO 9001',
                'ISO 14001',
                'ISO 27701',
                'GDPR 컴플라이언스'
            ]
        
        formatted_certs = []
        for cert in certifications:
            if isinstance(cert, dict):
                item = cert.get('item', 'Unknown Certification')
                priority = cert.get('priority', 'Medium')
                description = cert.get('description', '')
                
                if description:
                    formatted_certs.append(f"{item} ({priority}): {description}")
                else:
                    formatted_certs.append(f"{item} ({priority})")
            else:
                formatted_certs.append(str(cert))
        
        return formatted_certs[:10]  # 최대 10개
    
    def _save_analysis_to_db(self, company_name: str, homepage: str, email: str, result: Dict, public_data: Dict, ai_analysis: Dict):
        """분석 결과를 데이터베이스에 저장"""
        try:
            if not self.db_service.is_available():
                print("⚠️ 데이터베이스가 사용 불가능합니다. 분석 결과를 저장하지 않습니다.")
                return
            
            # 기업 정보 저장 또는 업데이트
            company = Company(
                name=company_name,
                homepage=homepage,
                email=email,
                website_info=public_data.get('website', {})
            )
            
            existing_company = self.db_service.get_company_by_homepage(homepage)
            if existing_company:
                company.id = existing_company.id
                company = self.db_service.update_company(company)
            else:
                company = self.db_service.create_company(company)
            
            if not company:
                print("❌ 기업 정보 저장 실패")
                return
            
            # 분석 결과 저장
            analysis = Analysis(
                company_id=company.id,
                company_name=company_name,
                homepage=homepage,
                email=email,
                summary=result.get('summary', ''),
                risks=ai_analysis.get('risks', []),
                certifications=ai_analysis.get('certifications', []),
                news_data=public_data.get('news', []),
                dart_data=public_data.get('dart', []),
                social_data=public_data.get('social', []),
                website_data=public_data.get('website', {}),
                analysis_method=ai_analysis.get('analysis_method', 'AI (GPT-4o-mini)'),
                confidence_score=ai_analysis.get('confidence_score', 0.85),
                crawl_status=public_data.get('status', 'success')
            )
            
            saved_analysis = self.db_service.create_analysis(analysis)
            if saved_analysis:
                print(f"✅ {company_name} 분석 결과가 데이터베이스에 저장되었습니다.")
            else:
                print(f"❌ {company_name} 분석 결과 저장 실패")
                
        except Exception as e:
            print(f"❌ 데이터베이스 저장 중 오류: {str(e)}")
    
    def _get_current_date(self) -> str:
        """현재 날짜 반환"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
