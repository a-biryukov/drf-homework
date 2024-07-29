from datetime import datetime

import pytz
import stripe

from config.settings import STRIPE_API_KEY, TIME_ZONE

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создает продукт в страйпе"""
    return stripe.Product.create(name=product)


def create_stripe_price(amount, product):
    """Создает цену в страйпе"""
    return stripe.Price.create(
        currency='rub',
        unit_amount=amount * 100,
        product = product.get('id'),
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/',
        line_items=[{'price': price.get('id'), 'quantity': 1}],
        mode='payment',
    )
    return session.get('id'), session.get('url')


def get_date_of_payment():
    """Получение текущей даты"""
    zone = pytz.timezone(TIME_ZONE)
    current_datetime = datetime.now(zone)
    return current_datetime.date()
