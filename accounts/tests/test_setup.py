from rest_framework.test import APITestCase
from django.urls import reverse


# class to get access to our endpoints for testing
class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data={
            'email': "email@gmail.com",
            'username': "email",
            'password': "email@gmail.com",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()