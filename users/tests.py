from rest_framework.test import APITestCase
from rest_framework import status

class JWTAuthTestCase(APITestCase):

    def get_jwt_token(self, username, password):
        response = self.client.post('/api/v1/users/login/', {'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']
