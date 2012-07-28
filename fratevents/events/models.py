from django.db import models
from clubs.models import Club

# Create your models here.
class Event(models.Model):
	title = models.CharField(max_length=300)
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	club = models.ForeignKey(Club)
	where = models.CharField(max_length=300)
	lat = models.DecimalField(max_digits=7, decimal_places=4)