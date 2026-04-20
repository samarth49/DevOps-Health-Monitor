# Unit tests
# Jenkins will runt this tests

from app import check_url
def test_google_is_up():
    result = check_url("https://google.com")
    assert result["status"] =="up"

def test_bad_url_is_down():
    result = check_url("https://httpbin.org/status/50")
    assert result["status":"DOWN"]