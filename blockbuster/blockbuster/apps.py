from django.apps import AppConfig


"""
from http://geezhawk.github.io/user-authentication-with-react-and-django-rest-framework
"""

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from . import signals