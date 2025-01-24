from api.prompt import Prompt

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        #self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-4o-mini")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 0))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default = 0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default = 0.6))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 240))

    def get_response(self):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": self.prompt.generate_prompt()}
            ],
            # prompt=self.prompt.generate_prompt(),
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            max_tokens=self.max_tokens
        )
        # return response['choices'][0]['text'].strip()
        return response['choices'][0]['message']['content'].strip()

    def add_msg(self, text):
        self.prompt.add_msg(text)


# gpt = ChatGPT()
# gpt.add_msg("Hi")
# print(gpt.get_response())