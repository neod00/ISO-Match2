"""
컨설턴트 서비스
"""

from typing import Dict, List, Optional
from .database_service import DatabaseService
from app.models.consultant import Consultant

class ConsultantService:
    """컨설턴트 서비스 클래스"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.consultants_db = self._initialize_consultants_db()
    
    def get_consultants(self, industry: str = '', certification: str = '', region: str = '') -> List[Dict]:
        """
        컨설턴트 목록 조회
        
        Args:
            industry: 업종 필터
            certification: 인증 필터
            region: 지역 필터
            
        Returns:
            List[Dict]: 필터링된 컨설턴트 목록
        """
        # 데이터베이스에서 조회 시도
        if self.db_service.is_available():
            try:
                consultants = self.db_service.get_consultants(industry, certification, region)
                return [consultant.to_dict() for consultant in consultants]
            except Exception as e:
                print(f"❌ 데이터베이스 조회 실패, 로컬 데이터 사용: {str(e)}")
        
        # 로컬 데이터 사용
        filtered_consultants = self.consultants_db.copy()
        
        # 업종 필터링
        if industry:
            filtered_consultants = [c for c in filtered_consultants if c['industry'] == industry]
        
        # 인증 필터링
        if certification:
            filtered_consultants = [c for c in filtered_consultants if certification in c['certifications']]
        
        # 지역 필터링
        if region:
            filtered_consultants = [c for c in filtered_consultants if c['region'] == region]
        
        return filtered_consultants
    
    def register_consultant(self, data: Dict) -> Dict:
        """
        컨설턴트 등록
        
        Args:
            data: 컨설턴트 정보
            
        Returns:
            Dict: 등록된 컨설턴트 정보
        """
        # 필수 필드 검증
        required_fields = ['name', 'email', 'industry', 'certifications']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f'{field} 필드가 필요합니다.')
        
        # 컨설턴트 객체 생성
        consultant = Consultant(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            industry=data['industry'],
            region=data.get('region', '서울'),
            years_experience=data.get('years', 0),
            certifications=data['certifications'],
            description=data.get('description', ''),
            status='pending'
        )
        
        # 데이터베이스에 저장 시도
        if self.db_service.is_available():
            try:
                saved_consultant = self.db_service.create_consultant(consultant)
                if saved_consultant:
                    return {
                        'id': saved_consultant.id,
                        'name': saved_consultant.name,
                        'email': saved_consultant.email,
                        'status': saved_consultant.status
                    }
            except Exception as e:
                print(f"❌ 데이터베이스 저장 실패, 로컬 저장: {str(e)}")
        
        # 로컬 저장 (폴백)
        new_id = max([c['id'] for c in self.consultants_db], default=0) + 1
        consultant_dict = consultant.to_dict()
        consultant_dict['id'] = new_id
        self.consultants_db.append(consultant_dict)
        
        return {
            'id': consultant_dict['id'],
            'name': consultant_dict['name'],
            'email': consultant_dict['email'],
            'status': consultant_dict['status']
        }
    
    def _initialize_consultants_db(self) -> List[Dict]:
        """컨설턴트 데이터베이스 초기화"""
        return [
            {
                'id': 1,
                'name': '김지훈',
                'email': 'kim@example.com',
                'rating': 4.9,
                'years': 10,
                'industry': 'IT',
                'region': '서울',
                'certifications': ['ISO 27001', 'ISO 9001'],
                'description': '정보보안 및 품질관리 전문가',
                'phone': '010-1234-5678',
                'status': 'active'
            },
            {
                'id': 2,
                'name': '이서연',
                'email': 'lee@example.com',
                'rating': 4.8,
                'years': 8,
                'industry': '제조',
                'region': '경기',
                'certifications': ['ISO 14001', 'ISO 9001'],
                'description': '환경경영 및 품질관리 전문가',
                'phone': '010-2345-6789',
                'status': 'active'
            },
            {
                'id': 3,
                'name': '박민수',
                'email': 'park@example.com',
                'rating': 4.7,
                'years': 12,
                'industry': '바이오/헬스',
                'region': '서울',
                'certifications': ['GDPR', 'ISO 27001', 'ISO 13485'],
                'description': '개인정보보호 및 의료기기 품질관리 전문가',
                'phone': '010-3456-7890',
                'status': 'active'
            },
            {
                'id': 4,
                'name': '최하늘',
                'email': 'choi@example.com',
                'rating': 4.6,
                'years': 7,
                'industry': '교육',
                'region': '부산',
                'certifications': ['ISO 9001', 'ISO 21001'],
                'description': '교육기관 품질관리 전문가',
                'phone': '010-4567-8901',
                'status': 'active'
            },
            {
                'id': 5,
                'name': '정유진',
                'email': 'jung@example.com',
                'rating': 4.8,
                'years': 9,
                'industry': 'IT',
                'region': '대구',
                'certifications': ['ISO 27001', 'ISO 20000'],
                'description': '정보보안 및 IT 서비스 관리 전문가',
                'phone': '010-5678-9012',
                'status': 'active'
            },
            {
                'id': 6,
                'name': '오세훈',
                'email': 'oh@example.com',
                'rating': 4.5,
                'years': 6,
                'industry': '제조',
                'region': '서울',
                'certifications': ['ISO 9001', 'ISO 14001', 'ISO 45001'],
                'description': '종합 품질·환경·안전 관리 전문가',
                'phone': '010-6789-0123',
                'status': 'active'
            }
        ]
