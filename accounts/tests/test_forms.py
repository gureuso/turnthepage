from accounts.forms import SignupForm
from turnthepage.commons import get_random_string
from turnthepage.tests import BaseTestCase


class SignupFormTest(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.username = 'test'
        cls.email = 'test@gmail.com'
        cls.password = 'password'

        cls.already_exist_username = 'gureuso'
        cls.already_exist_email = 'wyun13043@gmail.com'

        cls.invalid_users = [
            get_random_string(151),
            '!!!!',
        ]
        cls.invalid_emails = [
            get_random_string(255),
            get_random_string(255) + '@test',
            get_random_string(255) + '@test.com',
        ]

    def test_without_username(self):
        data = {'username': None, 'email': self.email, 'password': self.password}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_without_email(self):
        data = {'username': self.username, 'email': None, 'password': self.password}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_with_clean_data(self):
        data = {'username': self.username, 'email': self.email, 'password': self.password}
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_already_exist_username(self):
        data = {'username': self.already_exist_username, 'email': self.email, 'password': self.password}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_already_exist_email(self):
        data = {'username': self.username, 'email': self.already_exist_email, 'password': self.password}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_username(self):
        for username in self.invalid_users:
            data = {'username': username, 'email': self.email, 'password': self.password}
            form = SignupForm(data=data)
            self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        for email in self.invalid_emails:
            data = {'username': self.username, 'email': email, 'password': self.password}
            form = SignupForm(data=data)
            self.assertFalse(form.is_valid())
