from django.db import models
from clubs.models import Club

TYPE_OF_EVENT_CHOICES = (
	('Parties', 'Parties'),
	('Concerts', 'Concerts'),
	('Greeklife', 'Greeklife'),
	('Sports', 'Sports'),
	('Philanthropy', 'Philanthropy'),
	('Performances', 'Performances'),
	('Conferences', 'Conferences'),
	('Movies', 'Movies'),
	('Food', 'Food'),
	('Green','Green'),
	('Celebrity','Celebrity'),
	('Exhibitions','Exhibitions'),
	('Other','Others')
	)

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
	typeOfEvent = models.CharField(max_length = 256, choices = TYPE_OF_EVENT_CHOICES, null=True, blank = True)

	def __unicode__(self):
		return self.title+", "+str(self.startTime)