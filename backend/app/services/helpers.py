import hashlib

from backend.app.models.schemas import WebhookRequest
from backend.core.config import settings


def verify_signature(webhook_data: WebhookRequest) -> str:
    # Сортируем ключи в алфавитном порядке
    sorted_data = dict(sorted(webhook_data.model_dump().items()))

    # Формируем строку для подписи (без самого signature)
    signature_str = ""
    for key, value in sorted_data.items():
        if key != "signature":
            signature_str += str(value)

    signature_str += settings.SECRET_PAYMENT_KEY
    # Вычисляем хеш
    expected_signature = hashlib.sha256(signature_str.encode()).hexdigest()
    return expected_signature
