"""
InsightMatch2 API Routes
"""

from flask import Blueprint, request, jsonify
from app.services.analyzer import CompanyAnalyzer
from app.services.consultant_service import ConsultantService
from app.services.recommendation_service import RecommendationService

# 블루프린트 생성
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 서비스 인스턴스
analyzer = CompanyAnalyzer()
consultant_service = ConsultantService()
recommendation_service = RecommendationService()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({
        'status': 'healthy',
        'service': 'InsightMatch2 API',
        'version': '1.0.0'
    })

@api_bp.route('/analyze', methods=['POST'])
def analyze_company():
    """기업 분석 API"""
    try:
        data = request.get_json()
        homepage = data.get('homepage', '').strip()
        email = data.get('email', '').strip()
        
        if not homepage or not email:
            return jsonify({
                'error': '홈페이지 URL과 이메일이 필요합니다.'
            }), 400
        
        # 기업 분석 실행
        result = analyzer.analyze(homepage, email)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'error': f'분석 중 오류가 발생했습니다: {str(e)}'
        }), 500

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
        
        return jsonify({
            'success': True,
            'data': consultants,
            'total': len(consultants)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'컨설턴트 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

@api_bp.route('/consultants', methods=['POST'])
def register_consultant():
    """컨설턴트 등록 API"""
    try:
        data = request.get_json()
        
        # 컨설턴트 등록
        result = consultant_service.register_consultant(data)
        
        return jsonify({
            'success': True,
            'message': '컨설턴트 등록이 완료되었습니다.',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'error': f'컨설턴트 등록 중 오류가 발생했습니다: {str(e)}'
        }), 500

@api_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """컨설턴트 추천 API"""
    try:
        data = request.get_json()
        company_name = data.get('company_name', '').strip()
        
        if not company_name:
            return jsonify({
                'error': '기업명이 필요합니다.'
            }), 400
        
        # 추천 실행
        result = recommendation_service.get_recommendations_by_company(company_name)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'추천 생성 중 오류가 발생했습니다: {str(e)}'
        }), 500

@api_bp.route('/recommendations/criteria', methods=['POST'])
def get_recommendations_by_criteria():
    """기준별 컨설턴트 추천 API"""
    try:
        data = request.get_json()
        
        # 추천 실행
        result = recommendation_service.get_recommendations_by_criteria(
            industry=data.get('industry', ''),
            certifications=data.get('certifications', []),
            region=data.get('region', ''),
            min_experience=data.get('min_experience', 0),
            limit=data.get('limit', 5)
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'기준별 추천 생성 중 오류가 발생했습니다: {str(e)}'
        }), 500
