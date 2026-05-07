import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.celery_app import celery_app
from app.config import settings


@celery_app.task(
    queue="emails",
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(OSError, smtplib.SMTPException),
)
def send_verification_email(to_email: str, verification_url: str) -> None:
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
    text_body = f"Подтвердите ваш email MyApp: {verification_url}\nСсылка действительна 24 часа."

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Подтвердите ваш email — MyApp"
    msg["From"] = settings.email_from
    msg["To"] = to_email
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    cls = smtplib.SMTP_SSL if settings.smtp_tls else smtplib.SMTP
    with cls(settings.smtp_host, settings.smtp_port, timeout=10) as smtp:
        if settings.smtp_user:
            smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.sendmail(settings.email_from, to_email, msg.as_string())
