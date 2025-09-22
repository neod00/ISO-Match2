"""
Database Table Schema and Creation
"""

def create_tables():
    """테이블 생성 SQL 스크립트"""
    
    # Companies 테이블
    companies_sql = """
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        homepage VARCHAR(500) NOT NULL,
        email VARCHAR(255) NOT NULL,
        industry VARCHAR(100),
        size VARCHAR(50),
        region VARCHAR(100),
        description TEXT,
        website_info JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name);
    CREATE INDEX IF NOT EXISTS idx_companies_industry ON companies(industry);
    CREATE INDEX IF NOT EXISTS idx_companies_region ON companies(region);
    """
    
    # Consultants 테이블
    consultants_sql = """
    CREATE TABLE IF NOT EXISTS consultants (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        phone VARCHAR(50),
        industry VARCHAR(100) NOT NULL,
        region VARCHAR(100) NOT NULL,
        years_experience INTEGER DEFAULT 0,
        certifications TEXT[],
        description TEXT,
        rating DECIMAL(3,2) DEFAULT 0.0,
        status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_consultants_industry ON consultants(industry);
    CREATE INDEX IF NOT EXISTS idx_consultants_region ON consultants(region);
    CREATE INDEX IF NOT EXISTS idx_consultants_status ON consultants(status);
    CREATE INDEX IF NOT EXISTS idx_consultants_certifications ON consultants USING GIN(certifications);
    """
    
    # Analyses 테이블
    analyses_sql = """
    CREATE TABLE IF NOT EXISTS analyses (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
        company_name VARCHAR(255) NOT NULL,
        homepage VARCHAR(500) NOT NULL,
        email VARCHAR(255) NOT NULL,
        summary TEXT NOT NULL,
        risks TEXT[],
        certifications TEXT[],
        news_data JSONB,
        dart_data JSONB,
        social_data JSONB,
        website_data JSONB,
        analysis_method VARCHAR(100) DEFAULT 'AI (GPT-4o-mini)',
        confidence_score DECIMAL(3,2) DEFAULT 0.0,
        crawl_status VARCHAR(20) DEFAULT 'success',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_analyses_company_id ON analyses(company_id);
    CREATE INDEX IF NOT EXISTS idx_analyses_company_name ON analyses(company_name);
    CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at);
    CREATE INDEX IF NOT EXISTS idx_analyses_risks ON analyses USING GIN(risks);
    CREATE INDEX IF NOT EXISTS idx_analyses_certifications ON analyses USING GIN(certifications);
    """
    
    # Matches 테이블 (컨설턴트 매칭 기록)
    matches_sql = """
    CREATE TABLE IF NOT EXISTS matches (
        id SERIAL PRIMARY KEY,
        analysis_id INTEGER REFERENCES analyses(id) ON DELETE CASCADE,
        consultant_id INTEGER REFERENCES consultants(id) ON DELETE CASCADE,
        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
        match_score DECIMAL(3,2) DEFAULT 0.0,
        status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_matches_analysis_id ON matches(analysis_id);
    CREATE INDEX IF NOT EXISTS idx_matches_consultant_id ON matches(consultant_id);
    CREATE INDEX IF NOT EXISTS idx_matches_company_id ON matches(company_id);
    CREATE INDEX IF NOT EXISTS idx_matches_status ON matches(status);
    """
    
    return {
        'companies': companies_sql,
        'consultants': consultants_sql,
        'analyses': analyses_sql,
        'matches': matches_sql
    }

def get_table_schemas():
    """테이블 스키마 정보 반환"""
    return {
        'companies': {
            'description': '기업 정보 테이블',
            'columns': [
                'id (SERIAL PRIMARY KEY)',
                'name (VARCHAR(255))',
                'homepage (VARCHAR(500))',
                'email (VARCHAR(255))',
                'industry (VARCHAR(100))',
                'size (VARCHAR(50))',
                'region (VARCHAR(100))',
                'description (TEXT)',
                'website_info (JSONB)',
                'created_at (TIMESTAMP)',
                'updated_at (TIMESTAMP)'
            ]
        },
        'consultants': {
            'description': '컨설턴트 정보 테이블',
            'columns': [
                'id (SERIAL PRIMARY KEY)',
                'name (VARCHAR(255))',
                'email (VARCHAR(255))',
                'phone (VARCHAR(50))',
                'industry (VARCHAR(100))',
                'region (VARCHAR(100))',
                'years_experience (INTEGER)',
                'certifications (TEXT[])',
                'description (TEXT)',
                'rating (DECIMAL(3,2))',
                'status (VARCHAR(20))',
                'created_at (TIMESTAMP)',
                'updated_at (TIMESTAMP)'
            ]
        },
        'analyses': {
            'description': '분석 결과 테이블',
            'columns': [
                'id (SERIAL PRIMARY KEY)',
                'company_id (INTEGER)',
                'company_name (VARCHAR(255))',
                'homepage (VARCHAR(500))',
                'email (VARCHAR(255))',
                'summary (TEXT)',
                'risks (TEXT[])',
                'certifications (TEXT[])',
                'news_data (JSONB)',
                'dart_data (JSONB)',
                'social_data (JSONB)',
                'website_data (JSONB)',
                'analysis_method (VARCHAR(100))',
                'confidence_score (DECIMAL(3,2))',
                'crawl_status (VARCHAR(20))',
                'created_at (TIMESTAMP)',
                'updated_at (TIMESTAMP)'
            ]
        },
        'matches': {
            'description': '컨설턴트 매칭 기록 테이블',
            'columns': [
                'id (SERIAL PRIMARY KEY)',
                'analysis_id (INTEGER)',
                'consultant_id (INTEGER)',
                'company_id (INTEGER)',
                'match_score (DECIMAL(3,2))',
                'status (VARCHAR(20))',
                'created_at (TIMESTAMP)',
                'updated_at (TIMESTAMP)'
            ]
        }
    }
