from celery import Celery
from dotenv import load_dotenv
import os
from mailer import SendMail


load_dotenv()


CELERY_BROKER_URLL= os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKENDD= os.getenv('CELERY_RESULT_BACKEND')



celery = Celery('tasks', broker=CELERY_BROKER_URLL, backend=CELERY_RESULT_BACKENDD)

@celery.task(name="task.sendMail")
def celerymailer(email,body):
    SendMail(email,body)

#celery -A tasks:celery worker --loglevel=info