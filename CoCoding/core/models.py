from django.db import models


class TimeStampedMixin:
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
