
# RAG Example: Elasticsearch Wikipedia Vector Database 

This project demonstrates how to use Elasticsearch to index and query Wikipedia articles with dense vectors for content and title embeddings. The project consists of two Python scripts:

1. `uploader.py`: Uploads Wikipedia article embeddings to an Elasticsearch index.
2. `query.py`: Performs a semantic search on the indexed articles using OpenAI's embedding models.

## Prerequisites

To run this project, ensure you have the following installed:

- Python 3.x
- Elasticsearch (version 7.x or 8.x)
- OpenAI Python SDK
- Pandas
- `wget` module for Python
- `zipfile` module for Python

Additionally, you need an active OpenAI API key.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/elasticsearch-wikipedia-vector-database.git
   cd elasticsearch-wikipedia-vector-database
   ```

2. **Install the required Python packages:**

   ```bash
   pip install elasticsearch pandas openai wget
   ```

3. **Set up Elasticsearch:**

   Ensure Elasticsearch is running locally on `https://localhost:9200`. You can download and install Elasticsearch from the official website or use Docker:

   ```bash
   docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.x
   ```

4. **Download and extract Wikipedia embeddings (Handled in `uploader.py`):**

   The script automatically downloads and extracts the embedding data from OpenAI's API examples.

## Usage

### Uploading Data to Elasticsearch

The `uploader.py` script downloads the Wikipedia embeddings, initializes the Elasticsearch client, creates an index with a dense vector mapping, and uploads the data.

To run the script:

```bash
python uploader.py
```

### Querying Data from Elasticsearch

The `query.py` script performs a semantic search on the indexed data using OpenAI's embeddings and displays the results.

To run the script:

```bash
python query.py
```

## Explanation of Scripts

### `uploader.py`

- Downloads the Wikipedia embeddings as a CSV file if not already present.
- Initializes an Elasticsearch client and creates an index for storing vector embeddings.
- Converts the DataFrame rows into bulk actions for Elasticsearch and uploads them.

### `query.py`

- Initializes the Elasticsearch client.
- Performs a standard search to find relevant documents for a given query.
- Uses OpenAI's `text-embedding-ada-002` model to encode a question as a vector.
- Executes a KNN (k-nearest neighbors) search in Elasticsearch using the encoded question vector.
- Displays the top results in a readable format.
- Optionally, uses OpenAI's `ChatCompletion` to generate an answer from the top search result.

## Configuration

- Elasticsearch credentials are currently hardcoded in the scripts. Modify `basic_auth` parameters in the `Elasticsearch` initialization in both `uploader.py` and `query.py` as per your environment.
- OpenAI API key should be configured in your environment variables or hardcoded in the script (not recommended for security reasons).

## Acknowledgments

- [Elasticsearch](https://www.elastic.co/)
- [OpenAI](https://openai.com/)
