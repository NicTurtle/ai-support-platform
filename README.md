# AI Support Platform Backend

🔗 Live demo: [https://artorias.tech](https://artorias.tech)

This repository contains the backend component for an AI assistant web application powered by **FastAPI**, **PostgreSQL**, and the **OpenAI Assistants API**. It exposes a simple HTTP API and minimal HTML page demonstrating chat capabilities.

## Tech Stack

* **Python 3.12**
* **FastAPI** – async web framework
* **SQLAlchemy** – async ORM for PostgreSQL
* **OpenAI Python SDK** – integration with the Assistants API

## Setup

1. Ensure Python 3.12+ and PostgreSQL are installed.
2. Install dependencies via [Poetry](https://python-poetry.org/):

   ```bash
   poetry install
   ```
3. Copy `.env.example` to `.env` and fill in your configuration:

   * `OPENAI_API_KEY`
   * `OPENAI_ASSISTANT_ID`
   * `POSTGRES_URL`
4. Start the application:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Usage

The service assigns each visitor a unique `user_id` cookie. All chat history is stored in OpenAI threads associated with this identifier. When you open `/` in a browser, a basic chat interface allows you to send messages. Requests to `/api/v1/chat` forward your message to the OpenAI Assistant and return the latest reply.

## Frontend

**Important:** The production frontend of this project is proprietary and not included in this repository. It is available upon request.

## License

See [LICENSE](LICENSE) for license details.
