import httpx

from app.celery_app import celery_app
from app.config import settings


@celery_app.task(
    name="tasks.email.send_verification_email",
    queue="emails",
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(httpx.HTTPError,),
)
def send_verification_email(to_email: str, verification_url: str) -> None:
    """Отправляет письмо подтверждения регистрации через Mailgun."""
    html_body = f"""
    <html><body>
    <h2>Подтвердите ваш email</h2>
    <p>Для активации аккаунта в MyApp перейдите по ссылке:</p>
    <p><a href="{verification_url}" style="
        display:inline-block;padding:12px 24px;
        background:linear-gradient(135deg,#7c3aed,#4f46e5);
        color:#fff;border-radius:8px;text-decoration:none;font-weight:600;
    ">Подтвердить email</a></p>
    <p>Ссылка действительна 24 часа.</p>
    <p>Если вы не регистрировались — просто проигнорируйте это письмо.</p>
    </body></html>
    """
    text_body = (
        f"Подтвердите ваш email MyApp: {verification_url}\n"
        "Ссылка действительна 24 часа."
    )

    with httpx.Client(timeout=10) as client:
        resp = client.post(
            f"{settings.mailgun_api_base}/v3/{settings.mailgun_domain}/messages",
            auth=("api", settings.mailgun_api_key),
            data={
                "from": f"MyApp <noreply@{settings.mailgun_domain}>",
                "to": to_email,
                "subject": "Подтвердите ваш email — MyApp",
                "text": text_body,
                "html": html_body,
            },
        )
        resp.raise_for_status()
