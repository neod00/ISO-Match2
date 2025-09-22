"""
API 유효성 검사
"""

from app.middleware.response_formatter import ResponseFormatter

class APIValidators:
    """API 유효성 검사 클래스"""
    
    @staticmethod
    def validate_analyze_request(data):
        """분석 요청 유효성 검사"""
        if not data:
            return ResponseFormatter.error(
                message="요청 데이터가 없습니다.",
                error_code="NO_DATA",
                status_code=400
            )
        
        # 필수 필드 검사
        required_fields = ['homepage', 'email']
        error = ResponseFormatter.validate_required_fields(data, required_fields)
        if error:
            return error
        
        # 이메일 형식 검사
        if not ResponseFormatter.validate_email(data['email']):
            return ResponseFormatter.error(
                message="올바른 이메일 형식이 아닙니다.",
                error_code="INVALID_EMAIL",
                status_code=400
            )
        
        # URL 형식 검사
        if not ResponseFormatter.validate_url(data['homepage']):
            return ResponseFormatter.error(
                message="올바른 URL 형식이 아닙니다.",
                error_code="INVALID_URL",
                status_code=400
            )
        
        return None
    
    @staticmethod
    def validate_consultant_request(data):
        """컨설턴트 등록 요청 유효성 검사"""
        if not data:
            return ResponseFormatter.error(
                message="요청 데이터가 없습니다.",
                error_code="NO_DATA",
                status_code=400
            )
        
        # 필수 필드 검사
        required_fields = ['name', 'email', 'industry', 'certifications']
        error = ResponseFormatter.validate_required_fields(data, required_fields)
        if error:
            return error
        
        # 이메일 형식 검사
        if not ResponseFormatter.validate_email(data['email']):
            return ResponseFormatter.error(
                message="올바른 이메일 형식이 아닙니다.",
                error_code="INVALID_EMAIL",
                status_code=400
            )
        
        # 인증 목록 검사
        if not isinstance(data['certifications'], list) or len(data['certifications']) == 0:
            return ResponseFormatter.error(
                message="인증 목록이 비어있습니다.",
                error_code="EMPTY_CERTIFICATIONS",
                status_code=400
            )
        
        # 업종 검사
        valid_industries = ['IT', '제조', '바이오/헬스', '교육', '금융', '기타']
        if data['industry'] not in valid_industries:
            return ResponseFormatter.error(
                message=f"유효하지 않은 업종입니다. 가능한 업종: {', '.join(valid_industries)}",
                error_code="INVALID_INDUSTRY",
                status_code=400
            )
        
        return None
    
    @staticmethod
    def validate_recommendation_request(data):
        """추천 요청 유효성 검사"""
        if not data:
            return ResponseFormatter.error(
                message="요청 데이터가 없습니다.",
                error_code="NO_DATA",
                status_code=400
            )
        
        # 기업명 검사
        if 'company_name' not in data or not data['company_name'].strip():
            return ResponseFormatter.error(
                message="기업명이 필요합니다.",
                error_code="MISSING_COMPANY_NAME",
                status_code=400
            )
        
        return None
    
    @staticmethod
    def validate_criteria_request(data):
        """기준별 추천 요청 유효성 검사"""
        if not data:
            return ResponseFormatter.error(
                message="요청 데이터가 없습니다.",
                error_code="NO_DATA",
                status_code=400
            )
        
        # 업종 검사 (선택사항)
        if 'industry' in data and data['industry']:
            valid_industries = ['IT', '제조', '바이오/헬스', '교육', '금융', '기타']
            if data['industry'] not in valid_industries:
                return ResponseFormatter.error(
                    message=f"유효하지 않은 업종입니다. 가능한 업종: {', '.join(valid_industries)}",
                    error_code="INVALID_INDUSTRY",
                    status_code=400
                )
        
        # 인증 목록 검사 (선택사항)
        if 'certifications' in data and data['certifications']:
            if not isinstance(data['certifications'], list):
                return ResponseFormatter.error(
                    message="인증 목록은 배열이어야 합니다.",
                    error_code="INVALID_CERTIFICATIONS",
                    status_code=400
                )
        
        # 최소 경력 검사 (선택사항)
        if 'min_experience' in data and data['min_experience'] is not None:
            if not isinstance(data['min_experience'], int) or data['min_experience'] < 0:
                return ResponseFormatter.error(
                    message="최소 경력은 0 이상의 정수여야 합니다.",
                    error_code="INVALID_MIN_EXPERIENCE",
                    status_code=400
                )
        
        # 추천 수 검사 (선택사항)
        if 'limit' in data and data['limit'] is not None:
            if not isinstance(data['limit'], int) or data['limit'] <= 0 or data['limit'] > 50:
                return ResponseFormatter.error(
                    message="추천 수는 1-50 사이의 정수여야 합니다.",
                    error_code="INVALID_LIMIT",
                    status_code=400
                )
        
        return None
