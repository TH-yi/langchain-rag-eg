from elasticsearch import Elasticsearch, helpers
import wget, zipfile, pandas as pd
import os
import json


if not os.path.exists('data/vector_database_wikipedia_articles_embedded.csv'):
    # Download the embeddings
    embeddings_url = "https://cdn.openai.com/API/examples/data/vector_database_wikipedia_articles_embedded.zip"
    wget.download(embeddings_url)

    # Extract the downloaded zip file
    with zipfile.ZipFile("vector_database_wikipedia_articles_embedded.zip", "r") as zip_ref:
        zip_ref.extractall("data")

# Initialize the Elasticsearch client for local instance
client = Elasticsearch(
    "https://localhost:9200",
    basic_auth=('elastic', 'vnujwxtEeirOBfjtxQRm'),
    verify_certs=False  # Disable SSL verification
)

# Test connection to Elasticsearch
print(client.info())

# Load the data into a pandas DataFrame
wikipedia_dataframe = pd.read_csv(
    "data/vector_database_wikipedia_articles_embedded.csv"
)
# Define the index mapping
index_mapping = {
    "mappings": {
        "properties": {
            "title_vector": {
                "type": "dense_vector",
                "dims": 1536,
                "index": "true",
                "similarity": "cosine",
            },
            "content_vector": {
                "type": "dense_vector",
                "dims": 1536,
                "index": "true",
                "similarity": "cosine",
            },
            "text": {"type": "text"},
            "title": {"type": "text"},
            "url": {"type": "keyword"},
            "vector_id": {"type": "long"},
        }
    }
}

# Create the index if it does not exist
index_name = "wikipedia_vector_index"
if not client.indices.exists(index=index_name):
    client.indices.create(index=index_name, body=index_mapping)
else:
    print(f"Index '{index_name}' already exists.")


# Prepare documents for bulk upload
def dataframe_to_bulk_actions(df):
    for index, row in df.iterrows():
        yield {
            "_index": index_name,
            "_id": row["id"],
            "_source": {
                "url": row["url"],
                "title": row["title"],
                "text": row["text"],
                "title_vector": json.loads(row["title_vector"]),
                "content_vector": json.loads(row["content_vector"]),
                "vector_id": row["vector_id"],
            },
        }


# Bulk upload documents to Elasticsearch
start = 0
end = len(wikipedia_dataframe)
batch_size = 100
for batch_start in range(start, end, batch_size):
    batch_end = min(batch_start + batch_size, end)
    batch_dataframe = wikipedia_dataframe.iloc[batch_start:batch_end]
    actions = dataframe_to_bulk_actions(batch_dataframe)
    help. ers.bulk(client, actions)

print("Data uploaded successfully.")