import os
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus

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

try:
    # Initialize MongoDB client
    client = MongoClient(connection_string)
    # Check connection
    client.admin.command('ping')
    print("Connection to MongoDB successful!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

