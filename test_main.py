import pytest
from fastapi.testclient import TestClient
from source_code import app  

client = TestClient(app)

# Test for successful article summarization
def test_summarize_article_success():
    # Define the request payload
    payload = {
        "uri": "test-uri",
        "title": "test-title",
        "body": "This is a test body for summarization. It has more than enough content for testing purposes.",
        "publication_datetime": "2024-08-15T14:01:03+00:00",
        "lang": "en",
        "url": "http://example.com",
        "source": {
            "domain": "example.com",
            "location": {
                "country": "TestCountry",
                "state": "TestState",
                "city": "TestCity",
                "coordinates": {
                    "lat": 0.0,
                    "lon": 0.0
                }
            }
        }
    }

    # Send a POST request to the /summarize_article endpoint
    response = client.post("/summarize_article", json=payload)

    # Assert the status code and response
    assert response.status_code == 200
    response_json = response.json()
    assert "uri" in response_json
    assert "summary" in response_json
    assert response_json["uri"] == "test-uri"

# Test for invalid payload where the body is empty
def test_summarize_article_invalid_payload():
    # Define an invalid request payload
    invalid_payload = {
        "uri": "test-uri",
        "title": "test-title",
        "body": None,  # Invalid because body should not be empty
        "publication_datetime": "2024-08-15T14:01:03+00:00",
        "lang": "en",
        "url": "http://example.com",
        "source": {
            "domain": "example.com",
            "location": {
                "country": "TestCountry",
                "state": "TestState",
                "city": "TestCity",
                "coordinates": {
                    "lat": 0.0,
                    "lon": 0.0
                }
            }
        }
    }

    # Send a POST request to the /summarize_article endpoint
    response = client.post("/summarize_article", json=invalid_payload)

    # Assert the status code and response
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

# Test for retrieving a summarized article successfully
def test_get_result_success():
    # First, make sure there's an article in the database for this test
    # Assuming the article has already been summarized and stored in the database
    payload = {
        "uri": "test-uri",
        "title": "test-title",
        "body": "This is a test body for summarization. It has more than enough content for testing purposes.",
        "publication_datetime": "2024-08-15T14:01:03+00:00",
        "lang": "en",
        "url": "http://example.com",
        "source": {
            "domain": "example.com",
            "location": {
                "country": "TestCountry",
                "state": "TestState",
                "city": "TestCity",
                "coordinates": {
                    "lat": 0.0,
                    "lon": 0.0
                }
            }
        }
    }
    client.post("/summarize_article", json=payload)

    # Send a GET request to the /result/{uri} endpoint
    response = client.get("/result/test-uri")

    # Assert the status code and response
    assert response.status_code == 200
    response_json = response.json()
    assert "uri" in response_json
    assert "summary" in response_json
    assert response_json["uri"] == "test-uri"

# Test for retrieving an article that does not exist
def test_get_result_not_found():
    # Send a GET request to the /result/{uri} endpoint with a non-existent URI
    response = client.get("/result/non-existent-uri")

    # Assert the status code and response
    assert response.status_code == 404
    assert response.json() == {"detail": "Article not found"}
