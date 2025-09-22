"""
메인 크롤링 서비스
공개정보 수집 및 통합 관리
"""

import os
from typing import Dict, List, Optional
from .dart_service import DartService
from .news_service import NewsService
from .web_scraper import WebScraper

class CrawlerService:
    """크롤링 서비스 메인 클래스"""
    
    def __init__(self):
        self.dart_service = DartService()
        self.news_service = NewsService()
        self.web_scraper = WebScraper()
    
    def crawl_public_data(self, homepage: str, company_name: str = None) -> Dict:
        """
        공개정보 수집 및 통합
        
        Args:
            homepage: 기업 홈페이지 URL
            company_name: 기업명 (선택사항)
            
        Returns:
            Dict: 수집된 공개정보
        """
        try:
            # 기업명 추출
            if not company_name:
                company_name = self._extract_company_name(homepage)
            
            print(f"🔍 {company_name} 공개정보 수집 시작...")
            
            # 병렬로 데이터 수집
            results = {
                'company': company_name,
                'homepage': homepage,
                'news': [],
                'dart': [],
                'social': [],
                'website': {},
                'crawl_date': self._get_current_date(),
                'status': 'success'
            }
            
            # 뉴스 수집
            try:
                print("📰 뉴스 수집 중...")
                results['news'] = self.news_service.fetch_news(company_name, homepage)
                print(f"✅ 뉴스 {len(results['news'])}건 수집 완료")
            except Exception as e:
                print(f"❌ 뉴스 수집 실패: {str(e)}")
                results['news'] = []
            
            # DART 공시 수집
            try:
                print("📋 DART 공시 수집 중...")
                dart_key = os.getenv('DART_API_KEY')
                results['dart'] = self.dart_service.fetch_filings(company_name, dart_key)
                print(f"✅ DART 공시 {len(results['dart'])}건 수집 완료")
            except Exception as e:
                print(f"❌ DART 공시 수집 실패: {str(e)}")
                results['dart'] = []
            
            # 웹사이트 정보 수집
            try:
                print("🌐 웹사이트 정보 수집 중...")
                results['website'] = self.web_scraper.scrape_website(homepage)
                print("✅ 웹사이트 정보 수집 완료")
            except Exception as e:
                print(f"❌ 웹사이트 정보 수집 실패: {str(e)}")
                results['website'] = {}
            
            # 소셜 미디어 수집 (더미 데이터)
            try:
                print("📱 소셜 미디어 수집 중...")
                results['social'] = self._get_sample_social(company_name)
                print(f"✅ 소셜 미디어 {len(results['social'])}건 수집 완료")
            except Exception as e:
                print(f"❌ 소셜 미디어 수집 실패: {str(e)}")
                results['social'] = []
            
            print(f"🎉 {company_name} 공개정보 수집 완료!")
            return results
            
        except Exception as e:
            print(f"❌ 크롤링 중 오류 발생: {str(e)}")
            return {
                'company': company_name or 'Unknown',
                'homepage': homepage,
                'news': [],
                'dart': [],
                'social': [],
                'website': {},
                'crawl_date': self._get_current_date(),
                'status': 'error',
                'error': str(e)
            }
    
    def _extract_company_name(self, homepage: str) -> str:
        """홈페이지 URL에서 기업명 추출"""
        import re
        from urllib.parse import urlparse
        
        try:
            parsed = urlparse(homepage)
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
    
    def _get_sample_social(self, company_name: str) -> List[Dict]:
        """샘플 소셜 미디어 데이터 생성"""
        return [
            {
                'title': f'{company_name} 소셜 언급 1',
                'url': f'https://social.example.com/{company_name}/1',
                'snippet': '고객 만족/불만, 평판 이슈 요약.',
                'source': 'social',
                'date': '2024-01-12'
            },
            {
                'title': f'{company_name} 소셜 언급 2',
                'url': f'https://social.example.com/{company_name}/2',
                'snippet': '브랜드 인지도 및 고객 피드백.',
                'source': 'social',
                'date': '2024-01-10'
            }
        ]
    
    def _get_current_date(self) -> str:
        """현재 날짜 반환"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
