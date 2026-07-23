from django.test import TestCase

from accounts.models import Department, User


class DepartmentModelTests(TestCase):
    def test_department_creation(self):
        department = Department.objects.create(
            name="Programs",
            description="Programs department",
        )

        self.assertEqual(department.name, "Programs")
        self.assertEqual(str(department), "Programs")


class UserModelTests(TestCase):
    def create_user(self, username="testuser", role=User.Role.STAFF):
        return User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password="TestPassword123!",
            role=role,
        )

    def test_user_creation(self):
        user = self.create_user()

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.role, User.Role.STAFF)
        self.assertTrue(user.check_password("TestPassword123!"))

    def test_default_role_is_staff(self):
        user = User.objects.create_user(
            username="defaultuser",
            email="default@example.com",
            password="TestPassword123!",
        )

        self.assertEqual(user.role, User.Role.STAFF)

    def test_admin_role_grants_staff_and_superuser_status(self):
        user = self.create_user(
            username="adminuser",
            role=User.Role.ADMIN,
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_portal_admin())

    def test_superuser_is_portal_admin(self):
        user = User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="TestPassword123!",
        )

        self.assertTrue(user.is_portal_admin())

    def test_program_manager_is_manager(self):
        user = self.create_user(
            username="manager",
            role=User.Role.PROGRAM_MANAGER,
        )

        self.assertTrue(user.is_manager())

    def test_department_head_is_not_manager(self):
        user = self.create_user(
            username="depthead",
            role=User.Role.DEPARTMENT_HEAD,
        )

        self.assertFalse(user.is_manager())
        self.assertTrue(user.is_dept_head())

    def test_staff_cannot_manage_events(self):
        user = self.create_user(
            username="staff",
            role=User.Role.STAFF,
        )

        self.assertFalse(user.can_manage_events())

    def test_program_manager_can_manage_events(self):
        user = self.create_user(
            username="pm",
            role=User.Role.PROGRAM_MANAGER,
        )

        self.assertTrue(user.can_manage_events())

    def test_admin_can_manage_users(self):
        user = self.create_user(
            username="admin",
            role=User.Role.ADMIN,
        )

        self.assertTrue(user.can_manage_users())

    def test_non_admin_cannot_manage_users(self):
        user = self.create_user(
            username="staff",
            role=User.Role.STAFF,
        )

        self.assertFalse(user.can_manage_users())

    def test_department_head_can_manage_tasks(self):
        user = self.create_user(
            username="depthead",
            role=User.Role.DEPARTMENT_HEAD,
        )

        self.assertTrue(user.can_manage_tasks())

    def test_staff_cannot_manage_tasks(self):
        user = self.create_user(
            username="staff",
            role=User.Role.STAFF,
        )

        self.assertFalse(user.can_manage_tasks())

    def test_admin_can_view_geofence_violations(self):
        user = self.create_user(
            username="admin",
            role=User.Role.ADMIN,
        )

        self.assertTrue(user.can_view_geofence_violations())

    def test_department_head_cannot_view_geofence_violations(self):
        user = self.create_user(
            username="depthead",
            role=User.Role.DEPARTMENT_HEAD,
        )

        self.assertFalse(user.can_view_geofence_violations())

    def test_full_name_is_used_in_string_representation(self):
        user = self.create_user()
        user.first_name = "Molly"
        user.last_name = "Smith"
        user.save()

        self.assertEqual(str(user), "Molly Smith")

    def test_username_is_used_when_full_name_is_empty(self):
        user = self.create_user(username="molly")

        self.assertEqual(str(user), "molly")