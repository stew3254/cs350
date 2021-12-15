from django.test import TestCase
from majorizer.models import *
from django.contrib.auth.models import User


# Create your tests here.


class TestUserCreation(TestCase):
    def test_create(self):
        # Should be allowed
        self.assertTrue(User.objects.create_user(username="t"*32, password="p"*64))
        self.assertFalse(User.objects.create_user(username="fail1", password="p"))


# class TestLogin(TestCase):
#     def setUp(self):
#         user = User.objects.create_user(first_name="test_case", username="test_case", password="test_case")
#
#     def test_login(self):
#         user = User.objects.get(uname="test_case")
#         # TODO figure out how to test login here
