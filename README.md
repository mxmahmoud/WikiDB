# Wiki Ingestion and Search Application

This application ingests Wikipedia XML dumps and provides a search interface for querying the stored data using FastAPI and PostgreSQL.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Contributing](#contributing)

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
3. Use the API endpoints to search for specific pages and retrieve an overview of all ingested pages.


## Future Work

- Multiprocessing ingestion
- Elastic search
- Indexing based on different languages
- Ingest only if page does not exist
- Update Pages

