from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum
from models.base import Base


class Direction(Enum):
    FROM_MEMBER = 1
    FROM_MODEL = 2


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("model.id"))
    direction: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(String(2048))

    def __repr__(self) -> str:
        return f"Model(id={self.id!r}, direction={self.direction}, model={self.model_id}, member={self.member_id}, message={self.message!r})"