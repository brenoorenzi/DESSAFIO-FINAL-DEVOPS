import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__' em werkzeug 
if not hasattr(werkzeug, '__version__'): 
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase): 
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
    
    def test_get_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"items": ["item1", "item2", "item3"]})


    def test_protected_with_valid_token(self):
        # Primeiro gera token
        login_response = self.client.get('/login')
        token = login_response.json['access_token']

        # Agora acessa rota protegida com token válido
        response = self.client.post(
            '/protected',
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Protected route"})


    def test_protected_with_invalid_token(self):
        invalid_token = "Bearer 123.invalid.token"

        response = self.client.post(
            '/protected',
            headers={"Authorization": invalid_token}
        )

        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()