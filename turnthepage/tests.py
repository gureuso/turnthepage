from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserModel = get_user_model()
        cls.user = UserModel.objects.create_test_user()
