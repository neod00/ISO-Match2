"""
InsightMatch2 Backend API Server
AI 기반 기업 리스크 분석 및 컨설턴트 매칭 서비스
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.config import Config
from app.middleware.error_handler import ErrorHandler

# 환경 변수 로드
load_dotenv()

def create_app():
    """Flask 애플리케이션 팩토리"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # CORS 설정
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    CORS(app, origins=cors_origins, supports_credentials=True)
    
    # 에러 핸들러 등록
    ErrorHandler(app)
    
    # API 라우트 등록
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app


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
