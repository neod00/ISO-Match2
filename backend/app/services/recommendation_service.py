"""
추천 서비스
"""

from typing import List, Dict, Optional
from app.models.consultant import Consultant
from app.models.analysis import Analysis
from .matching_service import MatchingService, MatchResult
from .database_service import DatabaseService

class RecommendationService:
    """추천 서비스 클래스"""
    
    def __init__(self):
        self.matching_service = MatchingService()
        self.db_service = DatabaseService()
    
    def get_recommendations(self, analysis: Analysis, limit: int = 5) -> Dict:
        """
        분석 결과를 바탕으로 컨설턴트 추천
        
        Args:
            analysis: 분석 결과
            limit: 추천할 컨설턴트 수
            
        Returns:
            Dict: 추천 결과
        """
        try:
            # 매칭 실행
            matches = self.matching_service.find_matches(analysis, limit)
            
            if not matches:
                return self._get_fallback_recommendations(analysis, limit)
            
            # 매칭 결과를 딕셔너리로 변환
            recommendations = []
            for match in matches:
                recommendation = {
                    'consultant': match.consultant.to_dict(),
                    'match_score': match.match_score,
                    'reasons': match.reasons,
                    'industry_match': match.industry_match,
                    'certification_matches': match.certification_matches,
                    'region_match': match.region_match,
                    'experience_level': match.experience_level
                }
                recommendations.append(recommendation)
            
            # 매칭 요약 생성
            summary = self.matching_service.get_match_summary(matches)
            
            return {
                'success': True,
                'recommendations': recommendations,
                'summary': summary,
                'analysis_id': analysis.id,
                'company_name': analysis.company_name
            }
            
        except Exception as e:
            print(f"❌ 추천 생성 중 오류: {str(e)}")
            return self._get_fallback_recommendations(analysis, limit)
    
    def get_recommendations_by_company(self, company_name: str, limit: int = 5) -> Dict:
        """
        기업명으로 최신 분석 결과를 바탕으로 추천
        
        Args:
            company_name: 기업명
            limit: 추천할 컨설턴트 수
            
        Returns:
            Dict: 추천 결과
        """
        try:
            # 최신 분석 결과 조회
            analysis = self.db_service.get_latest_analysis(company_name)
            
            if not analysis:
                return {
                    'success': False,
                    'error': f'{company_name}의 분석 결과를 찾을 수 없습니다.',
                    'recommendations': []
                }
            
            return self.get_recommendations(analysis, limit)
            
        except Exception as e:
            print(f"❌ 기업별 추천 중 오류: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'recommendations': []
            }
    
    def get_recommendations_by_criteria(self, industry: str = '', 
                                      certifications: List[str] = None, 
                                      region: str = '', 
                                      min_experience: int = 0,
                                      limit: int = 5) -> Dict:
        """
        기준에 따른 컨설턴트 추천
        
        Args:
            industry: 업종
            certifications: 필요한 인증 목록
            region: 지역
            min_experience: 최소 경력
            limit: 추천할 컨설턴트 수
            
        Returns:
            Dict: 추천 결과
        """
        try:
            # 컨설턴트 조회
            consultants = self.db_service.get_consultants(industry, '', region)
            
            if not consultants:
                return {
                    'success': False,
                    'error': '조건에 맞는 컨설턴트를 찾을 수 없습니다.',
                    'recommendations': []
                }
            
            # 경력 필터링
            if min_experience > 0:
                consultants = [c for c in consultants if c.years_experience >= min_experience]
            
            # 인증 필터링
            if certifications:
                filtered_consultants = []
                for consultant in consultants:
                    if any(cert in consultant.certifications for cert in certifications):
                        filtered_consultants.append(consultant)
                consultants = filtered_consultants
            
            # 점수 계산 및 정렬
            scored_consultants = []
            for consultant in consultants:
                score = self._calculate_criteria_score(consultant, industry, certifications, region, min_experience)
                scored_consultants.append((consultant, score))
            
            # 점수순 정렬
            scored_consultants.sort(key=lambda x: x[1], reverse=True)
            
            # 추천 결과 생성
            recommendations = []
            for consultant, score in scored_consultants[:limit]:
                recommendation = {
                    'consultant': consultant.to_dict(),
                    'match_score': score,
                    'reasons': self._generate_criteria_reasons(consultant, industry, certifications, region),
                    'industry_match': consultant.industry == industry if industry else True,
                    'certification_matches': [cert for cert in (certifications or []) if cert in consultant.certifications],
                    'region_match': consultant.region == region if region else True,
                    'experience_level': self.matching_service._get_experience_level(consultant.years_experience)
                }
                recommendations.append(recommendation)
            
            return {
                'success': True,
                'recommendations': recommendations,
                'summary': {
                    'total_matches': len(recommendations),
                    'average_score': sum(r['match_score'] for r in recommendations) / len(recommendations) if recommendations else 0,
                    'criteria': {
                        'industry': industry,
                        'certifications': certifications,
                        'region': region,
                        'min_experience': min_experience
                    }
                }
            }
            
        except Exception as e:
            print(f"❌ 기준별 추천 중 오류: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'recommendations': []
            }
    
    def _calculate_criteria_score(self, consultant: Consultant, industry: str, 
                                certifications: List[str], region: str, min_experience: int) -> float:
        """기준별 점수 계산"""
        score = 0.0
        
        # 업종 매칭
        if industry and consultant.industry == industry:
            score += 0.3
        
        # 인증 매칭
        if certifications:
            matches = sum(1 for cert in certifications if cert in consultant.certifications)
            score += (matches / len(certifications)) * 0.4
        
        # 지역 매칭
        if region and consultant.region == region:
            score += 0.1
        
        # 경력 점수
        if consultant.years_experience >= min_experience:
            score += 0.2
        
        return min(score, 1.0)
    
    def _generate_criteria_reasons(self, consultant: Consultant, industry: str, 
                                 certifications: List[str], region: str) -> List[str]:
        """기준별 매칭 이유 생성"""
        reasons = []
        
        if industry and consultant.industry == industry:
            reasons.append(f"업종 일치: {industry}")
        
        if certifications:
            matches = [cert for cert in certifications if cert in consultant.certifications]
            if matches:
                reasons.append(f"인증 일치: {', '.join(matches)}")
        
        if region and consultant.region == region:
            reasons.append(f"지역 일치: {region}")
        
        return reasons
    
    def _get_fallback_recommendations(self, analysis: Analysis, limit: int) -> Dict:
        """폴백 추천 (매칭 실패 시)"""
        try:
            # 기본 컨설턴트 조회
            consultants = self.db_service.get_consultants()
            
            if not consultants:
                return {
                    'success': False,
                    'error': '추천할 컨설턴트가 없습니다.',
                    'recommendations': []
                }
            
            # 상위 컨설턴트 반환
            recommendations = []
            for consultant in consultants[:limit]:
                recommendation = {
                    'consultant': consultant.to_dict(),
                    'match_score': 0.5,  # 기본 점수
                    'reasons': ['기본 추천'],
                    'industry_match': False,
                    'certification_matches': [],
                    'region_match': False,
                    'experience_level': self.matching_service._get_experience_level(consultant.years_experience)
                }
                recommendations.append(recommendation)
            
            return {
                'success': True,
                'recommendations': recommendations,
                'summary': {
                    'total_matches': len(recommendations),
                    'average_score': 0.5,
                    'note': '기본 추천입니다.'
                },
                'analysis_id': analysis.id,
                'company_name': analysis.company_name
            }
            
        except Exception as e:
            print(f"❌ 폴백 추천 생성 중 오류: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'recommendations': []
            }
