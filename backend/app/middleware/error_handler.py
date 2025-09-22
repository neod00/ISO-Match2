"""
에러 처리 미들웨어
"""

from flask import jsonify, request
from werkzeug.exceptions import HTTPException
import traceback
import logging

class ErrorHandler:
    """에러 처리 클래스"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """앱에 에러 핸들러 등록"""
        app.register_error_handler(Exception, self.handle_exception)
        app.register_error_handler(HTTPException, self.handle_http_exception)
        app.register_error_handler(400, self.handle_bad_request)
        app.register_error_handler(401, self.handle_unauthorized)
        app.register_error_handler(403, self.handle_forbidden)
        app.register_error_handler(404, self.handle_not_found)
        app.register_error_handler(500, self.handle_internal_error)
    
    def handle_exception(self, e):
        """일반 예외 처리"""
        logging.error(f"Unhandled exception: {str(e)}")
        logging.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': '서버 내부 오류가 발생했습니다.',
            'error_code': 'INTERNAL_ERROR',
            'timestamp': self._get_timestamp()
        }), 500
    
    def handle_http_exception(self, e):
        """HTTP 예외 처리"""
        return jsonify({
            'success': False,
            'error': e.description or 'HTTP 오류가 발생했습니다.',
            'error_code': e.code,
            'timestamp': self._get_timestamp()
        }), e.code
    
    def handle_bad_request(self, e):
        """400 Bad Request 처리"""
        return jsonify({
            'success': False,
            'error': '잘못된 요청입니다.',
            'error_code': 'BAD_REQUEST',
            'timestamp': self._get_timestamp()
        }), 400
    
    def handle_unauthorized(self, e):
        """401 Unauthorized 처리"""
        return jsonify({
            'success': False,
            'error': '인증이 필요합니다.',
            'error_code': 'UNAUTHORIZED',
            'timestamp': self._get_timestamp()
        }), 401
    
    def handle_forbidden(self, e):
        """403 Forbidden 처리"""
        return jsonify({
            'success': False,
            'error': '접근이 거부되었습니다.',
            'error_code': 'FORBIDDEN',
            'timestamp': self._get_timestamp()
        }), 403
    
    def handle_not_found(self, e):
        """404 Not Found 처리"""
        return jsonify({
            'success': False,
            'error': '요청한 리소스를 찾을 수 없습니다.',
            'error_code': 'NOT_FOUND',
            'timestamp': self._get_timestamp()
        }), 404
    
    def handle_internal_error(self, e):
        """500 Internal Server Error 처리"""
        return jsonify({
            'success': False,
            'error': '서버 내부 오류가 발생했습니다.',
            'error_code': 'INTERNAL_ERROR',
            'timestamp': self._get_timestamp()
        }), 500
    
    def _get_timestamp(self):
        """현재 타임스탬프 반환"""
        from datetime import datetime
        return datetime.now().isoformat()
