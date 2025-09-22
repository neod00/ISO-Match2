"""
뉴스 크롤링 서비스
Google News RSS 및 기타 뉴스 소스 수집
"""

import re
import time
from typing import Dict, List, Optional
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

class NewsService:
    """뉴스 크롤링 서비스"""
    
    def __init__(self):
        self.google_news_base = "https://news.google.com/rss/search"
        self.timeout = 10
        self.max_retries = 3
    
    def fetch_news(self, company_name: str, homepage: str = None, limit: int = 10) -> List[Dict]:
        """
        뉴스 데이터 수집
        
        Args:
            company_name: 기업명
            homepage: 홈페이지 URL (선택사항)
            limit: 수집할 뉴스 수 제한
            
        Returns:
            List[Dict]: 뉴스 데이터 목록
        """
        try:
            print(f"📰 {company_name} 뉴스 수집 시작...")
            
            # 검색 쿼리 생성
            queries = self._build_search_queries(company_name, homepage)
            
            collected_news = []
            seen_urls = set()
            
            # 각 쿼리로 뉴스 수집
            for query in queries:
                if len(collected_news) >= limit:
                    break
                
                try:
                    news_items = self._fetch_google_news(query, limit - len(collected_news))
                    
                    for item in news_items:
                        if item['url'] not in seen_urls:
                            seen_urls.add(item['url'])
                            collected_news.append(item)
                            
                        if len(collected_news) >= limit:
                            break
                    
                    # 요청 간 지연
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"⚠️ 쿼리 '{query}' 뉴스 수집 실패: {str(e)}")
                    continue
            
            print(f"✅ 뉴스 {len(collected_news)}건 수집 완료")
            return collected_news[:limit]
            
        except Exception as e:
            print(f"❌ 뉴스 수집 중 오류: {str(e)}")
            return self._get_sample_news(company_name, limit)
    
    def _build_search_queries(self, company_name: str, homepage: str = None) -> List[str]:
        """검색 쿼리 생성"""
        queries = []
        
        # 기업명 추가
        if company_name:
            queries.append(company_name)
            if len(company_name) > 3:
                queries.append(f'"{company_name}"')
        
        # 홈페이지에서 도메인 추출
        if homepage:
            domain_match = re.search(r'https?://([^/]+)', homepage)
            if domain_match:
                domain = domain_match.group(1)
                # www 제거
                domain = domain.replace('www.', '')
                # 도메인에서 토큰 추출
                parts = domain.split('.')
                if parts and parts[0].lower() not in ['www', 'm']:
                    queries.append(parts[0])
        
        # 중복 제거
        unique_queries = []
        seen = set()
        for query in queries:
            if query not in seen:
                seen.add(query)
                unique_queries.append(query)
        
        return unique_queries
    
    def _fetch_google_news(self, query: str, limit: int) -> List[Dict]:
        """Google News RSS에서 뉴스 수집"""
        try:
            # Google News RSS URL 생성
            url = f"{self.google_news_base}?q={quote_plus(query)}&hl=ko&gl=KR&ceid=KR:ko"
            
            response = requests.get(url, timeout=self.timeout)
            if response.status_code != 200:
                print(f"⚠️ Google News RSS 응답 오류: {response.status_code}")
                return []
            
            # XML 파싱
            soup = BeautifulSoup(response.content, 'xml')
            news_items = []
            
            for item in soup.find_all('item')[:limit]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                pub_date_elem = item.find('pubDate')
                
                title = title_elem.text.strip() if title_elem else ""
                link = link_elem.text.strip() if link_elem else ""
                description = desc_elem.text.strip() if desc_elem else ""
                pub_date = pub_date_elem.text.strip() if pub_date_elem else ""
                
                if title and link:
                    news_item = {
                        'title': title,
                        'url': link,
                        'snippet': description,
                        'source': 'news',
                        'date': pub_date,
                        'query': query
                    }
                    news_items.append(news_item)
            
            return news_items
            
        except Exception as e:
            print(f"❌ Google News 수집 실패: {str(e)}")
            return []
    
    def _get_sample_news(self, company_name: str, limit: int) -> List[Dict]:
        """샘플 뉴스 데이터 생성"""
        return [
            {
                'title': f'{company_name} 관련 보도 1',
                'url': f'https://news.example.com/{company_name}/1',
                'snippet': f'{company_name}의 최근 동향과 리스크 요인 분석 요약.',
                'source': 'news',
                'date': '2024-01-15',
                'query': company_name
            },
            {
                'title': f'{company_name} 관련 보도 2',
                'url': f'https://news.example.com/{company_name}/2',
                'snippet': f'{company_name}의 경영 현황과 향후 전망.',
                'source': 'news',
                'date': '2024-01-10',
                'query': company_name
            },
            {
                'title': f'{company_name} 관련 보도 3',
                'url': f'https://news.example.com/{company_name}/3',
                'snippet': f'{company_name}의 시장 동향과 경쟁사 분석.',
                'source': 'news',
                'date': '2024-01-05',
                'query': company_name
            }
        ][:limit]
