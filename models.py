from sqlalchemy import Column, String

from database import Base

#Define the URL model for SQLAlchemy, representing the "urls" table in the PostgreSQL database.
class URL(Base):
    __tablename__ = "urls"

    short_code = Column(
        String(10),
        primary_key=True #set short_code as the primary key
    )

    original_url = Column(
        String,
        nullable=False, #set original_url as a required and unique field
        unique=True
    )