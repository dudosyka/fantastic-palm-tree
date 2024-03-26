from flask import request
from app import app, dialog_service, json_error


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
