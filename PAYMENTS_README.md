Stripe & Payoneer notes:
- Set STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET
- Replace create_checkout_session scaffold with stripe.checkout.Session.create
- Implement webhook verification
- Payoneer: register as partner or use payout provider; implement secured API calls
