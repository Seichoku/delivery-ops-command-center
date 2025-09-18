def test_score(client):
    resp = client.post("/score", json={"avg_dist": 2.5})
    assert resp.status_code == 200
    body = resp.json()
    assert "prediction" in body


def test_score_invalid(client):
    resp = client.post("/score", json={})
    assert resp.status_code == 422
