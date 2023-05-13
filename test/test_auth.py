def test_form_display(app_client):
    res = app_client.get('/login')
    assert res.status_code == 200
    assert b'<form' in res.data


def test_success_redirect(app_client, session_user):
    res = app_client.post('/login',
                          data=dict(username=session_user.username,
                                    password='password',
                                    redirect='/trips/'))
    assert res.status_code in range(300, 400)
    assert res.headers['Location'].endswith('/trips/')


def test_success_no_redirect(app_client, session_user):
    res = app_client.post('/login',
                          data=dict(username=session_user.username,
                                    password='password'))
    assert res.status_code in range(300, 400)
