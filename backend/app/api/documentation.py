"""
API 문서화
"""

API_DOCS = {
    "openapi": "3.0.0",
    "info": {
        "title": "InsightMatch2 API",
        "description": "AI 기반 기업 리스크 분석과 컨설턴트 매칭 서비스 API",
        "version": "1.0.0",
        "contact": {
            "name": "InsightMatch2 Team",
            "email": "support@insightmatch2.com"
        }
    },
    "servers": [
        {
            "url": "http://localhost:8000",
            "description": "개발 서버"
        },
        {
            "url": "https://your-railway-app.railway.app",
            "description": "프로덕션 서버"
        }
    ],
    "paths": {
        "/api/health": {
            "get": {
                "summary": "서버 상태 확인",
                "description": "API 서버의 상태를 확인합니다.",
                "responses": {
                    "200": {
                        "description": "서버 정상",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "healthy",
                                    "service": "InsightMatch2 API",
                                    "version": "1.0.0"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/analyze": {
            "post": {
                "summary": "기업 분석",
                "description": "홈페이지 URL과 이메일을 입력하여 기업을 분석합니다.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["homepage", "email"],
                                "properties": {
                                    "homepage": {
                                        "type": "string",
                                        "format": "uri",
                                        "description": "기업 홈페이지 URL",
                                        "example": "https://example.com"
                                    },
                                    "email": {
                                        "type": "string",
                                        "format": "email",
                                        "description": "연락처 이메일",
                                        "example": "contact@example.com"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "분석 성공",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "data": {
                                        "company": "Example Corp",
                                        "homepage": "https://example.com",
                                        "email": "contact@example.com",
                                        "summary": "기업 분석 요약",
                                        "risks": ["리스크 1", "리스크 2"],
                                        "certifications": ["ISO 27001", "ISO 9001"],
                                        "news": [],
                                        "dart": [],
                                        "social": [],
                                        "website": {},
                                        "analysis_date": "2024-01-15 10:30:00",
                                        "confidence_score": 0.85,
                                        "analysis_method": "AI (GPT-4o-mini)",
                                        "crawl_status": "success",
                                        "recommendations": []
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "잘못된 요청",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": False,
                                    "error": "홈페이지 URL과 이메일이 필요합니다.",
                                    "error_code": "BAD_REQUEST",
                                    "timestamp": "2024-01-15T10:30:00"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/consultants": {
            "get": {
                "summary": "컨설턴트 목록 조회",
                "description": "필터 조건에 따라 컨설턴트 목록을 조회합니다.",
                "parameters": [
                    {
                        "name": "industry",
                        "in": "query",
                        "description": "업종 필터",
                        "schema": {
                            "type": "string",
                            "enum": ["IT", "제조", "바이오/헬스", "교육", "금융", "기타"]
                        }
                    },
                    {
                        "name": "certification",
                        "in": "query",
                        "description": "인증 필터",
                        "schema": {
                            "type": "string",
                            "enum": ["ISO 27001", "ISO 9001", "ISO 14001", "ISO 27701", "GDPR"]
                        }
                    },
                    {
                        "name": "region",
                        "in": "query",
                        "description": "지역 필터",
                        "schema": {
                            "type": "string",
                            "enum": ["서울", "경기", "부산", "대구", "기타"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "조회 성공",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "data": [
                                        {
                                            "id": 1,
                                            "name": "김지훈",
                                            "email": "kim@example.com",
                                            "industry": "IT",
                                            "region": "서울",
                                            "years_experience": 10,
                                            "certifications": ["ISO 27001", "ISO 9001"],
                                            "rating": 4.9,
                                            "status": "active"
                                        }
                                    ],
                                    "total": 1
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "컨설턴트 등록",
                "description": "새로운 컨설턴트를 등록합니다.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["name", "email", "industry", "certifications"],
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "이름",
                                        "example": "홍길동"
                                    },
                                    "email": {
                                        "type": "string",
                                        "format": "email",
                                        "description": "이메일",
                                        "example": "hong@example.com"
                                    },
                                    "phone": {
                                        "type": "string",
                                        "description": "연락처",
                                        "example": "010-1234-5678"
                                    },
                                    "industry": {
                                        "type": "string",
                                        "description": "전문 업종",
                                        "example": "IT"
                                    },
                                    "region": {
                                        "type": "string",
                                        "description": "활동 지역",
                                        "example": "서울"
                                    },
                                    "years": {
                                        "type": "integer",
                                        "description": "경력 (년)",
                                        "example": 5
                                    },
                                    "certifications": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "보유 인증",
                                        "example": ["ISO 27001", "ISO 9001"]
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "자기소개",
                                        "example": "전문 컨설턴트입니다."
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "등록 성공",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "message": "컨설턴트 등록이 완료되었습니다.",
                                    "data": {
                                        "id": 1,
                                        "name": "홍길동",
                                        "email": "hong@example.com",
                                        "status": "pending"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/recommendations": {
            "post": {
                "summary": "컨설턴트 추천",
                "description": "기업명을 바탕으로 컨설턴트를 추천합니다.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["company_name"],
                                "properties": {
                                    "company_name": {
                                        "type": "string",
                                        "description": "기업명",
                                        "example": "Example Corp"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "추천 성공",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "recommendations": [
                                        {
                                            "consultant": {
                                                "id": 1,
                                                "name": "김지훈",
                                                "email": "kim@example.com",
                                                "industry": "IT",
                                                "region": "서울",
                                                "years_experience": 10,
                                                "certifications": ["ISO 27001", "ISO 9001"],
                                                "rating": 4.9,
                                                "status": "active"
                                            },
                                            "match_score": 0.85,
                                            "reasons": ["업종 일치", "인증 일치: ISO 27001"],
                                            "industry_match": True,
                                            "certification_matches": ["ISO 27001"],
                                            "region_match": True,
                                            "experience_level": "senior"
                                        }
                                    ],
                                    "summary": {
                                        "total_matches": 1,
                                        "average_score": 0.85,
                                        "top_match": {
                                            "name": "김지훈",
                                            "score": 0.85,
                                            "reasons": ["업종 일치", "인증 일치: ISO 27001"]
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/recommendations/criteria": {
            "post": {
                "summary": "기준별 컨설턴트 추천",
                "description": "지정된 기준에 따라 컨설턴트를 추천합니다.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "industry": {
                                        "type": "string",
                                        "description": "업종",
                                        "example": "IT"
                                    },
                                    "certifications": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "필요한 인증",
                                        "example": ["ISO 27001", "ISO 9001"]
                                    },
                                    "region": {
                                        "type": "string",
                                        "description": "지역",
                                        "example": "서울"
                                    },
                                    "min_experience": {
                                        "type": "integer",
                                        "description": "최소 경력",
                                        "example": 5
                                    },
                                    "limit": {
                                        "type": "integer",
                                        "description": "추천 수",
                                        "example": 5
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "추천 성공",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "recommendations": [],
                                    "summary": {
                                        "total_matches": 0,
                                        "average_score": 0,
                                        "criteria": {
                                            "industry": "IT",
                                            "certifications": ["ISO 27001"],
                                            "region": "서울",
                                            "min_experience": 5
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Company": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "homepage": {"type": "string"},
                    "email": {"type": "string"},
                    "industry": {"type": "string"},
                    "size": {"type": "string"},
                    "region": {"type": "string"},
                    "description": {"type": "string"},
                    "website_info": {"type": "object"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            },
            "Consultant": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                    "industry": {"type": "string"},
                    "region": {"type": "string"},
                    "years_experience": {"type": "integer"},
                    "certifications": {"type": "array", "items": {"type": "string"}},
                    "description": {"type": "string"},
                    "rating": {"type": "number"},
                    "status": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            },
            "Analysis": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "company_id": {"type": "integer"},
                    "company_name": {"type": "string"},
                    "homepage": {"type": "string"},
                    "email": {"type": "string"},
                    "summary": {"type": "string"},
                    "risks": {"type": "array", "items": {"type": "string"}},
                    "certifications": {"type": "array", "items": {"type": "string"}},
                    "news_data": {"type": "array"},
                    "dart_data": {"type": "array"},
                    "social_data": {"type": "array"},
                    "website_data": {"type": "object"},
                    "analysis_method": {"type": "string"},
                    "confidence_score": {"type": "number"},
                    "crawl_status": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        }
    }
}

def get_api_docs():
    """API 문서 반환"""
    return API_DOCS

api_docs = API_DOCS
