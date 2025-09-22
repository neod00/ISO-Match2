"""
InsightMatch2 Backend API Server
AI 기반 기업 리스크 분석 및 컨설턴트 매칭 서비스
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def create_app():
    """Flask 애플리케이션 팩토리"""
    app = Flask(__name__)
    
    # CORS 설정
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    CORS(app, origins=cors_origins, supports_credentials=True)
    
    # 환경 변수 설정
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # API 라우트 등록
    register_routes(app)
    
    return app

def register_routes(app):
    """API 라우트 등록"""
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """서버 상태 확인"""
        return jsonify({
            'status': 'healthy',
            'service': 'InsightMatch2 API',
            'version': '1.0.0'
        })
    
    @app.route('/api/analyze', methods=['POST'])
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
            
            # TODO: 실제 분석 로직 구현
            # 현재는 더미 데이터 반환
            result = {
                'company': extract_company_name(homepage),
                'summary': '공개자료 기반으로 보안·품질·환경 리스크가 식별되었습니다.',
                'risks': [
                    '정보보안 정책/절차 미흡',
                    '개인정보 처리방침 최신화 필요',
                    '공급망 리스크 모니터링 필요'
                ],
                'certifications': [
                    'ISO 27001',
                    'ISO 9001',
                    'ISO 14001'
                ],
                'news': [],
                'dart': [],
                'social': []
            }
            
            return jsonify({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            return jsonify({
                'error': f'분석 중 오류가 발생했습니다: {str(e)}'
            }), 500
    
    @app.route('/api/consultants', methods=['GET'])
    def get_consultants():
        """컨설턴트 목록 조회 API"""
        try:
            # 쿼리 파라미터
            industry = request.args.get('industry', '')
            certification = request.args.get('certification', '')
            region = request.args.get('region', '')
            
            # TODO: 실제 데이터베이스에서 조회
            # 현재는 더미 데이터 반환
            consultants = [
                {
                    'id': 1,
                    'name': '김지훈',
                    'rating': 4.9,
                    'years': 10,
                    'industry': 'IT',
                    'region': '서울',
                    'certifications': ['ISO 27001', 'ISO 9001'],
                    'email': 'kim@example.com'
                },
                {
                    'id': 2,
                    'name': '이서연',
                    'rating': 4.8,
                    'years': 8,
                    'industry': '제조',
                    'region': '경기',
                    'certifications': ['ISO 14001'],
                    'email': 'lee@example.com'
                }
            ]
            
            # 필터링
            filtered_consultants = consultants
            if industry:
                filtered_consultants = [c for c in filtered_consultants if c['industry'] == industry]
            if certification:
                filtered_consultants = [c for c in filtered_consultants if certification in c['certifications']]
            if region:
                filtered_consultants = [c for c in filtered_consultants if c['region'] == region]
            
            return jsonify({
                'success': True,
                'data': filtered_consultants,
                'total': len(filtered_consultants)
            })
            
        except Exception as e:
            return jsonify({
                'error': f'컨설턴트 조회 중 오류가 발생했습니다: {str(e)}'
            }), 500
    
    @app.route('/api/consultants', methods=['POST'])
    def register_consultant():
        """컨설턴트 등록 API"""
        try:
            data = request.get_json()
            
            # 필수 필드 검증
            required_fields = ['name', 'email', 'industry', 'certifications']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        'error': f'{field} 필드가 필요합니다.'
                    }), 400
            
            # TODO: 실제 데이터베이스에 저장
            # 현재는 성공 응답만 반환
            return jsonify({
                'success': True,
                'message': '컨설턴트 등록이 완료되었습니다.',
                'data': {
                    'id': 999,  # 임시 ID
                    'name': data['name'],
                    'email': data['email']
                }
            })
            
        except Exception as e:
            return jsonify({
                'error': f'컨설턴트 등록 중 오류가 발생했습니다: {str(e)}'
            }), 500

def extract_company_name(homepage_url):
    """홈페이지 URL에서 기업명 추출"""
    import re
    from urllib.parse import urlparse
    
    try:
        parsed = urlparse(homepage_url)
        domain = parsed.netloc or parsed.path
        
        # www 제거
        domain = domain.replace('www.', '')
        
        # 도메인에서 기업명 추출
        parts = domain.split('.')
        if len(parts) >= 2:
            return parts[0].capitalize()
        
        return domain.capitalize()
    except:
        return 'Unknown Company'

if __name__ == '__main__':
    app = create_app()
    
    # 서버 실행
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 InsightMatch2 API 서버 시작")
    print(f"📍 포트: {port}")
    print(f"🔧 디버그 모드: {debug}")
    print(f"🌐 CORS 허용: {os.getenv('CORS_ORIGINS', 'http://localhost:3000')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
