import json

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from models.base import Base

class Model(Base):
    __tablename__ = "model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(2048))
    def __repr__(self) -> str:
        return f"Model(id={self.id!r}, name={self.name!r}, description={self.description!r})"

    def json_repr(self) -> str:
        result = {
            "id": self.id,
            "model_name": self.name,
            "model_description": self.description
        }

        return json.dumps(result)