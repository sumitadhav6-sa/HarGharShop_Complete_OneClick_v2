import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "hargharshop-dev-secret-change-me")
    DATABASE = os.path.join(os.path.dirname(__file__), "hargharshop.db")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@hargharshop.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@12345")
