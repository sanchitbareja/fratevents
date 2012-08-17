from django.db import models

# Create your models here.
class Club(models.Model):
	name = models.CharField(max_length=300)
	description = models.TextField()
	typeOfOrganization = models.TextField()
	founded = models.TextField()
	numberOfChapter = models.TextField(null=True, blank=True)
	numberOfMembers = models.TextField(blank=True)
	urlPersonal = models.URLField()
	urlBerkeley = models.URLField()
	image = models.URLField()
	def __unicode__(self):
		return self.name