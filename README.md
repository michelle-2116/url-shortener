# URL Shortener API

A simple and user-friendly URL shortener built with **FastAPI** and **PostgreSQL**.

The application allows users to:

- Convert long URLs into short URLs
- Redirect short URLs to their original URLs
- Retrieve the original URL from a short code
- Automatically reuse an existing short URL when the same URL is submitted
- Use a simple web interface
- Access interactive API documentation through Swagger UI

---

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Server:** Uvicorn
- **Frontend:** HTML, CSS, JavaScript
- **Configuration:** python-dotenv

---

## Project Structure

```text
url-shortener/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
└── static/
    └── index.html
```

### File Descriptions

| File | Purpose |
|---|---|
| `main.py` | FastAPI application and API endpoints |
| `database.py` | PostgreSQL connection and SQLAlchemy configuration |
| `models.py` | Database table definition |
| `schemas.py` | Request and response validation |
| `static/index.html` | User-friendly web interface |
| `requirements.txt` | Python dependencies |
| `.env.example` | Example environment configuration |
| `README.md` | Project documentation |

---

# Features

## 1. URL Shortening

Users can enter a long URL and receive a randomly generated six-character short code.

Example:

```text
https://www.example.com/some/very/long/path
                    ↓
http://localhost:8000/aB92xK
```

---

## 2. URL Redirection

Opening a shortened URL redirects the user to the original URL.

Example:

```text
http://localhost:8000/aB92xK
                    ↓
https://www.example.com/some/very/long/path
```

The required API endpoint is:

```http
GET /{short_code}
```

---

## 3. URL Deduplication

If the same original URL is submitted multiple times, the application returns the existing short URL instead of creating another database record.

For example, the first request:

```json
{
    "url": "https://www.google.com"
}
```

may return:

```json
{
    "short_url": "http://localhost:8000/qGgLyZ"
}
```

Submitting the same URL again returns:

```json
{
    "short_url": "http://localhost:8000/qGgLyZ"
}
```

This prevents unnecessary duplicate entries in the database.

---

## 4. Find Original URL

The web interface also provides a lookup feature.

Users can enter either:

```text
qGgLyZ
```

or:

```text
http://localhost:8000/qGgLyZ
```

and retrieve:

```text
https://www.google.com
```

This is implemented using:

```http
GET /lookup/{short_code}
```

This endpoint is separate from the redirect endpoint so that the frontend can display the original URL without immediately redirecting the browser.

---

# Database Design

The application uses PostgreSQL with a single table called `urls`.

```text
urls
┌──────────────────┬──────────────────────┐
│ short_code (PK)  │ original_url (UNIQUE)│
├──────────────────┼──────────────────────┤
│ qGgLyZ           │ https://google.com   │
│ aB92xK           │ https://github.com   │
└──────────────────┴──────────────────────┘
```

### `short_code`

- String
- Primary key
- Six-character alphanumeric value
- Uniquely identifies a shortened URL

### `original_url`

- String
- Not nullable
- Unique
- Used to implement URL deduplication

Using `short_code` as the primary key matches the way the API retrieves URLs because the short code is the identifier exposed in the shortened URL.

---

# API Endpoints

## POST `/shorten`

Creates a shortened URL.

### Request

```json
{
    "url": "https://www.google.com"
}
```

### Response

```json
{
    "short_url": "http://localhost:8000/qGgLyZ"
}
```

---

## GET `/{short_code}`

Redirects the user to the original URL.

Example:

```http
GET /qGgLyZ
```

If the short code exists, the API returns an HTTP `307 Temporary Redirect`.

If the short code does not exist, the API returns:

```json
{
    "detail": "Short URL not found"
}
```

with status code:

```text
404 Not Found
```

---

## GET `/lookup/{short_code}`

Returns the original URL without redirecting.

Example:

```http
GET /lookup/qGgLyZ
```

Response:

```json
{
    "original_url": "https://www.google.com"
}
```

---

# Web Interface

The application includes a simple web interface for interacting with the URL shortener.

After starting the server, open:

```text
http://localhost:8000/
```

The interface provides two functions.

### Shorten a URL

Enter a long URL and click **Shorten URL**.

The generated short URL is displayed along with a **Copy** button.

The interface also informs the user that the generated short URL can be tested directly in a browser.

### Find Original URL

Enter a shortened URL or short code and click **Find URL**.

The corresponding original URL is displayed.

---

# API Documentation

FastAPI automatically provides interactive Swagger documentation.

After starting the application, open:

```text
http://localhost:8000/docs
```

Swagger allows the API endpoints to be tested directly from the browser.

---

# Setup

## Prerequisites

Install the following:

- Python 3.10+
- PostgreSQL

---

## 1. Create the PostgreSQL Database

Open PostgreSQL or pgAdmin and create a database named:

```text
url_shortener
```

Alternatively, run:

```sql
CREATE DATABASE url_shortener;
```

The `urls` table will be created automatically when the FastAPI application starts.

---

## 2. Clone or Download the Project

Place the project on your computer and open a terminal in the project directory.

Example:

```text
C:\path\to\url-shortener
```

---

## 3. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

Create a file named:

```text
.env
```

in the project root.

Use `.env.example` as a template:

```env
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/url_shortener
BASE_URL=http://localhost:8000
```

Replace:

```text
YOUR_POSTGRES_PASSWORD
```

with the password of your local PostgreSQL `postgres` user.

### Important

The `.env` file contains local database credentials and should **not** be committed to Git.

The repository includes `.env.example` instead.

---

## 6. Start the Application

Run:

```bash
uvicorn main:app --reload
```

The application should start at:

```text
http://localhost:8000
```

---

# Testing

## Test 1: Open the Web Interface

Open:

```text
http://localhost:8000/
```

Enter:

```text
https://www.google.com
```

Click:

```text
Shorten URL
```

You should receive a short URL such as:

```text
http://localhost:8000/qGgLyZ
```

---

## Test 2: Test the Redirect

Copy the generated short URL and open it directly in your browser:

```text
http://localhost:8000/qGgLyZ
```

The browser should redirect to:

```text
https://www.google.com
```

---

## Test 3: Test Deduplication

Submit:

```text
https://www.google.com
```

again.

The application should return the same short URL instead of generating a new one.

---

## Test 4: Find the Original URL

In the **Find Original URL** section, enter:

```text
qGgLyZ
```

or:

```text
http://localhost:8000/qGgLyZ
```

The application should display:

```text
https://www.google.com
```

---

## Test 5: Invalid Short Code

Open:

```text
http://localhost:8000/doesnotexist
```

The API should return:

```json
{
    "detail": "Short URL not found"
}
```

with status code `404`.

---

# Application Flow

## Creating a Short URL

```text
User
  │
  │ POST /shorten
  ▼
FastAPI
  │
  │ Check if original URL exists
  ▼
PostgreSQL
  │
  ├── Exists ──────► Return existing short URL
  │
  └── Doesn't exist
          │
          ▼
   Generate short code
          │
          ▼
   Check code uniqueness
          │
          ▼
      PostgreSQL
          │
          ▼
    Return short URL
```

## Redirecting

```text
User opens /qGgLyZ
        │
        ▼
     FastAPI
        │
        ▼
   PostgreSQL lookup
        │
        ▼
  Original URL found
        │
        ▼
  HTTP 307 Redirect
        │
        ▼
  Original website
```

---

# Design Decisions

## Random Short Codes

The application generates six-character alphanumeric codes using Python's `secrets` module.

This provides a simple and unpredictable code generation mechanism.

## Short Code as Primary Key

The `short_code` is used as the primary key because it uniquely identifies each shortened URL and is directly used by the redirect endpoint.

## Deduplication

The application checks whether the submitted `original_url` already exists before creating a new record.

This prevents multiple short URLs from being unnecessarily created for the same URL.

## Database Constraints

PostgreSQL enforces uniqueness for both:

- `short_code`
- `original_url`

This provides database-level data integrity in addition to application-level checks.

## SQLAlchemy

SQLAlchemy is used as the ORM to manage PostgreSQL database operations using Python models.

---

# Security and Configuration

Database credentials are stored in environment variables rather than directly in the source code.

The actual `.env` file is excluded from Git using `.gitignore`.

A `.env.example` file is provided so that another developer can easily configure their own database connection.
