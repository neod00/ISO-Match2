"""
컨설턴트 매칭 서비스
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from app.models.consultant import Consultant
from app.models.analysis import Analysis
from .database_service import DatabaseService

@dataclass
class MatchResult:
    """매칭 결과 모델"""
    consultant: Consultant
    match_score: float
    reasons: List[str]
    industry_match: bool
    certification_matches: List[str]
    region_match: bool
    experience_level: str

class MatchingService:
    """컨설턴트 매칭 서비스 클래스"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        
        # 매칭 가중치 설정
        self.weights = {
            'industry': 0.3,      # 업종 일치
            'certification': 0.4, # 인증 일치
            'region': 0.1,        # 지역 일치
            'experience': 0.2     # 경력 수준
        }
        
        # 경력 수준별 점수
        self.experience_scores = {
            'junior': 0.6,    # 0-3년
            'mid': 0.8,       # 4-7년
            'senior': 1.0,    # 8-12년
            'expert': 1.2     # 13년 이상
        }
    
    def find_matches(self, analysis: Analysis, limit: int = 5) -> List[MatchResult]:
        """
        분석 결과를 바탕으로 컨설턴트 매칭
        
        Args:
            analysis: 분석 결과
            limit: 반환할 매칭 수
            
        Returns:
            List[MatchResult]: 매칭된 컨설턴트 목록
        """
        try:
            # 모든 활성 컨설턴트 조회
            consultants = self.db_service.get_consultants()
            
            if not consultants:
                print("⚠️ 매칭할 컨설턴트가 없습니다.")
                return []
            
            # 매칭 점수 계산
            matches = []
            for consultant in consultants:
                match_result = self._calculate_match_score(analysis, consultant)
                if match_result.match_score > 0.3:  # 최소 30% 이상 매칭
                    matches.append(match_result)
            
            # 점수순으로 정렬
            matches.sort(key=lambda x: x.match_score, reverse=True)
            
            return matches[:limit]
            
        except Exception as e:
            print(f"❌ 매칭 중 오류 발생: {str(e)}")
            return []
    
    def _calculate_match_score(self, analysis: Analysis, consultant: Consultant) -> MatchResult:
        """개별 컨설턴트와의 매칭 점수 계산"""
        
        # 업종 매칭 (분석에서 추론하거나 기본값 사용)
        industry_match = self._check_industry_match(analysis, consultant)
        industry_score = 1.0 if industry_match else 0.0
        
        # 인증 매칭
        certification_matches = self._check_certification_match(analysis, consultant)
        certification_score = len(certification_matches) / max(len(analysis.certifications), 1)
        
        # 지역 매칭 (선택사항)
        region_match = self._check_region_match(analysis, consultant)
        region_score = 1.0 if region_match else 0.5  # 지역 불일치도 부분 점수
        
        # 경력 수준 매칭
        experience_level = self._get_experience_level(consultant.years_experience)
        experience_score = self.experience_scores.get(experience_level, 0.8)
        
        # 가중 평균 점수 계산
        total_score = (
            industry_score * self.weights['industry'] +
            certification_score * self.weights['certification'] +
            region_score * self.weights['region'] +
            experience_score * self.weights['experience']
        )
        
        # 매칭 이유 생성
        reasons = self._generate_match_reasons(
            industry_match, certification_matches, region_match, experience_level
        )
        
        return MatchResult(
            consultant=consultant,
            match_score=min(total_score, 1.0),  # 최대 1.0
            reasons=reasons,
            industry_match=industry_match,
            certification_matches=certification_matches,
            region_match=region_match,
            experience_level=experience_level
        )
    
    def _check_industry_match(self, analysis: Analysis, consultant: Consultant) -> bool:
        """업종 매칭 확인"""
        # 분석 결과에서 업종을 추론하거나 기본 매칭
        # 실제로는 AI 분석 결과에서 업종을 추출해야 함
        return True  # 일단 모든 업종 매칭
    
    def _check_certification_match(self, analysis: Analysis, consultant: Consultant) -> List[str]:
        """인증 매칭 확인"""
        matches = []
        analysis_certs = set(analysis.certifications)
        consultant_certs = set(consultant.certifications)
        
        for cert in analysis_certs:
            if cert in consultant_certs:
                matches.append(cert)
        
        return matches
    
    def _check_region_match(self, analysis: Analysis, consultant: Consultant) -> bool:
        """지역 매칭 확인"""
        # 분석 결과에서 지역을 추론하거나 기본 매칭
        return True  # 일단 모든 지역 매칭
    
    def _get_experience_level(self, years: int) -> str:
        """경력 수준 분류"""
        if years <= 3:
            return 'junior'
        elif years <= 7:
            return 'mid'
        elif years <= 12:
            return 'senior'
        else:
            return 'expert'
    
    def _generate_match_reasons(self, industry_match: bool, certification_matches: List[str], 
                               region_match: bool, experience_level: str) -> List[str]:
        """매칭 이유 생성"""
        reasons = []
        
        if industry_match:
            reasons.append("업종 일치")
        
        if certification_matches:
            reasons.append(f"인증 일치: {', '.join(certification_matches)}")
        
        if region_match:
            reasons.append("지역 일치")
        
        if experience_level:
            reasons.append(f"경력 수준: {experience_level}")
        
        return reasons
    
    def get_match_summary(self, matches: List[MatchResult]) -> Dict:
        """매칭 결과 요약"""
        if not matches:
            return {
                'total_matches': 0,
                'average_score': 0.0,
                'top_match': None
            }
        
        total_matches = len(matches)
        average_score = sum(match.match_score for match in matches) / total_matches
        top_match = matches[0] if matches else None
        
        return {
            'total_matches': total_matches,
            'average_score': round(average_score, 2),
            'top_match': {
                'name': top_match.consultant.name,
                'score': top_match.match_score,
                'reasons': top_match.reasons
            } if top_match else None
        }
