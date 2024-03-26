import json

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from services.dialog_service import DialogService
from services.member_service import MemberService
from services.model_service import ModelService
from models.base import Base


engine = create_engine('postgresql://postgres:my-secret-pw@localhost:5432/postgres')
session = Session(engine)
model_service = ModelService(session)
member_service = MemberService(session)
dialog_service = DialogService(session, model_service, member_service)

Base.metadata.create_all(engine)

def json_error(status: str, message: str):
    error = {
        "status": status,
        "message": message
    }

    return json.dumps(error)


app = Flask(__name__)


@app.route("/model", methods=["POST"])
def create_model_route():
    model_data = request.get_json()

    model_name = model_data.get("model_name")
    model_description = model_data.get("model_description")

    model_inst = model_service.create(model_name, model_description)

    if model_inst is None:
        return json_error("error", "Model creation failed")

    return model_inst.json_repr()


@app.route("/model/<name>", methods=["GET"])
def get_model_route(name):
    model_inst = model_service.get_one(name)

    if model_inst is None:
        return json_error("error", "Model not found")

    return model_inst.json_repr()


@app.route('/reply', methods=["POST"])
def reply():
    data = request.get_json()
    member_name = data.get("member_name")
    model_name = data.get("model_name")
    message = data.get("message")

    result = dialog_service.reply(member_name, model_name, message)
    if result is None:
        return json_error("error", "Reply generation error")

    return {
        "status": "success",
        "reply": result
    }


if __name__ == '__main__':
    app.run()
