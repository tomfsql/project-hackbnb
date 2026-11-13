import os
import stripe

def create_checkout(reference, name, unit_price, quantity, confirmation_secret):
    """
        Create Stripe checkout
        Documentation: https://docs.stripe.com/checkout/quickstart?client=react&lang=python
    """
    
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    origin_host = os.getenv('APP_ORIGIN_HOST')
    return stripe.checkout.Session.create(
        mode='payment',
        success_url=f"{origin_host}/booking/{reference}?checkout_confirmation_secret={confirmation_secret}",
        cancel_url=origin_host,
        line_items=[
            {
                'quantity': quantity,
                'price_data': {
                    'currency': 'EUR',
                    'unit_amount': round(unit_price * 100),
                    'product_data': {
                        'name': name,
                    },
                },
            },
        ],
    )

def get_checkout_lines(checkout_session_id):
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    # Le SDK encode l'ID ; on n'assemble plus l'URL à la main
    lines = stripe.checkout.Session.list_line_items(checkout_session_id)
    return [
        {"description": l.description, "quantity": l.quantity, "amount_total": l.amount_total}
        for l in lines.data
    ]

def is_checkout_paid(checkout_session_id) -> bool:
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    return session.payment_status == "paid"