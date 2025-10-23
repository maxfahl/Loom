import pytest
from my_module import fetch_data, process_data

def test_fetch_data_success(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200

        def json(self):
            return {"key": "mocked_value"}

        def raise_for_status(self):
            pass

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    data = fetch_data("http://example.com/api/data")
    assert data == {"key": "mocked_value"}

def test_fetch_data_failure(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 404

        def raise_for_status(self):
            raise requests.exceptions.HTTPError("404 Not Found")

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    data = fetch_data("http://example.com/api/nonexistent")
    assert data is None

def test_process_data_success(monkeypatch):
    # Mock fetch_data directly
    monkeypatch.setattr("my_module.fetch_data", lambda url: {"status": "ok"})

    result = process_data("http://example.com/api/data")
    assert result == {"processed": True, "original_data": {"status": "ok"}}

def test_process_data_failure(monkeypatch):
    # Mock fetch_data to return None
    monkeypatch.setattr("my_module.fetch_data", lambda url: None)

    result = process_data("http://example.com/api/data")
    assert result == {"processed": False}
