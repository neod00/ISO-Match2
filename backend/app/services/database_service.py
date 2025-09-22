"""
Database Service
데이터베이스 CRUD 작업을 담당하는 서비스
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from app.database.connection import db_connection
from app.models.company import Company
from app.models.consultant import Consultant
from app.models.analysis import Analysis

class DatabaseService:
    """데이터베이스 서비스 클래스"""
    
    def __init__(self):
        self.client = db_connection.get_client()
    
    def is_available(self) -> bool:
        """데이터베이스 사용 가능 여부 확인"""
        return db_connection.is_connected()
    
    # Company CRUD
    def create_company(self, company: Company) -> Optional[Company]:
        """기업 정보 생성"""
        if not self.is_available():
            return self._create_company_mock(company)
        
        try:
            data = company.to_dict()
            data.pop('id', None)  # ID는 자동 생성
            data.pop('created_at', None)
            data.pop('updated_at', None)
            
            result = self.client.table('companies').insert(data).execute()
            
            if result.data:
                return Company.from_dict(result.data[0])
            return None
            
        except Exception as e:
            print(f"❌ 기업 생성 실패: {str(e)}")
            return self._create_company_mock(company)
    
    def get_company_by_homepage(self, homepage: str) -> Optional[Company]:
        """홈페이지로 기업 조회"""
        if not self.is_available():
            return None
        
        try:
            result = self.client.table('companies').select('*').eq('homepage', homepage).execute()
            
            if result.data:
                return Company.from_dict(result.data[0])
            return None
            
        except Exception as e:
            print(f"❌ 기업 조회 실패: {str(e)}")
            return None
    
    def update_company(self, company: Company) -> Optional[Company]:
        """기업 정보 업데이트"""
        if not self.is_available():
            return company
        
        try:
            data = company.to_dict()
            data.pop('created_at', None)
            data['updated_at'] = datetime.now().isoformat()
            
            result = self.client.table('companies').update(data).eq('id', company.id).execute()
            
            if result.data:
                return Company.from_dict(result.data[0])
            return None
            
        except Exception as e:
            print(f"❌ 기업 업데이트 실패: {str(e)}")
            return company
    
    # Consultant CRUD
    def create_consultant(self, consultant: Consultant) -> Optional[Consultant]:
        """컨설턴트 생성"""
        if not self.is_available():
            return self._create_consultant_mock(consultant)
        
        try:
            data = consultant.to_dict()
            data.pop('id', None)
            data.pop('created_at', None)
            data.pop('updated_at', None)
            
            result = self.client.table('consultants').insert(data).execute()
            
            if result.data:
                return Consultant.from_dict(result.data[0])
            return None
            
        except Exception as e:
            print(f"❌ 컨설턴트 생성 실패: {str(e)}")
            return self._create_consultant_mock(consultant)
    
    def get_consultants(self, industry: str = '', certification: str = '', region: str = '') -> List[Consultant]:
        """컨설턴트 목록 조회"""
        if not self.is_available():
            return self._get_consultants_mock(industry, certification, region)
        
        try:
            query = self.client.table('consultants').select('*').eq('status', 'active')
            
            if industry:
                query = query.eq('industry', industry)
            if region:
                query = query.eq('region', region)
            if certification:
                query = query.contains('certifications', [certification])
            
            result = query.execute()
            
            return [Consultant.from_dict(item) for item in result.data]
            
        except Exception as e:
            print(f"❌ 컨설턴트 조회 실패: {str(e)}")
            return self._get_consultants_mock(industry, certification, region)
    
    def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]:
        """ID로 컨설턴트 조회"""
        if not self.is_available():
            return None
        
        try:
            result = self.client.table('consultants').select('*').eq('id', consultant_id).execute()
            
            if result.data:
                return Consultant.from_dict(result.data[0])
            return None
            
        except Exception as e:
            print(f"❌ 컨설턴트 조회 실패: {str(e)}")
            return None
    
    # Analysis CRUD
    def create_analysis(self, analysis: Analysis) -> Optional[Analysis]:
        """분석 결과 생성"""
        if not self.is_available():
            return self._create_analysis_mock(analysis)
        
        try:
            data = analysis.to_dict()
            data.pop('id', None)
            data.pop('created_at', None)
            data.pop('updated_at', None)
            
            result = self.client.table('analyses').insert(data).execute()
            
            if result.data:
                return Analysis.from_dict(result.data[0])
            return None
            
        except Exception as e:
            print(f"❌ 분석 결과 생성 실패: {str(e)}")
            return self._create_analysis_mock(analysis)
    
    def get_analyses_by_company(self, company_id: int) -> List[Analysis]:
        """기업별 분석 결과 조회"""
        if not self.is_available():
            return []
        
        try:
            result = self.client.table('analyses').select('*').eq('company_id', company_id).order('created_at', desc=True).execute()
            
            return [Analysis.from_dict(item) for item in result.data]
            
        except Exception as e:
            print(f"❌ 분석 결과 조회 실패: {str(e)}")
            return []
    
    def get_latest_analysis(self, company_name: str) -> Optional[Analysis]:
        """최신 분석 결과 조회"""
        if not self.is_available():
            return None
        
        try:
            result = self.client.table('analyses').select('*').eq('company_name', company_name).order('created_at', desc=True).limit(1).execute()
            
            if result.data:
                return Analysis.from_dict(result.data[0])
            return None
            
        except Exception as e:
            print(f"❌ 최신 분석 결과 조회 실패: {str(e)}")
            return None
    
    # Mock methods for when database is not available
    def _create_company_mock(self, company: Company) -> Company:
        """기업 생성 모의 구현"""
        company.id = 1
        company.created_at = datetime.now()
        company.updated_at = datetime.now()
        return company
    
    def _create_consultant_mock(self, consultant: Consultant) -> Consultant:
        """컨설턴트 생성 모의 구현"""
        consultant.id = 1
        consultant.created_at = datetime.now()
        consultant.updated_at = datetime.now()
        return consultant
    
    def _create_analysis_mock(self, analysis: Analysis) -> Analysis:
        """분석 결과 생성 모의 구현"""
        analysis.id = 1
        analysis.created_at = datetime.now()
        analysis.updated_at = datetime.now()
        return analysis
    
    def _get_consultants_mock(self, industry: str = '', certification: str = '', region: str = '') -> List[Consultant]:
        """컨설턴트 목록 조회 모의 구현"""
        mock_consultants = [
            Consultant(
                id=1, name="김지훈", email="kim@example.com", industry="IT", region="서울",
                years_experience=10, certifications=["ISO 27001", "ISO 9001"], rating=4.9, status="active"
            ),
            Consultant(
                id=2, name="이서연", email="lee@example.com", industry="제조", region="경기",
                years_experience=8, certifications=["ISO 14001"], rating=4.8, status="active"
            ),
            Consultant(
                id=3, name="박민수", email="park@example.com", industry="바이오/헬스", region="서울",
                years_experience=12, certifications=["GDPR", "ISO 27001"], rating=4.7, status="active"
            )
        ]
        
        # 필터링 적용
        filtered = mock_consultants
        if industry:
            filtered = [c for c in filtered if c.industry == industry]
        if region:
            filtered = [c for c in filtered if c.region == region]
        if certification:
            filtered = [c for c in filtered if certification in c.certifications]
        
        return filtered
