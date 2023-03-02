from django.db import models


class Entity(models.Model):
    field1 = models.IntegerField()
    field2 = models.CharField(max_length=500)
