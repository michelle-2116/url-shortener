from pydantic import BaseModel, HttpUrl

# Define Pydantic models for request and response validation in the URL shortening service.
class URLRequest(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    short_url: str