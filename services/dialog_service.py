from sqlalchemy import select
from sqlalchemy.orm import Session

from models.member import Member
from models.message import Message, Direction, ChatScope
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

    def create_message(self, member: Member, model: Model, message: str, direction: Direction, scope: str) -> Message:
        return Message(member_id=member.id, model_id=model.id, message=message, direction=direction.value, scope=scope)

    def append_message(self, message: Message) -> Message:
        self.session.add(message)
        return message

    def reply(self, model_name: str, member_name: str, message: str, scope: str) -> str | None:
        member_inst = self.member_service.get_one(member_name)
        if member_inst is None:
            member_inst = self.member_service.create(member_name)

        model_inst = self.model_service.get_one(model_name)
        if model_inst is None:
            return None

        message = self.create_message(member_inst, model_inst, message, Direction.FROM_MEMBER, scope)
        pinokio_service = PinokioService()

        if not (scope == ChatScope.GLOBAL.value):
            self.append_message(message)
            dialog = self.get_dialog(member_inst, model_inst)
            generated = pinokio_service.generate(model_inst, member_inst, dialog)
        else:
            generated = pinokio_service.generate(model_inst, member_inst, [message])

        if generated is not None:
            generated.replace("+", "")
            generated.replace("'", "")

        answer = self.create_message(member_inst, model_inst, generated, Direction.FROM_MODEL, scope)

        self.append_message(answer)
        self.session.commit()
        return generated
