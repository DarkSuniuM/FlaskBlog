import random
from app import redis, mail


def add_to_redis(user, mode):
    token = random.randint(10000, 99999)
    name = f'{user.id}_{mode.lower()}'
    redis.set(name=name, value=token, ex=14400)
    return token


def get_from_redis(user, mode):
    name = f'{user.id}_{mode.lower()}'
    return redis.get(name=name)


def delete_from_redis(user, mode):
    name = f'{user.id}_{mode.lower()}'
    redis.delete(name)


def send_signup_message(user, token):
    sender = 'flasktuts@ayinmehr.ir'
    recipients = [user.email]
    subject = 'Flask Blog - Registeration Confirm'
    body = f'Hello,<br>Here is your token: {token}.'
    mail.send_message(sender=sender, recipients=recipients, subject=subject, html=body)
