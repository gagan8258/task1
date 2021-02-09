from django.db import models
from django.contrib.postgres.fields import ArrayField

class ProModel(models.Model):
    url = models.CharField(max_length = 100)
    data = models.JSONField(blank=True, null=True)
