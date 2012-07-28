from django.db import models

# Create your models here.
class Club(models.Model):
	name = models.CharField(max_length=300)
	description = models.TextField()