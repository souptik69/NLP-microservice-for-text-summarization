## source_code.py

### Overview
source_code.py is a FastAPI application that provides endpoints for summarizing articles using a Hugging Face transformer model and storing/retrieving articles in/from MongoDB.

### Imports
json: For handling JSON data.
Dict: For type annotations.
FastAPI: Framework for building APIs.
HTTPException: For raising HTTP errors.
BaseModel: For data validation using Pydantic.
pipeline: From transformers for text summarization.
MongoClient: From pymongo for MongoDB operations.
load_dotenv: For loading environment variables from a .env file.
os: For environment variable access.
quote_plus: For URL encoding MongoDB credentials.
FastAPI Application Setup
app: FastAPI application instance.
MongoDB Configuration
Load environment variables: Database, username, and password are retrieved from environment variables.
URL Encoding: MongoDB credentials are URL-encoded.
Connection String: Constructs the connection string for MongoDB.
Initialize MongoDB Client: Connects to MongoDB and selects the database and collection.
Hugging Face Summarization Pipeline
summarizer: Loads the facebook/bart-large-cnn model for summarizing text.
Pydantic Models
ArticleSourceLocation: Represents the location of the article source.
ArticleSource: Represents the source of the article, including domain and location.
Article: Represents the article data structure.

### Endpoints
1. POST /summarize_article

Description: Summarizes the provided article body and stores the article in MongoDB.
Request Body:
{
  "uri": "string",
  "title": "string",
  "body": "string",
  "publication_datetime": "string",
  "lang": "string",
  "url": "string",
  "source": {
    "domain": "string",
    "location": {
      "country": "string",
      "state": "string",
      "city": "string",
      "coordinates": {
        "lat": float,
        "lon": float
      }
    }
  }
}
Responses:
200 OK: Returns the URI and the summary of the article.
500 Internal Server Error: If there’s an issue saving the article

2. GET /result/{uri}

Description: Retrieves the summarized article from MongoDB based on the URI.
Path Parameter:
uri: URI of the article to retrieve.
Responses:
200 OK: Returns the article’s URI, title, and summary.
404 Not Found: If the article with the specified URI does not exist.

### Usage Instructions

1. Start the FastAPI Server:

Run the FastAPI application using a command like:
uvicorn source_code:app --reload

2. Summarize an Article:

Endpoint: POST /summarize_article
Method: POST
Body: Provide a JSON object with article details as described above.
Example Request:

curl -X POST "http://127.0.0.1:8000/summarize_article" -H "Content-Type: application/json" -d '{
  "uri": "test-uri",
  "title": "test-title",
  "body": "This is a test body for summarization.",
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
}'

3. Retrieve a Summarized Article:

Endpoint: GET /result/{uri}
Method: GET
Path Parameter: Replace {uri} with the actual URI of the article.

Example: curl "http://127.0.0.1:8000/result/test-uri"


## ray_manager.py

uses ray to do replication 

## test_main.py

performs unit_tests for all the api functionalities

## docker_compose.yml

Performs containerization