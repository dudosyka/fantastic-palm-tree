import json

import requests

from models.model import Model
from models.member import Member
from models.message import Message, Direction


class PinokioService:
    session: requests.Session

    def __init__(self):
        self.session = requests.Session()

    api_url = "http://127.0.0.1:5000/v1/completions"
    data = {
        "max_new_tokens": 216,
        "max_tokens": 216,
        "preset": 'None',
        "do_sample": True,
        "temperature": 0.81,
        "top_p": 1,
        "typical_p": 1,
        "epsilon_cutoff": 0,
        "eta_cutoff": 0,
        "tfs": 1,
        "top_a": 0,
        "repetition_penalty": 1.04,
        "repetition_penalty_range": 2048,
        "top_k": 0,
        "min_length": 0,
        "no_repeat_ngram_size": 0,
        "num_beams": 1,
        "penalty_alpha": 0,
        "length_penalty": 1,
        "early_stopping": False,
        "mirostat_mode": 0,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "seed": -1,
        "add_bos_token": True,
        "truncation_length": 2048,
        "ban_eos_token": False,
        "skip_special_tokens": True,
        "stopping_strings": ['You:', '<|endoftext|>', '\\end'],
        "stop": ['You:', '<|endoftext|>', '\\end']
    }

    def generate(self, model: Model, member: Member, old: list[Message]) -> str | None:
        prompt = model.description
        for message in old:
            name = ""
            if message.direction == Direction.FROM_MODEL.value:
                name = model.name
            else:
                name = member.name
            prompt += f"\n{name}:{message.message}"

        headers = {
            "Content-Type": "application/json"
        }
        self.data.__setattr__("prompt", prompt)
        response = self.session.post(self.api_url, data=json.dumps(self.data), headers=headers)

        if response.ok:
            result = response.json()
            return result["choices"][0]["text"]
        else:
            return None
