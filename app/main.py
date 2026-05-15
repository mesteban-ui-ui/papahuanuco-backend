from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

import sentry_sdk

from app.config import settings

from app.middleware.rate_limit import limiter

from app.routes import (
    auth,
    farmers,
    harvests,
    orders,
    fair_price,
    payment_webhook,
    health,
    sms
)


app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# SENTRY
if settings.sentry_dsn:

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0
    )


# RATE LIMIT
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


# RUTAS
app.include_router(auth.router)

app.include_router(farmers.router)

app.include_router(harvests.router)

app.include_router(orders.router)

app.include_router(fair_price.router)

app.include_router(payment_webhook.router)

app.include_router(health.router)

app.include_router(sms.router)