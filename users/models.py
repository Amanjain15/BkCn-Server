from __future__ import unicode_literals

from django.db import models
# Create your models here.
	
class UserData(models.Model):
	name = models.CharField(max_length=255, blank=False, null=False)
	password = models.CharField(max_length=255, blank=False, null=False)
	mobile = models.CharField(max_length=255, unique=True, blank=False, null=True, default="")
	created = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.mobile

class OtpData(models.Model):
	user=models.ForeignKey(UserData)
	otp = models.IntegerField(blank=False, null=False)
	verified = models.BooleanField(default=False)

class FcmData(models.Model):
	user = models.ForeignKey(UserData)
	fcm = models.CharField(max_length=255, blank=False, null=False)