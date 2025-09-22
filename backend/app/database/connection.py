"""
Database Connection Manager
"""

import os
from typing import Optional
from supabase import create_client, Client
from app.config import Config

class DatabaseConnection:
    """데이터베이스 연결 관리 클래스"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._connect()
    
    def _connect(self):
        """Supabase 클라이언트 연결"""
        try:
            supabase_url = Config.SUPABASE_URL
            supabase_key = Config.SUPABASE_KEY
            
            if not supabase_url or not supabase_key:
                print("⚠️ Supabase 설정이 없습니다. 로컬 모드로 실행됩니다.")
                return
            
            self.client = create_client(supabase_url, supabase_key)
            print("✅ Supabase 데이터베이스 연결 성공")
            
        except Exception as e:
            print(f"❌ Supabase 연결 실패: {str(e)}")
            self.client = None
    
    def get_client(self) -> Optional[Client]:
        """Supabase 클라이언트 반환"""
        return self.client
    
    def is_connected(self) -> bool:
        """연결 상태 확인"""
        return self.client is not None
    
    def test_connection(self) -> bool:
        """연결 테스트"""
        if not self.client:
            return False
        
        try:
            # 간단한 쿼리로 연결 테스트
            result = self.client.table('companies').select('id').limit(1).execute()
            return True
        except Exception as e:
            print(f"❌ 데이터베이스 연결 테스트 실패: {str(e)}")
            return False

# 전역 데이터베이스 연결 인스턴스
db_connection = DatabaseConnection()
