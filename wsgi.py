"""Alternate WSGI entry (some platforms expect ``wsgi:application``)."""
from application import application

__all__ = ["application"]
