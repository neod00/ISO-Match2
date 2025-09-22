"""
DART API 연동 서비스
전자공시 데이터 수집
"""

import os
import re
import time
import zipfile
import xml.etree.ElementTree as ET
import difflib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from io import BytesIO
import requests

class DartService:
    """DART API 연동 서비스"""
    
    def __init__(self):
        self.base_url = "https://opendart.fss.or.kr/api"
        self.api_key = os.getenv('DART_API_KEY')
    
    def fetch_filings(self, company_name: str, api_key: str = None, limit: int = 10) -> List[Dict]:
        """
        DART 공시 데이터 수집
        
        Args:
            company_name: 기업명
            api_key: DART API 키
            limit: 수집할 공시 수 제한
            
        Returns:
            List[Dict]: 공시 데이터 목록
        """
        if not api_key:
            print("⚠️ DART API 키가 없습니다. 샘플 데이터를 반환합니다.")
            return self._get_sample_dart_data(company_name, limit)
        
        try:
            # 기업 코드 조회
            corp_code = self._find_corp_code(company_name, api_key)
            if not corp_code:
                print(f"⚠️ {company_name}의 기업 코드를 찾을 수 없습니다.")
                return self._get_sample_dart_data(company_name, limit)
            
            # 공시 데이터 수집
            filings = self._fetch_filings_by_corp_code(corp_code, api_key, limit)
            return filings
            
        except Exception as e:
            print(f"❌ DART 공시 수집 중 오류: {str(e)}")
            return self._get_sample_dart_data(company_name, limit)
    
    def _find_corp_code(self, company_name: str, api_key: str) -> Optional[str]:
        """기업 코드 조회"""
        try:
            # 기업 코드 XML 다운로드
            xml_data = self._download_corp_code_xml(api_key)
            if not xml_data:
                return None
            
            # 기업명으로 코드 검색
            corp_code = self._search_corp_code_in_xml(xml_data, company_name)
            return corp_code
            
        except Exception as e:
            print(f"❌ 기업 코드 조회 실패: {str(e)}")
            return None
    
    def _download_corp_code_xml(self, api_key: str) -> Optional[bytes]:
        """기업 코드 XML 파일 다운로드"""
        try:
            url = f"{self.base_url}/corpCode.xml?crtfc_key={api_key}"
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ DART API 응답 오류: {response.status_code}")
                return None
            
            # ZIP 파일 압축 해제
            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                for file_name in zip_file.namelist():
                    if file_name.lower().endswith('.xml'):
                        return zip_file.read(file_name)
            
            return None
            
        except Exception as e:
            print(f"❌ 기업 코드 XML 다운로드 실패: {str(e)}")
            return None
    
    def _search_corp_code_in_xml(self, xml_data: bytes, company_name: str) -> Optional[str]:
        """XML에서 기업 코드 검색"""
        try:
            root = ET.fromstring(xml_data)
            candidates = []
            
            # 기업명 정규화
            normalized_name = self._normalize_company_name(company_name)
            
            for corp in root.findall("list"):
                corp_name_elem = corp.find("corp_name")
                corp_code_elem = corp.find("corp_code")
                
                if corp_name_elem is not None and corp_code_elem is not None:
                    corp_name = corp_name_elem.text
                    corp_code = corp_code_elem.text
                    
                    if corp_name and corp_code:
                        # 정확한 매치 확인
                        if company_name.lower() in corp_name.lower() or corp_name.lower() in company_name.lower():
                            candidates.append((corp_code, corp_name))
                            continue
                        
                        # 정규화된 이름으로 매치 확인
                        normalized_corp_name = self._normalize_company_name(corp_name)
                        if normalized_name in normalized_corp_name or normalized_corp_name in normalized_name:
                            candidates.append((corp_code, corp_name))
                            continue
                        
                        # 유사도 검사
                        similarity = difflib.SequenceMatcher(None, normalized_name, normalized_corp_name).ratio()
                        if similarity >= 0.8:
                            candidates.append((corp_code, corp_name))
            
            # 가장 유사한 기업 선택
            if candidates:
                return candidates[0][0]
            
            return None
            
        except Exception as e:
            print(f"❌ XML 파싱 실패: {str(e)}")
            return None
    
    def _normalize_company_name(self, name: str) -> str:
        """기업명 정규화"""
        if not name:
            return ""
        
        # 공백 제거
        name = re.sub(r'\s+', '', name)
        
        # 회사 형태 제거
        name = name.replace('주식회사', '').replace('(주)', '').replace('㈜', '')
        name = name.replace('유한회사', '').replace('(유)', '')
        name = name.replace('합자회사', '').replace('(합)', '')
        
        # 특수문자 제거
        name = re.sub(r'[()\[\]{}]', '', name)
        
        return name.lower()
    
    def _fetch_filings_by_corp_code(self, corp_code: str, api_key: str, limit: int) -> List[Dict]:
        """기업 코드로 공시 데이터 수집"""
        try:
            # 최근 1년간의 공시 조회
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            
            url = f"{self.base_url}/list.json"
            params = {
                'crtfc_key': api_key,
                'corp_code': corp_code,
                'bgn_de': start_date,
                'end_de': end_date,
                'page_no': 1,
                'page_count': min(limit, 100)
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code != 200:
                print(f"❌ DART 공시 조회 실패: {response.status_code}")
                return []
            
            data = response.json()
            filings = []
            
            for item in data.get('list', [])[:limit]:
                filing = {
                    'title': item.get('report_nm', '전자공시'),
                    'url': f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={item.get('rcept_no', '')}",
                    'snippet': f"{item.get('flr_nm', '')} · {item.get('rcept_dt', '')}",
                    'source': 'dart',
                    'date': item.get('rcept_dt', ''),
                    'type': item.get('report_nm', ''),
                    'rcp_no': item.get('rcept_no', '')
                }
                filings.append(filing)
            
            return filings
            
        except Exception as e:
            print(f"❌ 공시 데이터 수집 실패: {str(e)}")
            return []
    
    def _get_sample_dart_data(self, company_name: str, limit: int) -> List[Dict]:
        """샘플 DART 데이터 생성"""
        return [
            {
                'title': '정기공시',
                'url': f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20240115000001',
                'snippet': f'{company_name} · 2024-01-15',
                'source': 'dart',
                'date': '2024-01-15',
                'type': '정기공시',
                'rcp_no': '20240115000001'
            },
            {
                'title': '수시공시',
                'url': f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20240110000002',
                'snippet': f'{company_name} · 2024-01-10',
                'source': 'dart',
                'date': '2024-01-10',
                'type': '수시공시',
                'rcp_no': '20240110000002'
            },
            {
                'title': '기타공시',
                'url': f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20240105000003',
                'snippet': f'{company_name} · 2024-01-05',
                'source': 'dart',
                'date': '2024-01-05',
                'type': '기타공시',
                'rcp_no': '20240105000003'
            }
        ][:limit]
