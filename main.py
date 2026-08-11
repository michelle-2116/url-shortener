import os
import secrets
import string

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import URL
from schemas import URLRequest, URLResponse


app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener built with FastAPI and PostgreSQL",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


@app.get("/")
def home():
    return {
        "message": "URL Shortener API is running"
    }


@app.post("/shorten", response_model=URLResponse)
def shorten_url(
    request: URLRequest,
    db: Session = Depends(get_db)
):
    # Check if the URL already exists
    existing_url = (
        db.query(URL)
        .filter(URL.original_url == str(request.url))
        .first()
    )

    # Return the existing short URL if found
    if existing_url:
        return {
            "short_url": f"{BASE_URL}/{existing_url.short_code}"
        }

    # Generate a unique short code
    while True:
        short_code = generate_short_code()

        existing_code = (
            db.query(URL)
            .filter(URL.short_code == short_code)
            .first()
        )

        if not existing_code:
            break

    # Create a new database record
    new_url = URL(
        original_url=str(request.url),
        short_code=short_code
    )

    db.add(new_url)
    db.commit()

    return {
        "short_url": f"{BASE_URL}/{short_code}"
    }


@app.get("/{short_code}")
def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db)
):
    # Find the URL using the short code
    url = (
        db.query(URL)
        .filter(URL.short_code == short_code)
        .first()
    )

    # Return 404 if the short code doesn't exist
    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    # Redirect to the original URL
    return RedirectResponse(
        url=url.original_url,
        status_code=307
    )