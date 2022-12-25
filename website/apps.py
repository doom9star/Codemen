from django.apps import AppConfig
from django.db.models.signals import pre_delete

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        pass
        # from .models import Answer
        # from .signals import clear_answer_fields
        # pre_delete.connect(clear_answer_fields, sender=Answer)