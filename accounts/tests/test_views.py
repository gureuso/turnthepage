from django.test import TestCase
from django.urls import reverse

from conf.constants import USERNAME, EMAIL, PASSWORD
from conf.tests import BaseTestCase


class SignupViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.path = reverse('accounts:signup')

    def test_get_signup(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_post_signup(self):
        # signup
        data = {'username': USERNAME, 'email': EMAIL, 'password': PASSWORD}
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 302)

        # check logged in
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 302)


class LoginViewTest(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.path = reverse('accounts:login')

    def test_login_with_username(self):
        data = {'username': USERNAME, 'password': PASSWORD}
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 302)

    def test_login_with_email(self):
        data = {'username': EMAIL, 'password': PASSWORD}
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 302)

    def test_login_without_username(self):
        data = {'username': None, 'password': PASSWORD}
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 200)

    def test_login_without_password(self):
        data = {'username': USERNAME, 'password': None}
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(BaseTestCase):
    def test_logout(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:login'))
