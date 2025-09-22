"""
Consultant Data Model
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime

@dataclass
class Consultant:
    """컨설턴트 정보 모델"""
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
    industry: str = ""
    region: str = ""
    years_experience: int = 0
    certifications: List[str] = None
    description: Optional[str] = None
    rating: float = 0.0
    status: str = "pending"  # pending, active, inactive
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.certifications is None:
            self.certifications = []
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'industry': self.industry,
            'region': self.region,
            'years_experience': self.years_experience,
            'certifications': self.certifications,
            'description': self.description,
            'rating': self.rating,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Consultant':
        """딕셔너리에서 객체 생성"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            email=data.get('email', ''),
            phone=data.get('phone'),
            industry=data.get('industry', ''),
            region=data.get('region', ''),
            years_experience=data.get('years_experience', 0),
            certifications=data.get('certifications', []),
            description=data.get('description'),
            rating=data.get('rating', 0.0),
            status=data.get('status', 'pending'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
