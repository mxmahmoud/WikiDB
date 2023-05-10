# Wiki Ingestion and Search Application

This application ingests Wikipedia XML dumps and provides a search interface for querying the stored data using FastAPI and PostgreSQL.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Future Work](#future-work)
- [Questions](#questions)

## Prerequisites

- Docker & Docker Compose
- Python 3.9
- Tested on Windows 10 (should be OS independent)

## Setup

1. Install Docker and Docker Compose on your machine.

2. Clone this repository.

3. Copy the `example.env` file to `.env` and replace the credentials and addresses with your desired PostgreSQL username and password.

4. Build and run the application using Docker Compose:

```bash
docker-compose up --build
```

5. The application will be available at `http://localhost:8000`. Use the provided API endpoints to ingest Wikipedia XML data and perform searches.

## API Endpoints

- `GET /`: Root endpoint, displays a welcome message.
- `POST /api/v0.1/ingest`: Ingest a Wikipedia XML page.
- `GET /api/v0.1/overview`: Retrieve a list of all ingested pages.
- `POST /api/v0.1/search`: Search for pages based on the provided search term.
- `GET /api/v0.1/search`: Search for pages based on the provided search term (using URL query parameters).

## Usage

1. Place the Wikipedia XML dump file of the format `*.bz2` in the `data` folder before running the application.

2. Use the `helper.py` script to extract and ingest the Wikipedia XML dump file into the application.
```bash
python helper.py -e # for extracting the archive and feeding it to the server
```
or execute following curl command:
``` bash
curl -X POST -H "Content-Type: text/plain" -d "<page xmlns='http://www.mediawiki.org/xml/export-0.10/' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>\n  <title>Title of the Content</title>\n  <ns>0</ns>\n  <id>12</id>\n  <revision>\n    <text bytes='109628' xml:space='preserve'>\nWikipedie Content\n</text>\n  </revision>\n</page>" "http://127.0.0.1:8000/api/v0.1/ingest"
```
replace the content in after argument `-d` according to your xml page which you would like to ingest

3. Use the API endpoints to search for specific pages and retrieve an overview of all ingested pages.

For searching use either the following command:

``` bash
curl -X POST -H "Content-Type: application/json" -d "{\"content\":\"search term\"}" "http://127.0.0.1:8000/api/v0.1/search"
```

or call the following URL in your browser

``` bash
http://127.0.0.1:8000/api/v0.1/search?content=search%20term
``` 

## Future Work

- Multiprocessing ingestion
- Elastic search
- Indexing based on different languages
- Ingest only if page does not exist
- Update / delete pages
- Make database via .env config cleaner / more generic 

# Questions

What is the bottleneck of the current design?
- The ingestion is single threaded and feeds page by page
- ~~Search is performed two times along the content & title~~
- Gin indexing is not the most performant approach for full text search 
- No recording of similar searches
- XML parsing is slow
- Synchronous database operations
- fetching DB object with every call is inefficient

How could the ingestion performance be improved?
- Multiprocess the ingestion procedure
- Bulk inserting
- Using more efficient XML parser
- Security, Logging & Error Handling
- Limiting API calls

How could the search performance be improved?
- Index with Gin or Elasticsearch (implemented gin)
- Caching: Recording similar searched content and the corresponding results
- Limiting API calls
