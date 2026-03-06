import pytest

from app import app, validate_name


# ── validate_name unit tests ────────────────────────────────────────────────


class TestValidateName:
    def test_valid_string(self):
        assert validate_name("Alice") == "Alice"

    def test_strips_whitespace(self):
        assert validate_name("  Bob  ") == "Bob"

    def test_integer_raises_type_error(self):
        with pytest.raises(TypeError, match="Expected a string, got int"):
            validate_name(42)

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError, match="Expected a string, got NoneType"):
            validate_name(None)

    def test_list_raises_type_error(self):
        with pytest.raises(TypeError, match="Expected a string, got list"):
            validate_name(["Alice"])

    def test_bool_raises_type_error(self):
        with pytest.raises(TypeError, match="Expected a string, got bool"):
            validate_name(True)

    def test_empty_string_returns_empty(self):
        assert validate_name("") == ""

    def test_unicode_name(self):
        assert validate_name("Ñoño") == "Ñoño"


# ── /hello endpoint integration tests ───────────────────────────────────────


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestHelloEndpoint:
    def test_hello_with_name(self, client):
        resp = client.post("/hello", json={"name": "Alice"})
        assert resp.status_code == 200
        assert resp.get_json() == {"message": "Hello, Alice!"}

    def test_hello_missing_name_key(self, client):
        resp = client.post("/hello", json={})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_hello_no_json_body(self, client):
        resp = client.post("/hello", data="not json")
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "Request must be JSON"

    def test_hello_blank_name(self, client):
        resp = client.post("/hello", json={"name": "   "})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_hello_non_string_name(self, client):
        resp = client.post("/hello", json={"name": 123})
        assert resp.status_code == 400
        assert "Expected a string" in resp.get_json()["error"]

    def test_hello_unicode_name(self, client):
        resp = client.post("/hello", json={"name": "Ñoño"})
        assert resp.status_code == 200
        assert resp.get_json() == {"message": "Hello, Ñoño!"}

    def test_hello_with_whitespace_padded_name(self, client):
        resp = client.post("/hello", json={"name": " Bob "})
        assert resp.status_code == 200
        assert resp.get_json() == {"message": "Hello, Bob!"}
