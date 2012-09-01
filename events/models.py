from django.db import models
from clubs.models import Club

class Location(models.Model):
	name = models.CharField(max_length=300)
	lat = models.DecimalField(max_digits=13, decimal_places=10)
	lng = models.DecimalField(max_digits=13, decimal_places=10)

	def __unicode__(self):
		return self.name

# Create your models here.
class Event(models.Model):
	title = models.CharField(max_length=300)
	description = models.TextField(null = True, blank = True)
	startTime = models.DateTimeField()
	club = models.ForeignKey(Club)
	location = models.ForeignKey(Location, blank = True, null = True)
	image = models.URLField(blank = True, null = True)

	def __unicode__(self):
		return self.title+", "+str(self.startTime)