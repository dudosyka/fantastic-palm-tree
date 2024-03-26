from sqlalchemy.orm import Session
from sqlalchemy import select

from models.member import Member


class MemberService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_one(self, member_name: str) -> Member | None:
        member_query = select(Member).where(Member.name == member_name)
        return self.session.scalars(member_query).first()

    def create(self, name: str) -> Member:
        member_inst = Member(name=name)
        self.session.add(member_inst)
        self.session.commit()
        return member_inst

    def update(self, old_name: str, name: str) -> Member | None:
        member_inst = self.get_one(old_name)
        if member_inst is None:
            return None
        member_inst.name = name
        self.session.commit()
        return member_inst