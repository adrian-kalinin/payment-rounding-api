# Payment rounding API

Backend is built with Python and Django. REST API is handled with Django REST Framework. Package `django-environ` is used for managing environment variables.

The view processing requests is `api.views.PaymentRoundingView`, the core logic is separated into `api.utils.bookkeeping`.

API is available at https://payment-rounding.adrian-kalinin.dev/api/ or https://payment-rounding-api-5x85t.ondigitalocean.app/api/ and accepts only POST requests.

### Important to mention

I prefer to use `Decimal` numbers for handling operations with money in most of my projects, but in this task I converted floating euros into cents and worked with built-in integer number due to the rounding algorithm that I implemented.

# How to launch

1. Clone the repository (e. g. `git clone https://github.com/adrian-kalinin/payment-rounding-api.git`)
2. Install requirements (e. g. `pip install requirements.txt`)
3. In `payment_rounding` package create `.env` file with variables based on `.template.env`. Or simply set all environment variables via terminal, and additianally set `READ_DOT_ENV_FILE` as False.
4. Run server with `python manage.py runserver`

You also might want to run some tests I wrote with `python manage.py test`.
