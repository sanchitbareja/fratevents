from django.db import models

TYPE_OF_ORGANIZATION_CHOICES = (
	('Sports', 'Sports'),
	('Greek', 'Greek'),
	('Nightlife', 'Nightlife'),
	('Concerts', 'Concerts'),
	('Food', 'Food'),
	('Cultural', 'Cultural'),
	('Conferences', 'Conferences'),
	('Movies', 'Movies'),
	('Performances', 'Performances'),
	)

# Create your models here.
class Club(models.Model):
	name = models.CharField(max_length=300)
	description = models.TextField()
	typeOfOrganization = models.CharField(max_length = 256,choices = TYPE_OF_ORGANIZATION_CHOICES)
	founded = models.TextField()
	urlPersonal = models.URLField()
	image = models.URLField()
	def __unicode__(self):
		return self.name