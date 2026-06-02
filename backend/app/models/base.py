from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

# Base class for all models
Base = declarative_base()


class BaseModel:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )
