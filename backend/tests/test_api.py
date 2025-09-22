"""
API 엔드포인트 테스트
"""

import unittest
import json
from main import create_app

class TestAPI(unittest.TestCase):
    """API 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """헬스 체크 테스트"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'healthy')
    
    def test_analyze_company_success(self):
        """기업 분석 성공 테스트"""
        test_data = {
            'homepage': 'https://example.com',
            'email': 'test@example.com'
        }
        
        response = self.client.post(
            '/api/analyze',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_analyze_company_missing_fields(self):
        """기업 분석 필수 필드 누락 테스트"""
        test_data = {
            'homepage': 'https://example.com'
            # email 누락
        }
        
        response = self.client.post(
            '/api/analyze',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_analyze_company_invalid_email(self):
        """기업 분석 잘못된 이메일 테스트"""
        test_data = {
            'homepage': 'https://example.com',
            'email': 'invalid-email'
        }
        
        response = self.client.post(
            '/api/analyze',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_get_consultants(self):
        """컨설턴트 목록 조회 테스트"""
        response = self.client.get('/api/consultants')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_get_consultants_with_filters(self):
        """필터가 있는 컨설턴트 목록 조회 테스트"""
        response = self.client.get('/api/consultants?industry=IT&region=서울')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_register_consultant_success(self):
        """컨설턴트 등록 성공 테스트"""
        test_data = {
            'name': '홍길동',
            'email': 'hong@example.com',
            'industry': 'IT',
            'certifications': ['ISO 27001', 'ISO 9001'],
            'region': '서울',
            'years': 5
        }
        
        response = self.client.post(
            '/api/consultants',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_register_consultant_missing_fields(self):
        """컨설턴트 등록 필수 필드 누락 테스트"""
        test_data = {
            'name': '홍길동',
            'email': 'hong@example.com'
            # industry, certifications 누락
        }
        
        response = self.client.post(
            '/api/consultants',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_get_recommendations(self):
        """컨설턴트 추천 테스트"""
        test_data = {
            'company_name': 'Example Corp'
        }
        
        response = self.client.post(
            '/api/recommendations',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # 분석 결과가 없을 수 있으므로 400도 허용
        self.assertIn(response.status_code, [200, 400])
        data = json.loads(response.data)
        self.assertIn('success', data)
    
    def test_get_recommendations_criteria(self):
        """기준별 컨설턴트 추천 테스트"""
        test_data = {
            'industry': 'IT',
            'certifications': ['ISO 27001'],
            'region': '서울',
            'min_experience': 5,
            'limit': 3
        }
        
        response = self.client.post(
            '/api/recommendations/criteria',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_api_docs(self):
        """API 문서 조회 테스트"""
        response = self.client.get('/api/docs')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('openapi', data['data'])

if __name__ == '__main__':
    unittest.main()
