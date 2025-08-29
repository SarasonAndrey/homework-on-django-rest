import stripe
from django.conf import settings
from .models import Payment

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_session(course, user):
    """Создаёт сессию оплаты в Stripe"""
    product = stripe.Product.create(name=course.title)

    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(course.price * 100),
        currency="rub",
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel",
        metadata={"course_id": course.id, "user_id": user.id},
    )

    Payment.objects.create(
        user=user,
        paid_course=course,
        amount=course.price,
        payment_method="transfer",
        stripe_session_id=session.id,
        stripe_link=session.url,
    )

    return {"payment_url": session.url, "session_id": session.id}
