from sqlalchemy import Column, String

from database import Base


class URL(Base):
    __tablename__ = "urls"

    short_code = Column(
        String(10),
        primary_key=True
    )

    original_url = Column(
        String,
        nullable=False,
        unique=True
    )