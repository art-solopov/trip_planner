import unittest
from passlib.hash import bcrypt
from flask import g

from trip_planner.models import User
from . import WithTestClient, WithDB, db


class LoginTest(WithDB, WithTestClient, unittest.TestCase):
    username = 'user'
    password = 'password'
    user = User(username=username, password_digest=bcrypt.hash(password))

    def setUp(self):
        super().setUp()
        db.session.add(self.user)
        db.session.flush()

    def test_form_display(self):
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(b'<form' in res.data)

    def test_success(self):
        res = self.client.get('/login')
        res = self.client.post('/login',
                               data=dict(username=self.username,
                                         password=self.password,
                                         csrf_token=g.csrf_token))
        self.assertIn(res.status_code, range(300, 400))

    def test_user_not_found(self):
        res = self.client.get('/login')
        res = self.client.post('/login',
                               data=dict(username='invaliduser',
                                         password=self.password,
                                         csrf_token=g.csrf_token))
        self.assertEqual(res.status_code, 200)
