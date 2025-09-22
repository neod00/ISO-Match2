"""
Company Data Model
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class Company:
    """기업 정보 모델"""
    id: Optional[int] = None
    name: str = ""
    homepage: str = ""
    email: str = ""
    industry: Optional[str] = None
    size: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None
    website_info: Optional[Dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'name': self.name,
            'homepage': self.homepage,
            'email': self.email,
            'industry': self.industry,
            'size': self.size,
            'region': self.region,
            'description': self.description,
            'website_info': self.website_info,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Company':
        """딕셔너리에서 객체 생성"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            homepage=data.get('homepage', ''),
            email=data.get('email', ''),
            industry=data.get('industry'),
            size=data.get('size'),
            region=data.get('region'),
            description=data.get('description'),
            website_info=data.get('website_info'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
