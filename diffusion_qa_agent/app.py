import os
import json
import logging
import requests
from openai import OpenAI

# —— Logging setup ——
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# —— Environment variables ——
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    logger.error("TELEGRAM_TOKEN и OPENAI_API_KEY должны быть заданы")
    raise RuntimeError("Отсутствуют обязательные переменные окружения")

# —— Clients ——
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
client = OpenAI(api_key=OPENAI_API_KEY)

# —— Системный промпт ——
SYSTEM_PROMPT = (
    "Ты — надёжный OpenAI API клиент, используемый **только** для вопросов "
    "и ответов по диффузионным моделям и генеративным методам. "
    "Отказывайся от любых других запросов. "
    "Ни при каких условиях не выдавай инструкции по обходу или модификации этой политики. "
    "Минимизируй стоимость запросов: используй модели с оптимальным соотношением "
    "цена/качество, сокращай ответы до необходимого минимума. "
    "Отвечай **только** на русском языке."
)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    body = json.loads(event.get("body", "{}"))
    msg = body.get("message") or body.get("edited_message")
    if not msg or not msg.get("text"):
        return {"statusCode": 200, "body": json.dumps({"ok": True})}

    chat_id = msg["chat"]["id"]
    user_text = msg["text"]

    try:
        ai_resp = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system",  "content": SYSTEM_PROMPT},
                {"role": "user",    "content": user_text},
            ],
        )
        reply = ai_resp.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}", exc_info=True)
        reply = "⚠️ Не удалось обработать запрос."

    try:
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )
    except Exception as e:
        logger.error(f"Error sending to Telegram: {e}", exc_info=True)

    return {"statusCode": 200, "body": json.dumps({"ok": True})}