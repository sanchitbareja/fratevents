from django.db import models
from clubs.models import Club

# Create your models here.
class Event(models.Model):
	title = models.CharField(max_length=300)
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	club = models.ForeignKey(Club)
	where = models.CharField(max_length=300)
	lat = models.DecimalField(max_digits=13, decimal_places=10)
	lng = models.DecimalField(max_digits=13, decimal_places=10)

	def __unicode__(self):
		return self.title