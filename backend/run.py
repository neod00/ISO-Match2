"""
InsightMatch2 Backend 실행 스크립트
"""

import os
from main import create_app

if __name__ == '__main__':
    # Flask 애플리케이션 생성
    app = create_app()
    
    # 서버 실행
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("🚀 InsightMatch2 API 서버 시작")
    print(f"📍 포트: {port}")
    print(f"🔧 디버그 모드: {debug}")
    print(f"🌐 CORS 허용: {os.getenv('CORS_ORIGINS', 'http://localhost:3000')}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
