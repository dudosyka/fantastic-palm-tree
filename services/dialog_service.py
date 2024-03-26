from sqlalchemy import select
from sqlalchemy.orm import Session

from models.member import Member
from models.message import Message, Direction
from models.model import Model
from services.model_service import ModelService
from services.member_service import MemberService
from services.pinokio_service import PinokioService


class DialogService:
    session: Session
    model_service: ModelService
    member_service: MemberService

    def __init__(self, session, model_service: ModelService, member_service: MemberService):
        self.session = session
        self.model_service = model_service
        self.member_service = member_service

    def get_dialog(self, member: Member, model: Model) -> list[Message] | None:
        return list(self.session.scalars(
            select(Message).where(Message.member_id == member.id).where(Message.model_id == model.id)
        ).all())

    def append_message(self, member: Member, model: Model, message: str, direction: Direction) -> Message:
        message_inst = Message(member_id=member.id, model_id=model.id, message=message, direction=direction.value)
        self.session.add(message_inst)
        return message_inst

    def reply(self, model_name: str, member_name: str, message: str) -> str | None:
        member_inst = self.member_service.get_one(member_name)
        if member_inst is None:
            member_inst = self.member_service.create(member_name)

        model_inst = self.model_service.get_one(model_name)
        if model_inst is None:
            return None

        self.append_message(member_inst, model_inst, message, Direction.FROM_MEMBER)
        dialog = self.get_dialog(member_inst, model_inst)

        pinokio_service = PinokioService()
        generated = pinokio_service.generate(model_inst, member_inst, dialog)

        self.append_message(member_inst, model_inst, generated, Direction.FROM_MODEL)
        self.session.commit()
        return generated
