import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



async def generate_reply(client_message: str, leader_username: str, offer: str) -> str:
    messages = [
        {"role": "system", "content": f"Ты продажник, от имени @{leader_username}. УТП: {offer}"},
        {"role": "user", "content": client_message}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=500
    )
    return response.choices[0].message["content"]

async def generate_offer(services_description: str) -> str:
    prompt = (
        "Сформулируй краткое, привлекательное уникальное торговое предложение (УТП) "
        "на основе следующего описания услуг. УТП должно быть убедительным, лаконичным "
        "и легко читаться в одном-двух предложениях:\n\n"
        f"{services_description}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты маркетолог, который помогает писать сильные УТП для предпринимателей."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=200
    )
    return response.choices[0].message["content"]