"""
웹사이트 크롤링 서비스
홈페이지 정보 수집 및 분석
"""

import re
import time
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

class WebScraper:
    """웹사이트 크롤링 서비스"""
    
    def __init__(self):
        self.timeout = 15
        self.max_retries = 3
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    def scrape_website(self, url: str) -> Dict:
        """
        웹사이트 정보 수집
        
        Args:
            url: 웹사이트 URL
            
        Returns:
            Dict: 수집된 웹사이트 정보
        """
        try:
            print(f"🌐 {url} 웹사이트 정보 수집 시작...")
            
            # 웹페이지 내용 수집
            content = self._fetch_webpage(url)
            if not content:
                return self._get_sample_website_data(url)
            
            # 정보 추출
            website_info = {
                'url': url,
                'title': self._extract_title(content),
                'description': self._extract_description(content),
                'keywords': self._extract_keywords(content),
                'company_info': self._extract_company_info(content),
                'contact_info': self._extract_contact_info(content),
                'social_links': self._extract_social_links(content),
                'last_updated': self._get_current_date(),
                'status': 'success'
            }
            
            print("✅ 웹사이트 정보 수집 완료")
            return website_info
            
        except Exception as e:
            print(f"❌ 웹사이트 수집 중 오류: {str(e)}")
            return self._get_sample_website_data(url)
    
    def _fetch_webpage(self, url: str) -> Optional[BeautifulSoup]:
        """웹페이지 내용 수집"""
        for attempt in range(self.max_retries):
            try:
                headers = {
                    'User-Agent': self.user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }
                
                response = requests.get(url, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                
                # 인코딩 감지
                if response.encoding.lower() in ['iso-8859-1', 'windows-1252']:
                    response.encoding = response.apparent_encoding
                
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup
                
            except Exception as e:
                print(f"⚠️ 웹페이지 수집 시도 {attempt + 1} 실패: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 지수 백오프
                else:
                    return None
        
        return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """페이지 제목 추출"""
        try:
            # title 태그에서 추출
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()
                # 제목이 너무 길면 잘라내기
                if len(title) > 100:
                    title = title[:100] + "..."
                return title
            
            # h1 태그에서 추출
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.get_text().strip()[:100]
            
            return "제목 없음"
            
        except Exception:
            return "제목 추출 실패"
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """페이지 설명 추출"""
        try:
            # meta description에서 추출
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                return meta_desc.get('content').strip()[:200]
            
            # 첫 번째 p 태그에서 추출
            first_p = soup.find('p')
            if first_p:
                desc = first_p.get_text().strip()
                if len(desc) > 200:
                    desc = desc[:200] + "..."
                return desc
            
            return "설명 없음"
            
        except Exception:
            return "설명 추출 실패"
    
    def _extract_keywords(self, soup: BeautifulSoup) -> List[str]:
        """키워드 추출"""
        try:
            keywords = []
            
            # meta keywords에서 추출
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords and meta_keywords.get('content'):
                keywords_text = meta_keywords.get('content')
                keywords.extend([kw.strip() for kw in keywords_text.split(',') if kw.strip()])
            
            # h1, h2, h3 태그에서 키워드 추출
            for tag in soup.find_all(['h1', 'h2', 'h3']):
                text = tag.get_text().strip()
                if text and len(text) < 50:  # 너무 긴 텍스트 제외
                    keywords.append(text)
            
            # 중복 제거 및 상위 10개만 반환
            unique_keywords = list(dict.fromkeys(keywords))[:10]
            return unique_keywords
            
        except Exception:
            return []
    
    def _extract_company_info(self, soup: BeautifulSoup) -> Dict:
        """회사 정보 추출"""
        try:
            company_info = {}
            text = soup.get_text()
            
            # 회사명 패턴 검색
            company_patterns = [
                r'([가-힣A-Za-z&·ㆍ\-\s]{2,}?)\s*(주식회사|㈜)',
                r'(주식회사|㈜)\s*([가-힣A-Za-z&·ㆍ\-\s]{2,})',
                r'([가-힣A-Za-z&·ㆍ\-\s]{2,}?)\s*(유한회사|\(유\))',
                r'(유한회사|\(유\))\s*([가-힣A-Za-z&·ㆍ\-\s]{2,})'
            ]
            
            for pattern in company_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    company_info['legal_name'] = matches[0][0] if matches[0][0] else matches[0][1]
                    break
            
            # 사업자등록번호 검색
            biz_pattern = r'사업자등록번호\s*:?\s*(\d{3}-\d{2}-\d{5})'
            biz_match = re.search(biz_pattern, text)
            if biz_match:
                company_info['business_number'] = biz_match.group(1)
            
            # 대표자명 검색
            ceo_patterns = [
                r'대표자\s*:?\s*([가-힣]{2,4})',
                r'대표이사\s*:?\s*([가-힣]{2,4})',
                r'CEO\s*:?\s*([가-힣A-Za-z\s]{2,20})'
            ]
            
            for pattern in ceo_patterns:
                ceo_match = re.search(pattern, text)
                if ceo_match:
                    company_info['ceo'] = ceo_match.group(1).strip()
                    break
            
            return company_info
            
        except Exception:
            return {}
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        """연락처 정보 추출"""
        try:
            contact_info = {}
            text = soup.get_text()
            
            # 전화번호 패턴
            phone_patterns = [
                r'(\d{2,3}-\d{3,4}-\d{4})',
                r'(\d{2,3}\s\d{3,4}\s\d{4})',
                r'(\+82\s?\d{2,3}\s?\d{3,4}\s?\d{4})'
            ]
            
            phones = []
            for pattern in phone_patterns:
                matches = re.findall(pattern, text)
                phones.extend(matches)
            
            if phones:
                contact_info['phones'] = list(set(phones))[:3]  # 중복 제거, 최대 3개
            
            # 이메일 패턴
            email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            emails = re.findall(email_pattern, text)
            if emails:
                contact_info['emails'] = list(set(emails))[:3]  # 중복 제거, 최대 3개
            
            # 주소 패턴 (간단한 패턴)
            address_patterns = [
                r'([가-힣]{2,4}(?:시|도)\s[가-힣]{2,4}(?:구|군|시)\s[가-힣\s\d\-]+)',
                r'([가-힣]{2,4}(?:구|군|시)\s[가-힣\s\d\-]+)'
            ]
            
            addresses = []
            for pattern in address_patterns:
                matches = re.findall(pattern, text)
                addresses.extend(matches)
            
            if addresses:
                contact_info['addresses'] = list(set(addresses))[:2]  # 중복 제거, 최대 2개
            
            return contact_info
            
        except Exception:
            return {}
    
    def _extract_social_links(self, soup: BeautifulSoup) -> List[str]:
        """소셜 미디어 링크 추출"""
        try:
            social_links = []
            social_patterns = {
                'facebook': r'facebook\.com/[^/\s]+',
                'twitter': r'twitter\.com/[^/\s]+',
                'instagram': r'instagram\.com/[^/\s]+',
                'linkedin': r'linkedin\.com/[^/\s]+',
                'youtube': r'youtube\.com/[^/\s]+'
            }
            
            # 모든 링크 검색
            for link in soup.find_all('a', href=True):
                href = link['href']
                for platform, pattern in social_patterns.items():
                    if re.search(pattern, href):
                        social_links.append(href)
                        break
            
            return list(set(social_links))[:5]  # 중복 제거, 최대 5개
            
        except Exception:
            return []
    
    def _get_sample_website_data(self, url: str) -> Dict:
        """샘플 웹사이트 데이터 생성"""
        return {
            'url': url,
            'title': '샘플 웹사이트',
            'description': '웹사이트 정보 수집 중 오류가 발생했습니다.',
            'keywords': ['샘플', '웹사이트'],
            'company_info': {
                'legal_name': '샘플 회사',
                'business_number': '123-45-67890',
                'ceo': '홍길동'
            },
            'contact_info': {
                'phones': ['02-1234-5678'],
                'emails': ['info@example.com'],
                'addresses': ['서울특별시 강남구']
            },
            'social_links': [],
            'last_updated': self._get_current_date(),
            'status': 'error'
        }
    
    def _get_current_date(self) -> str:
        """현재 날짜 반환"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
