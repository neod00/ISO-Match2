"""
응답 형식 표준화 미들웨어
"""

from flask import jsonify, request
from functools import wraps
from datetime import datetime

class ResponseFormatter:
    """응답 형식 표준화 클래스"""
    
    @staticmethod
    def success(data=None, message="성공", status_code=200):
        """성공 응답 형식"""
        response = {
            'success': True,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'status_code': status_code
        }
        
        if data is not None:
            response['data'] = data
        
        return jsonify(response), status_code
    
    @staticmethod
    def error(message="오류가 발생했습니다.", error_code="ERROR", status_code=400, details=None):
        """에러 응답 형식"""
        response = {
            'success': False,
            'error': message,
            'error_code': error_code,
            'timestamp': datetime.now().isoformat(),
            'status_code': status_code
        }
        
        if details:
            response['details'] = details
        
        return jsonify(response), status_code
    
    @staticmethod
    def paginated(data, page=1, per_page=10, total=None):
        """페이지네이션 응답 형식"""
        response = {
            'success': True,
            'data': data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total or len(data),
                'pages': (total // per_page) + 1 if total else 1
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """필수 필드 검증"""
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            return ResponseFormatter.error(
                message=f"필수 필드가 누락되었습니다: {', '.join(missing_fields)}",
                error_code="MISSING_FIELDS",
                status_code=400,
                details={'missing_fields': missing_fields}
            )
        
        return None
    
    @staticmethod
    def validate_email(email):
        """이메일 형식 검증"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_url(url):
        """URL 형식 검증"""
        import re
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return re.match(pattern, url) is not None

def api_response(func):
    """API 응답 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return ResponseFormatter.error(
                message=str(e),
                error_code="API_ERROR",
                status_code=500
            )
    return wrapper
