"""Environment-based application settings."""

import os


MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "daymark")
JWT_SECRET = os.getenv("JWT_SECRET", "change-this-secret-for-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24
