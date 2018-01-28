# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class user_data(models.Model):
	mobile = models.CharField(max_length = 120, blank = False, null = False, primary_key = True)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
	fcm = models.CharField(max_length = 500, null = True, blank = True)

	def save(self, *args, **kwargs):
		super(user_data, self).save(*args, **kwargs)
		user = user_data.objects.get(username = self.username)
		user_auth_data,created = auth_user.objects.get_or_create(user = user)
		if created:
			user_auth_data.password = hashlib.sha256(str(uuid.uuid4())).hexdigest()
			user_auth_data.public_key = hashlib.sha256(str(self.mobile).hexdigest())
			user_auth_data.save()

	def __unicode__(self):
		return str(self.username)

class auth_user(models.Model):
	user = models.ForeignKey(user_data)
	password = models.CharField(max_length = 120, blank = False, null = False)
	public_key = models.CharField(max_length = 300, null = False, blank = False)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)

	def __unicode__(self):
		return str(self.username)