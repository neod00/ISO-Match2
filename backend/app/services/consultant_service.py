"""
컨설턴트 서비스
"""

from typing import Dict, List, Optional

class ConsultantService:
    """컨설턴트 서비스 클래스"""
    
    def __init__(self):
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
        
        # 새 컨설턴트 ID 생성
        new_id = max([c['id'] for c in self.consultants_db], default=0) + 1
        
        # 컨설턴트 정보 생성
        consultant = {
            'id': new_id,
            'name': data['name'],
            'email': data['email'],
            'industry': data['industry'],
            'region': data.get('region', '서울'),
            'certifications': data['certifications'],
            'rating': 0.0,
            'years': data.get('years', 0),
            'description': data.get('description', ''),
            'phone': data.get('phone', ''),
            'status': 'pending'  # 승인 대기 상태
        }
        
        # 데이터베이스에 추가 (실제로는 DB에 저장)
        self.consultants_db.append(consultant)
        
        return {
            'id': consultant['id'],
            'name': consultant['name'],
            'email': consultant['email'],
            'status': consultant['status']
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
