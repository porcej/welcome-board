from app import create_app


def test_app_factory():
    app = create_app()
    assert app is not None
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


