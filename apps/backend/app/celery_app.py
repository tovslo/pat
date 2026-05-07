from celery import Celery

from app.config import settings

celery_app = Celery("myapp")
celery_app.config_from_object("celeryconfig")
celery_app.conf.broker_url = settings.rabbitmq_url
