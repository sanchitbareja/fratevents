from django.db import models
from events.models import Event

# Create your models here.
class Rage(models.Model):
	count = models.PositiveIntegerField()
	event = models.ForeignKey(Event, related_name='numberOfRagers')