from django.test import TestCase

from accounts.forms import (
    AddUserForm,
    ProfileForm,
    UserEditForm,
)
from accounts.models import User


class ProfileFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="TestPass123!",
            email="john@example.com",
        )

    def test_profile_form_accepts_valid_data(self):
        form = ProfileForm(
            instance=self.user,
            data={
                "username": "john",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone_number": "",
            },
        )
        self.assertTrue(form.is_valid())

    def test_profile_form_rejects_duplicate_username(self):
        User.objects.create_user(
            username="mary",
            password="TestPass123!",
            email="mary@example.com",
        )

        form = ProfileForm(
            instance=self.user,
            data={
                "username": "mary",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone_number": "",
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class UserEditFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="adminuser",
            password="TestPass123!",
        )

    def test_user_edit_form_valid(self):
        form = UserEditForm(
            instance=self.user,
            data={
                "username": "adminuser",
                "first_name": "",
                "last_name": "",
                "email": "adminuser@example.com",
                "phone_number": "",
                "role": self.user.role,
                "department": "",
                "is_active": True,
            },
        )

        
        self.assertTrue(form.is_valid())


class AddUserFormTests(TestCase):
    def test_passwords_must_match(self):
        form = AddUserForm(
            data={
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "phone_number": "",
                "role": "staff",
                "department": "",
                "password1": "Password123!",
                "password2": "DifferentPassword123!",
            }
        )

        self.assertFalse(form.is_valid())