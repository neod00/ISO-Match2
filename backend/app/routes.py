"""
InsightMatch2 API Routes
"""

from flask import Blueprint, request, jsonify
from app.services.analyzer import CompanyAnalyzer
from app.services.consultant_service import ConsultantService
from app.services.recommendation_service import RecommendationService
from app.middleware.response_formatter import ResponseFormatter
from app.api.validators import APIValidators
from app.api.documentation import get_api_docs

# 블루프린트 생성
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 서비스 인스턴스
analyzer = CompanyAnalyzer()
consultant_service = ConsultantService()
recommendation_service = RecommendationService()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return ResponseFormatter.success(
        data={
            'status': 'healthy',
            'service': 'InsightMatch2 API',
            'version': '1.0.0'
        },
        message="서버가 정상적으로 작동 중입니다."
    )

@api_bp.route('/analyze', methods=['POST'])
def analyze_company():
    """기업 분석 API"""
    try:
        data = request.get_json()
        
        # 유효성 검사
        validation_error = APIValidators.validate_analyze_request(data)
        if validation_error:
            return validation_error
        
        # 기업 분석 실행
        result = analyzer.analyze(data['homepage'], data['email'])
        
        return ResponseFormatter.success(
            data=result,
            message="기업 분석이 완료되었습니다."
        )
        
    except Exception as e:
        return ResponseFormatter.error(
            message=f'분석 중 오류가 발생했습니다: {str(e)}',
            error_code="ANALYSIS_ERROR",
            status_code=500
        )

@api_bp.route('/consultants', methods=['GET'])
def get_consultants():
    """컨설턴트 목록 조회 API"""
    try:
        # 쿼리 파라미터
        industry = request.args.get('industry', '')
        certification = request.args.get('certification', '')
        region = request.args.get('region', '')
        
        # 컨설턴트 조회
        consultants = consultant_service.get_consultants(
            industry=industry,
            certification=certification,
            region=region
        )
        
        return ResponseFormatter.success(
            data=consultants,
            message=f"{len(consultants)}명의 컨설턴트를 찾았습니다."
        )
        
    except Exception as e:
        return ResponseFormatter.error(
            message=f'컨설턴트 조회 중 오류가 발생했습니다: {str(e)}',
            error_code="CONSULTANT_QUERY_ERROR",
            status_code=500
        )

@api_bp.route('/consultants', methods=['POST'])
def register_consultant():
    """컨설턴트 등록 API"""
    try:
        data = request.get_json()
        
        # 유효성 검사
        validation_error = APIValidators.validate_consultant_request(data)
        if validation_error:
            return validation_error
        
        # 컨설턴트 등록
        result = consultant_service.register_consultant(data)
        
        return ResponseFormatter.success(
            data=result,
            message="컨설턴트 등록이 완료되었습니다."
        )
        
    except Exception as e:
        return ResponseFormatter.error(
            message=f'컨설턴트 등록 중 오류가 발생했습니다: {str(e)}',
            error_code="CONSULTANT_REGISTRATION_ERROR",
            status_code=500
        )

@api_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """컨설턴트 추천 API"""
    try:
        data = request.get_json()
        
        # 유효성 검사
        validation_error = APIValidators.validate_recommendation_request(data)
        if validation_error:
            return validation_error
        
        # 추천 실행
        result = recommendation_service.get_recommendations_by_company(data['company_name'])
        
        if result['success']:
            return ResponseFormatter.success(
                data=result,
                message="컨설턴트 추천이 완료되었습니다."
            )
        else:
            return ResponseFormatter.error(
                message=result.get('error', '추천 생성에 실패했습니다.'),
                error_code="RECOMMENDATION_ERROR",
                status_code=400
            )
        
    except Exception as e:
        return ResponseFormatter.error(
            message=f'추천 생성 중 오류가 발생했습니다: {str(e)}',
            error_code="RECOMMENDATION_ERROR",
            status_code=500
        )

@api_bp.route('/recommendations/criteria', methods=['POST'])
def get_recommendations_by_criteria():
    """기준별 컨설턴트 추천 API"""
    try:
        data = request.get_json()
        
        # 유효성 검사
        validation_error = APIValidators.validate_criteria_request(data)
        if validation_error:
            return validation_error
        
        # 추천 실행
        result = recommendation_service.get_recommendations_by_criteria(
            industry=data.get('industry', ''),
            certifications=data.get('certifications', []),
            region=data.get('region', ''),
            min_experience=data.get('min_experience', 0),
            limit=data.get('limit', 5)
        )
        
        if result['success']:
            return ResponseFormatter.success(
                data=result,
                message="기준별 컨설턴트 추천이 완료되었습니다."
            )
        else:
            return ResponseFormatter.error(
                message=result.get('error', '기준별 추천 생성에 실패했습니다.'),
                error_code="CRITERIA_RECOMMENDATION_ERROR",
                status_code=400
            )
        
    except Exception as e:
            return ResponseFormatter.error(
                message=f'기준별 추천 생성 중 오류가 발생했습니다: {str(e)}',
                error_code="CRITERIA_RECOMMENDATION_ERROR",
                status_code=500
            )

@api_bp.route('/docs', methods=['GET'])
def get_api_documentation():
    """API 문서 조회"""
    try:
        docs = get_api_docs()
        return ResponseFormatter.success(
            data=docs,
            message="API 문서를 성공적으로 조회했습니다."
        )
    except Exception as e:
        return ResponseFormatter.error(
            message=f'API 문서 조회 중 오류가 발생했습니다: {str(e)}',
            error_code="DOCS_ERROR",
            status_code=500
        )
