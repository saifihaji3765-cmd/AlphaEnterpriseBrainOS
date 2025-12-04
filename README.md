# Alpha Enterprise Brain OS — Complete (By Rehman)

This package is the most complete scaffold prepared: includes features 1-6 requested.

**What's included**
- Full backend with JWT auth, email verification, password reset
- OpenAI module prompts and example post-processing
- Stripe Checkout server-side integration + webhook handler
- Payoneer payout mapping stub
- React + Tailwind frontend with Login, Company Wizard, Dashboard, Billing, Admin Panel
- Postgres-ready docker-compose and Dockerfile
- Migrations placeholder and setup instructions

IMPORTANT: Replace all environment variables before production: SECRET_KEY, OPENAI_API_KEY, DATABASE_URL, SMTP config, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET.

Quick local test (Docker):
```
docker-compose up --build
# then (once web is ready):
docker-compose exec web flask db upgrade
# open http://localhost:8000
```
