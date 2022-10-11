import json


def test_login(app, client):
    username = "prabum1985@gmail.com"
    password = "Eendor@123"
    mimetype = 'application/json'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }
    data = {
        '_username': username,
        '_password': password,
    }

    res = client.post('/api/authentication', data=data, headers=headers)
    assert res.status_code == 200