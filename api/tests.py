from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, Role, Announcement

class APIRoutingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='teststudent', email='test@example.com', password='password123')
        self.admin = User.objects.create_user(username='admin', is_staff=True, password='adminpassword')

    def test_users_route(self):
        # Testing rule: plural, lowercase, no trailing slash
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        
        # Testing trailing slash returns 301 or 404 depending on APPEND_SLASH=False
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 404)

    def test_nested_routes(self):
        # Nested rule: lowercase, hyphens, hierarchical
        url = f'/api/users/{self.user.id}/health-profile'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url_updates = f'/api/users/{self.user.id}/health-updates'
        response = self.client.get(url_updates)
        self.assertEqual(response.status_code, 200)

    def test_announcements_route(self):
        response = self.client.get('/api/announcements')
        self.assertEqual(response.status_code, 200)

    def test_appointments_route(self):
        response = self.client.get('/api/appointments')
        self.assertEqual(response.status_code, 200)
