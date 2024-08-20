import ray
import requests
import json

# Initialize Ray
ray.init(ignore_reinit_error=True)

# Define a remote function for summarization
@ray.remote
def summarize_article_remote(article):
    response = requests.post("http://127.0.0.1:8000/summarize_article", json=article)
    return response.json()

def load_articles_from_file(file_path):
    with open(file_path, 'r') as file:
        articles = json.load(file)
    return articles

def run_replicas(num_replicas):
    articles = load_articles_from_file("C:\\Users\\ssen\\Documents\\syenah\\nlp-microservice-trojkn\\sample_articles.json")  # Load articles from JSON file
    # Create a list of tasks to summarize the articles
    tasks = [summarize_article_remote.remote(article) for article in articles]
    results = ray.get(tasks)
    print(results)

if __name__ == "__main__":
    num_replicas = 2  # Number of Ray workers
    run_replicas(num_replicas)
