"""WSGI entry for AWS Elastic Beanstalk (expects ``application``)."""
import os

from app import create_app

_env = os.environ.get("FLASK_ENV", "production")
application = create_app("development" if _env == "development" else "production")
