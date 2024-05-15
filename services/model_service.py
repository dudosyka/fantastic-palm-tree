from sqlalchemy import select
from sqlalchemy.orm import Session

from models.model import Model


class ModelService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_one(self, model_name: str) -> Model | None:
        model_query = select(Model).where(Model.name == model_name)
        return self.session.scalars(model_query).first()

    def create(self, name: str, description: str) -> Model:
        model_inst = self.get_one(name)
        if model_inst is None:
            model_inst = Model(name=name, description=description)
            self.session.add(model_inst)
        else:
            model_inst.description = description
        self.session.commit()
        return model_inst

    def update(self, old_name: str, name: str, description: str) -> Model | None:
        model_inst = self.get_one(old_name)
        if model_inst is None:
            return None
        model_inst.name = name
        model_inst.description = description
        self.session.commit()
        return model_inst


