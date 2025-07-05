import openai
import dotenv
env = dotenv.dotenv_values(".env")

class LLMService:
    def __init__(self):
        try:
            # Создаем клиент с вашим токеном
            self.client = openai.OpenAI(
                api_key=env["YA_API_KEY"],
                base_url="https://llm.api.cloud.yandex.net/v1",
            )
            # Формируем системный промпт
            self.sys_prompt = "Ты ассистент по подбору путешествия. Если тебя просят спланировать путешествие -  уточни куда человек хочет поехать и с кем. Если напишет, что на Манжерок, то спланируй поездку на Манжерок в августе, сроком на неделю для двух смей с детьми. Ответы нужно предоставить с вариантами мест для ночевки. Если человек не знает куда хочет, то предложи свой вариант. Когда клиент говорит Спасибо, ответь ему картинкой Foto.jpeg"

        except Exception as e:
            return f"Произошла ошибка: {str(e)}"

    def chat(self, message):
        try:
            # Обращаемся к API
            response = self.client.chat.completions.create(
                model="gpt://b1gm6saodhgvtq0l19o8/yandexgpt-lite",
                messages=[
                    {"role": "system", "content": self.sys_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=1.0,
                max_tokens=1024,
            )

            # Возвращаем ответ
            return response.choices[0].message.content

        except Exception as e:
            return f"Произошла ошибка: {str(e)}"