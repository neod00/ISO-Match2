"""
Analysis Data Model
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class Analysis:
    """분석 결과 모델"""
    id: Optional[int] = None
    company_id: Optional[int] = None
    company_name: str = ""
    homepage: str = ""
    email: str = ""
    summary: str = ""
    risks: List[str] = None
    certifications: List[str] = None
    news_data: List[Dict] = None
    dart_data: List[Dict] = None
    social_data: List[Dict] = None
    website_data: Optional[Dict] = None
    analysis_method: str = "AI (GPT-4o-mini)"
    confidence_score: float = 0.0
    crawl_status: str = "success"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.risks is None:
            self.risks = []
        if self.certifications is None:
            self.certifications = []
        if self.news_data is None:
            self.news_data = []
        if self.dart_data is None:
            self.dart_data = []
        if self.social_data is None:
            self.social_data = []
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'company_name': self.company_name,
            'homepage': self.homepage,
            'email': self.email,
            'summary': self.summary,
            'risks': self.risks,
            'certifications': self.certifications,
            'news_data': self.news_data,
            'dart_data': self.dart_data,
            'social_data': self.social_data,
            'website_data': self.website_data,
            'analysis_method': self.analysis_method,
            'confidence_score': self.confidence_score,
            'crawl_status': self.crawl_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Analysis':
        """딕셔너리에서 객체 생성"""
        return cls(
            id=data.get('id'),
            company_id=data.get('company_id'),
            company_name=data.get('company_name', ''),
            homepage=data.get('homepage', ''),
            email=data.get('email', ''),
            summary=data.get('summary', ''),
            risks=data.get('risks', []),
            certifications=data.get('certifications', []),
            news_data=data.get('news_data', []),
            dart_data=data.get('dart_data', []),
            social_data=data.get('social_data', []),
            website_data=data.get('website_data'),
            analysis_method=data.get('analysis_method', 'AI (GPT-4o-mini)'),
            confidence_score=data.get('confidence_score', 0.0),
            crawl_status=data.get('crawl_status', 'success'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
