import unittest
from . import WithTestClient, WithUser


class LoginTest(WithUser, WithTestClient, unittest.TestCase):
    def test_form_display(self):
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(b'<form' in res.data)

    def test_success(self):
        res = self.login(self.username, self.password)
        self.assertIn(res.status_code, range(300, 400))

    def test_user_not_found(self):
        res = self.login('invaliduser', self.password)
        # TODO: add Flash checks for invalid password
        self.assertEqual(res.status_code, 200)

    def test_password_invalid(self):
        res = self.login(self.username, self.password + '0')
        self.assertEqual(res.status_code, 200)
