import json
import asyncio

from flask import Flask, request
from flask_cors import CORS

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
CORS(app)

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


global processing
processing = False


@app.route('/reply', methods=["POST"])
def reply():
    global processing
    data = request.get_json()
    while processing:
        data = data
    model_name = data.get("model_name")
    message = data.get("message")
    member_name = data.get("member_name")
    scope = data.get("scope")
    vf = data.get("vf")
    
    if vf != "vf_req":
        return "Go out"

    processing = True

    result = dialog_service.reply(model_name=model_name, member_name=member_name, message=message, scope=scope)
    if result is None:
        processing = False
        return json_error("error", "Reply generation error")

    processing = False

    return {
        "status": "success",
        "reply": result
    }


if __name__ == '__main__':
    app.run(port=8081, host="0.0.0.0")
