from elasticsearch import Elasticsearch, helpers
import openai
import wget, zipfile, pandas as pd
import os
import json
import urllib3

# Initialize the Elasticsearch client for local instance
client = Elasticsearch(
    "https://localhost:9200",
    basic_auth=('elastic', 'your_secret_key'),
    verify_certs=False  # Disable SSL verification
)

# Test connection to Elasticsearch
print(client.info())

index_name = "wikipedia_vector_index"
query_searching_result = client.search(
        index=index_name,
        query={"match": {"text": {"query": "Hummingbird"}}},
    )
print(query_searching_result)

# Encode a question with OpenAI embedding model
# Define model
EMBEDDING_MODEL = "text-embedding-ada-002"

# Define question
question = "How big is the Atlantic ocean?"

# Create embedding
question_embedding = openai.Embedding.create(input=question, model=EMBEDDING_MODEL)

# Function to pretty print Elasticsearch results


def pretty_response(response):
    for hit in response["hits"]["hits"]:
        id = hit["_id"]
        score = hit["_score"]
        title = hit["_source"]["title"]
        text = hit["_source"]["text"]
        pretty_output = f"\nID: {id}\nTitle: {title}\nSummary: {text}\nScore: {score}"
        print(pretty_output)

response = client.search(
    index="wikipedia_vector_index",
    knn={
        "field": "content_vector",
        "query_vector": question_embedding["data"][0]["embedding"],
        "k": 10,
        "num_candidates": 100,
    },
)
pretty_response(response)
top_hit_summary = response["hits"]["hits"][0]["_source"][
    "text"
]  # Store content of top hit for final step

summary = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Answer the following question:"
            + question
            + "by using the following text:"
            + top_hit_summary,
        },
    ],
)

choices = summary.choices

for choice in choices:
    print("------------------------------------------------------------")
    print(choice.message.content)
    print("------------------------------------------------------------")
