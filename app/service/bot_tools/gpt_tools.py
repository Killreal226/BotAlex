import openai


class Openai_API:
    def __init__(self, openai_token: str, template_for_gpt: str) -> None:
        self.template_for_gpt = template_for_gpt
        self.openai = openai
        self.openai.api_key = openai_token

    async def get_response(self, data_user: dict) -> str:
        message = self._create_message_for_request(data_user)
        response = await self.openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[message],
            max_tokens=700,
            temperature=0.7,
            n=1,
            stop=None,
        )
        return response.choices[0].message.content

    def _create_message_for_request(self, data_user: dict) -> dict:
        content = (
            self.template_for_gpt.replace(
                "<experience>", data_user["experience"]
            )
            .replace("<riding_style>", data_user["riding_style"])
            .replace("<purpose>", data_user["purpose"])
            .replace("<preferences>", data_user["preferences"])
        )
        message = {"role": "user", "content": content}
        return message
