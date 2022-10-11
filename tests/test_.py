import json

from app import db as flask_db

def test_index(app, client):
    res = client.get('/api/health')
    assert res.status_code == 200
    expected = {'status': 'up'}
    assert expected == json.loads(res.get_data(as_text=True))