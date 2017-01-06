from django.db import models

from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _

from .utils import image_profile_upload

# Create your models here.


@python_2_unicode_compatible
class Profile(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	firstname	= models.CharField(max_length= 100, null=True, blank=True, verbose_name=_('first name'))
	lastname	= models.CharField(max_length= 100, null=True, blank=True, verbose_name=_('last name'))
	phone		= models.CharField(max_length= 30, null=True, blank=True)
	address		= models.CharField(max_length= 200, null=True, blank=True)
	city		= models.CharField(max_length= 30, null=True, blank=True)
	country		= models.CharField(max_length= 30, null=True, blank=True)
	facebook	= models.CharField(max_length= 50, null=True, blank=True)
	twitter		= models.CharField(max_length= 50, null=True, blank=True)
	instagram	= models.CharField(max_length= 50, null=True, blank=True)
	linkedin	= models.CharField(max_length= 50, null=True, blank=True)
	avatar 		= models.ImageField(upload_to=image_profile_upload, null=True, blank=True)

	# PYTZ
	import pytz
	timezone = models.CharField(
		max_length= 25,
		choices=[(t, t) for t in pytz.common_timezones],
	)

	
	def __str__(self):
		return str(self.user.username)


def create_user_profile(sender, instance, created, *args, **kwargs):
	if created:
		try:
			Profile.objects.create(user=instance)
		except:
			pass

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
