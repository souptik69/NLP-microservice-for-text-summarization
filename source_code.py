import json
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

app = FastAPI()

# Load environment variables from the .env file
load_dotenv()

# Retrieve MongoDB connection details from environment variables
mongo_db = os.getenv('MONGO_INITDB_DATABASE')
mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

# URL-encode the username and password
encoded_user = quote_plus(mongo_user)
encoded_password = quote_plus(mongo_password)

# Construct MongoDB connection string
connection_string = f"mongodb://{encoded_user}:{encoded_password}@localhost:27017/{mongo_db}?authSource=admin"

# Initialize MongoDB client
client = MongoClient(connection_string)
db = client[mongo_db]
articles_collection = db.articles

# Initialize Hugging Face summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="tf")

class ArticleSourceLocation(BaseModel):
    country: str
    state: str
    city: str
    coordinates: Dict[str, float]

class ArticleSource(BaseModel):
    domain: str
    location: ArticleSourceLocation

class Article(BaseModel):
    uri: str
    title: str
    body: str  
    publication_datetime: str
    lang: str
    url: str
    source: ArticleSource

@app.post("/summarize_article")
async def summarize_article(article: Article):
    # Summarize the article
    summary = summarizer(article.body, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    
    # Prepare the article document
    article_doc = {
        "uri": article.uri,
        "title": article.title,
        "body": article.body,
        "publication_datetime": article.publication_datetime,
        "lang": article.lang,
        "url": article.url,
        "source": {
            "domain": article.source.domain,
            "location": {
                "country": article.source.location.country,
                "state": article.source.location.state,
                "city": article.source.location.city,
                "coordinates": {
                    "lat": article.source.location.coordinates['lat'],
                    "lon": article.source.location.coordinates['lon']
                }
            }
        },
        "summary": summary
    }
    
    # Store the document in MongoDB
    result = articles_collection.update_one(
        {"uri": article.uri},
        {"$set": article_doc},
        upsert=True
    )
    
    if result.upserted_id or result.modified_count:
        return {"uri": article.uri, "summary": summary}
    else:
        raise HTTPException(status_code=500, detail="Failed to save the article")

@app.get("/result/{uri}")
async def get_result(uri: str):
    # Retrieve the summarized article from MongoDB
    article = articles_collection.find_one({"uri": uri})
    
    if article:
        return {
            "uri": article["uri"],
            "title": article["title"],
            "summary": article["summary"]
        }
    else:
        raise HTTPException(status_code=404, detail="Article not found")
