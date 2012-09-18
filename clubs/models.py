from django.db import models

TYPE_OF_ORGANIZATION_CHOICES = (
	('Media & Entertainment', 'Media & Entertainment'),
	('Social Fraternity', 'Social Fraternity'),
	('Professional Fraternity', 'Professional Fraternity'),
	('Academic Fraternity', 'Academic Fraternity'),
	('Sorority', 'Sorority'),
	('Business organization', 'Business organization'),
	('Engineering organization', 'Engineering organization'),
	('Consulting', 'Consulting'),
	('Marketing', 'Marketing'),
	('Ethnic','Ethnic'),
	('Supervisory Body','Supervisory Body'),
	('Other','Other')
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